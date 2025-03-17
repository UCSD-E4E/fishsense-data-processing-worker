'''Fishsense Data Processing Worker
'''
import asyncio
import datetime as dt

import pytz
import tornado
from prometheus_client import start_http_server

from fishsense_data_processing_worker.config import configure_logging
from fishsense_data_processing_worker.handlers import HomePageHandler
from fishsense_data_processing_worker.metrics import system_monitor_thread


class Service:
    """Service class
    """
    # pylint: disable=too-few-public-methods
    # runtime
    def __init__(self):
        start_time = dt.datetime.now(tz=pytz.UTC)
        self.stop_event = asyncio.Event()
        configure_logging()

        self._app = tornado.web.Application([
            (r'/()', HomePageHandler, {'start_time': start_time})
        ])

    async def run(self):
        """Main entry point
        """
        start_http_server(9090)
        system_monitor_thread.start()
        self._app.listen(80)

        await self.stop_event.wait()


def main() -> None:
    """Main entry point
    """
    asyncio.run(Service().run())


if __name__ == '__main__':
    main()
