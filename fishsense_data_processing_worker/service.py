'''Fishsense Data Processing Worker
'''
import asyncio
import datetime as dt

import pytz
import tornado
from prometheus_client import start_http_server

from fishsense_data_processing_worker.config import configure_logging, settings
from fishsense_data_processing_worker.core import Core
from fishsense_data_processing_worker.handlers import (HomePageHandler,
                                                       JobHandler,
                                                       VersionHandler)
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
            (r'/()', HomePageHandler, {'start_time': start_time}),
            (r'/process_fsl()', JobHandler),
            (r'/version()', VersionHandler)
        ])

        self.core = Core(db=settings.core.db)

    async def run(self):
        """Main entry point
        """
        start_http_server(9090)
        system_monitor_thread.start()
        self._app.listen(80)
        self.core.start()

        await self.stop_event.wait()

        self.core.stop()


def main() -> None:
    """Main entry point
    """
    asyncio.run(Service().run())


if __name__ == '__main__':
    main()
