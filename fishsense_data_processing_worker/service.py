'''Fishsense Data Processing Worker
'''
import signal
from threading import Event

from prometheus_client import start_http_server

from fishsense_data_processing_worker.config import configure_logging, settings
from fishsense_data_processing_worker.core import Core
from fishsense_data_processing_worker.downloader import Downloader
from fishsense_data_processing_worker.metrics import system_monitor_thread


class Service:
    """Service class
    """
    # pylint: disable=too-few-public-methods
    # runtime
    def __init__(self):
        self.stop_event = Event()
        configure_logging()

        self._downloader = Downloader(
            n_workers=settings.core.max_cpu
        )

        self.core = Core(
            orchestrator=settings.core.orchestrator,
            api_key=settings.core.api_key,
            worker_name=settings.core.worker_name,
            downloader=self._downloader,
            max_cpu=settings.core.max_cpu,
            max_gpu=settings.core.max_gpu,
            batch_size=settings.core.max_batch_size,
        )
        signal.signal(signal.SIGTERM, self.stop_event.set)

    def run(self):
        """Main entry point
        """
        start_http_server(9090)
        system_monitor_thread.start()
        self.core.start()
        self._downloader.start()

        self.stop_event.wait()

        self._downloader.stop()
        self.core.stop()


def main() -> None:
    """Main entry point
    """
    Service().run()


if __name__ == '__main__':
    main()
