'''Core thread
'''
import datetime as dt
import json
import logging
import subprocess
from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event, Thread
from typing import Any, Callable, Dict, List, Optional

import requests

from fishsense_data_processing_worker.downloader import Downloader
from fishsense_data_processing_worker.metrics import add_thread_to_monitor


class Core:
    def __init__(self,
                 orchestrator: str,
                 api_key: str,
                 worker_name: str,
                 downloader: Downloader
                 ):
        self._log = logging.getLogger('Core')
        self.__host = orchestrator
        self.__key = api_key
        self._worker_name = worker_name
        self._downloader = downloader
        self.stop_event = Event()

        self._n_images: int = 50

        self._worker_thread = Thread(
            target=self._process_loop,
            name='process_worker'
        )
        add_thread_to_monitor(self._worker_thread)

        self._operation_map: Dict[str,
                                  Callable[[str, List[str], int, Optional[str]], None]] = {
            'preprocess': self._preprocess,
            'preprocess_with_laser': self._preprocess_with_laser
        }

    def _process_loop(self):
        while not self.stop_event.is_set():
            # Get next set of jobs
            with requests.Session() as session:
                retrieve_batch_url = f'{self.__host}/api/v1/jobs/retrieve_batch'
                response = session.post(
                    url=retrieve_batch_url,
                    headers={
                        'api_key': self.__key
                    },
                    params={
                        'nImages': self._n_images,
                        'worker': self._worker_name,
                        'expiration': int((dt.datetime.now() + dt.timedelta(minutes=60)).timestamp())
                    }
                )
                if response.status_code != HTTPStatus.OK:
                    self._log.error('Failed to retrieve %s: %d',
                                    retrieve_batch_url, response.status_code)
                    self.stop_event.wait(1)
                    continue
                job_definition: Dict = response.json()
                jobs: List[Dict] = job_definition['jobs']
                for job in jobs:
                    job_id: str = job['jobId']
                    frame_ids: List[str] = job['frameIds']
                    camera_id: int = job['cameraId']
                    dive_id: Optional[str] = job['diveId']

                    operation: str = job['operation']

                    self._log.debug('Got job %s to %s frames %s on camera %s, dive %s',
                                    job_id,
                                    operation,
                                    frame_ids,
                                    camera_id,
                                    dive_id
                                    )

                    process_fn = self._operation_map[operation]

                    self._log.debug('Using fn %s', process_fn.__name__)
                    try:
                        process_fn(job_id, frame_ids, camera_id, dive_id)
                    except Exception as exc:
                        self._log.exception('Failed: %s', exc)
                        session.put(
                            url=f'{self.__host}/api/v1/jobs/status',
                            params={
                                'jobId': job_id,
                                # TODO switch to failed later, this only for dev
                                'status': 'cancelled'
                            },
                            headers={
                                'api_key': self.__key
                            }
                        )
                        raise exc

    def _preprocess_with_laser(self, job_id: str, frame_ids: List[str], camera_id: int, _: Optional[str]):
        # pylint: disable=too-many-locals
        raw_urls = [
            f'{self.__host}/api/v1/data/raw/{frame_id}' for frame_id in frame_ids
        ]
        request_headers = {
            'api_key': self.__key
        }
        laser_urls = [
            f'{self.__host}/api/v1/data/laser/{frame_id}' for frame_id in frame_ids
        ]
        lens_cal_url = f'{self.__host}/api/v1/data/lens_cal/{camera_id}'
        with TemporaryDirectory() as raw_files_dir, \
                TemporaryDirectory() as lens_cal_dir, \
                TemporaryDirectory() as laser_label_dir, \
                TemporaryDirectory() as job_dir, \
                TemporaryDirectory() as output_dir:
            raw_files = Path(raw_files_dir)
            lens_cal_path = Path(lens_cal_dir)
            laser_label_path = Path(laser_label_dir)
            output_path = Path(output_dir)
            job_dir_path = Path(job_dir)

            raw_file_paths = self._downloader.download_urls(
                urls=raw_urls,
                request_headers=request_headers,
                working_dir=raw_files
            )
            lens_cal_paths = self._downloader.download_urls(
                urls=[lens_cal_url],
                request_headers=request_headers,
                working_dir=lens_cal_path,
                suffix='.pkg'
            )
            laser_label_paths = self._downloader.download_urls(
                urls=laser_urls,
                request_headers=request_headers,
                working_dir=laser_label_path,
                suffix='.json'
            )
            laser_labels: List[Dict[str, Any]] = []
            for url, label_path in laser_label_paths.items():
                with open(label_path, 'r', encoding='utf-8') as handle:
                    laser_label: Dict[str, int] = json.load(handle)
                    laser_label['cksum'] = url.split('/')[-1]
                    laser_labels.append(laser_label)
            label_studio_dump = [
                {
                    'id': task['task_id'],
                    'data': {
                        'img': (raw_files / str(task['cksum'])).with_suffix('.JPG').as_posix(),
                    },
                    'annotations': [
                        {
                            'result': [
                                {
                                    'value': {
                                        'x': task['x'] / 4014 * 100,
                                        'y': task['y'] / 3016 * 100,
                                    },
                                    'original_width': 4014,
                                    'original_height': 3016
                                }
                            ]
                        }
                    ]
                }
                for task in laser_labels
            ]
            with open(laser_label_path / 'label_studio_dump.json', 'w', encoding='utf-8') as handle:
                blob = json.dumps(label_studio_dump)
                handle.write(blob)
            self._log.debug('Label studio dump: %s', blob)
            job_document = {
                'jobs': [
                    {
                        'display_name': job_id,
                        'job_name': 'preprocess_with_laser',
                        'parameters': {
                            'data': [path.as_posix() for path in raw_file_paths.values()],
                            'lens-calibration': lens_cal_paths[lens_cal_url].as_posix(),
                            'format': 'JPG',
                            'output': output_path.as_posix(),
                            'laser-labels': (laser_label_path / 'label_studio_dump.json').as_posix(),
                            'debug-path': '/tmp'  # TODO remove this when fsl stops dumping shit into
                            # .debug
                        },
                    }
                ]
            }
            job_path = job_dir_path / 'job.json'
            with open(job_path, 'w', encoding='utf-8') as handle:
                document = json.dumps(job_document, indent=2)
                handle.write(document)
            self._log.info('Executing job %s', document)

            result = subprocess.run(
                ['fsl', 'run-jobs', job_path.as_posix()],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False
            )
            self._log.debug('Subprocess output: %s', result.stdout.decode())
            result.check_returncode()
            self._log.debug('Output dir: %s', list(output_path.glob('*.JPG')))
            with requests.Session() as session:
                for output_file in output_path.glob('*.JPG'):
                    cksum = output_file.stem
                    with open(output_file, 'rb') as handle:
                        response = session.put(
                            url=f'{self.__host}/api/v1/data/laser_jpeg/{cksum}',
                            headers={
                                'api_key': self.__key
                            },
                            data=handle.read()
                        )
                        response.raise_for_status()
                session.put(
                    url=f'{self.__host}/api/v1/jobs/status',
                    headers={
                        'api_key': self.__key
                    },
                    params={
                        'jobId': job_id,
                        'status': 'completed',
                        'progress': 100
                    }
                ).raise_for_status()

    def _preprocess(self, job_id: str, frame_ids: List[str], camera_id: int, _: Optional[str]):
        # pylint: disable=too-many-locals
        raw_urls = [
            f'{self.__host}/api/v1/data/raw/{frame_id}' for frame_id in frame_ids]
        request_headers = {
            'api_key': self.__key
        }
        lens_cal_url = f'{self.__host}/api/v1/data/lens_cal/{camera_id}'
        with TemporaryDirectory() as raw_files_dir, \
                TemporaryDirectory() as lens_cal_dir, \
                TemporaryDirectory() as job_dir, \
                TemporaryDirectory() as output_dir:
            raw_files = Path(raw_files_dir)
            lens_cal_path = Path(lens_cal_dir)
            output_path = Path(output_dir)
            job_dir_path = Path(job_dir)
            raw_file_paths = self._downloader.download_urls(
                urls=raw_urls,
                request_headers=request_headers,
                working_dir=raw_files
            )
            lens_cal_paths = self._downloader.download_urls(
                urls=[lens_cal_url],
                request_headers=request_headers,
                working_dir=lens_cal_path,
                suffix='.pkg'
            )
            job_document = {
                'jobs': [
                    {
                        'display_name': job_id,
                        'job_name': 'preprocess',
                        'parameters': {
                            'data': [path.as_posix() for path in raw_file_paths.values()],
                            'lens-calibration': lens_cal_paths[lens_cal_url].as_posix(),
                            'format': 'JPG',
                            'output': output_path.as_posix()
                        }
                    }
                ]
            }
            job_path = job_dir_path / 'job.json'
            with open(job_path, 'w', encoding='utf-8') as handle:
                document = json.dumps(job_document, indent=2)
                handle.write(document)
            self._log.info('Executing job %s', document)

            result = subprocess.run(
                ['fsl', 'run-jobs', job_path.as_posix()],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False
            )
            self._log.debug('Subprocess output: %s', result.stdout.decode())
            result.check_returncode()
            self._log.debug('Output dir: %s', list(output_path.glob('*.JPG')))
            with requests.Session() as session:
                for output_file in output_path.glob('*.JPG'):
                    cksum = output_file.stem
                    with open(output_file, 'rb') as handle:
                        response = session.put(
                            url=f'{self.__host}/api/v1/data/preprocess_jpeg/{cksum}',
                            headers={
                                'api_key': self.__key
                            },
                            data=handle.read()
                        )
                        response.raise_for_status()
                session.put(
                    url=f'{self.__host}/api/v1/jobs/status',
                    headers={
                        'api_key': self.__key
                    },
                    params={
                        'jobId': job_id,
                        'status': 'completed',
                        'progress': 100
                    }
                ).raise_for_status()

    def start(self):
        """Starts the core worker thread
        """
        self._worker_thread.start()

    def stop(self):
        """Stops the core worker thread
        """
        self.stop_event.set()
        self._worker_thread.join()
