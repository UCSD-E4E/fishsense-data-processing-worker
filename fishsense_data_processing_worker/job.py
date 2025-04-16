'''Job Wrapper
'''
import enum
from collections import namedtuple
from pathlib import Path
from typing import List, Optional, Dict

from fishsense_data_processing_worker.downloader import Downloader


class JobType(enum.Enum):
    PREPROCESS = 'preprocess'
    PREPROCESS_WITH_LASER = 'preprocess_with_laser'

class Job:
    def __init__(self,
                 job_id: str,
                 operation: JobType,
                 frame_ids: List[str],
                 camera_id: int,
                 dive_id: Optional[str] = None
                 ):
        self._job_id = job_id
        self._operation = operation
        self._frame_ids = frame_ids
        self._camera_id = camera_id
        self._dive_id = dive_id

    def download_data(self,
                      path: Path,
                      api_key: str,
                      downloader: Downloader,
                      *,
                      server: str = 'https://orchestrator.fishsense.e4e.ucsd.edu'):
        '''
        Download the data from the server using the API key and save it to the specified path.
        '''
        DownloadTarget = namedtuple('DownloadTarget', ['urls', 'path', 'suffix', 'downloaded_files'])
        raw_data = DownloadTarget(
            urls=[
                f'{server}/api/v1/data/raw/{frame_id}' for frame_id in self._frame_ids
            ],
            path=path / 'raw',
            suffix='.ORF',
            downloaded_files={}
        )
        laser_labels = DownloadTarget(
            urls=[
                f'{server}/api/v1/data/laser/{frame_id}' for frame_id in self._frame_ids
            ],
            path=path / 'laser_labels',
            suffix='.JSON',
            downloaded_files={}
        )
        lens_cal = DownloadTarget(
            urls=[f'{server}/api/v1/data/lens_cal/{self._camera_id}'],
            path=path / 'lens_cal',
            suffix='.PKG',
            downloaded_files={}
        )


        operation_download_map: Dict[JobType, List[DownloadTarget]] = {
            JobType.PREPROCESS: [raw_data, lens_cal],
            JobType.PREPROCESS_WITH_LASER: [raw_data, laser_labels, lens_cal]
        }

        download_targets = operation_download_map[self._operation]
        for target in download_targets:
            target.downloaded_files = downloader.download_urls(
                urls=target.urls,
                request_headers={
                    'api_key': api_key,
                },
                working_dir=target.path,
                suffix=target.suffix,
            )