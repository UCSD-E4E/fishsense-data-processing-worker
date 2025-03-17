'''Fishsense Data Processing Worker
'''
from prometheus_client import start_http_server

from fishsense_data_processing_worker.metrics import system_monitor_thread


class Service:
    """Service class
    """
    # pylint: disable=too-few-public-methods
    # runtime
    def __init__(self):
        pass

    def run(self):
        """Main entry point
        """
        start_http_server(9090)
        system_monitor_thread.start()
        while True:
            pass


def main() -> None:
    """Main entry point
    """
    Service().run()


if __name__ == '__main__':
    main()
