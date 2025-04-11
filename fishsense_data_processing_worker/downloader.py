'''Download Workers
'''
import logging
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread, current_thread
from typing import Dict, List, Tuple
from urllib.parse import urlparse

import requests

from fishsense_data_processing_worker.metrics import add_thread_to_monitor


class Downloader:
    """Parallel Downloader
    """
    def __init__(self,
                 n_workers: int = 8,
                 ):
        """Initializes the parallel downloader

        Args:
            n_workers (int, optional): Number of worker threads. Defaults to 8.
        """
        self._n_workers = n_workers
        self.stop_event = Event()
        self._job_pickup_queue: Queue[Tuple[str, Dict[str, str], Path]] = Queue()
        self._log = logging.getLogger('Downloader')
        self.workers_ready = Event()
        self._workers: List[Thread] = []

    def _download_worker(self):
        thread_handle = current_thread()
        _log = logging.getLogger(f'Downloader {thread_handle.name}')
        self.workers_ready.set()
        while not self.stop_event.is_set():
            try:
                url, request_headers, output_path = self._job_pickup_queue.get(timeout=1)
            except Empty:
                continue
            _log.debug('Trying %s', url)
            try:
                with requests.session() as session:
                    req = session.get(
                        url=url,
                        headers=request_headers
                    )
                    req.raise_for_status()
                    with open(output_path, 'wb') as handle:
                        handle.write(req.content)
            except requests.exceptions.RequestException as exc:
                self._log.exception('Downloading %s failed: %s',
                                    url, exc)
            finally:
                self._job_pickup_queue.task_done()


    def start(self):
        """Starts the parallel download workers
        """
        self._workers = [
            Thread(
                target=self._download_worker,
                name=f'download_worker_{idx:03d}'
            )
            for idx in range(self._n_workers)
        ]
        for worker in self._workers:
            add_thread_to_monitor(worker)
        for worker in self._workers:
            worker.start()

    def download_urls(self,
                      urls: List[str],
                      request_headers: Dict[str, str],
                      working_dir: Path,
                      timeout: float = None,
                      suffix: str = '.ORF'
                      ) -> Dict[str, Path]:
        """Downloads the specified URLs.

        Args:
            urls (List[str]): List of URLs to download
            request_headers (Dict[str, str]): Request headers to use during download
            working_dir (Path): Directory in which to store the downloaded files
            timeout (float): Seconds to wait for download to complete.  Defaults to None (wait 
                forever).
            suffix (str): Suffix to use.  Defaults to '.ORF'.

        Returns:
            Dict[str, Path]: Output mapping of url to downloaded file
        """
        # pylint: disable=too-many-arguments, too-many-positional-arguments
        if not self.workers_ready.is_set():
            raise RuntimeError('Download works not running!')
        job_output_map: Dict[Path, str] = {}
        for url in urls:
            url_parts = urlparse(url)
            url_path = Path(url_parts.path)
            output_path = (working_dir / url_path.name).with_suffix(suffix)
            if output_path in job_output_map:
                self._log.warning('Multiple paths overlap! %s', output_path)
            if output_path.exists():
                self._log.warning('Path already exists! %s', output_path)
            job_output_map[output_path] = url
        for output_path, url in job_output_map.items():
            self._job_pickup_queue.put((url, request_headers, output_path))
        # hack to get a joinable queue
        join_thread = Thread(
            target=self._job_pickup_queue.join
        )
        join_thread.start()
        join_thread.join(timeout=timeout)
        if join_thread.is_alive():
            # pickup queue is not done!
            self.stop()
            # dump queue
            self._job_pickup_queue = Queue()
            self._log.warning('Dumping queue! Resource leak!')
            # restart workers
            self.start()
            raise TimeoutError()
        return_map: Dict[str, Path] = {}
        for output_path, url in job_output_map.items():
            if not output_path.exists():
                self._log.error('%s was not downloaded!', url)
                continue
            return_map[url] = output_path
        return return_map

    def stop(self):
        """Stops the worker threads
        """
        self.stop_event.set()
        for worker in self._workers:
            worker.join()
