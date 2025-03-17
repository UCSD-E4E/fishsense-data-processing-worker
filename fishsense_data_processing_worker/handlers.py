'''Worker endpoints
'''
import datetime as dt
from http import HTTPStatus

from tornado.web import RequestHandler

from fishsense_data_processing_worker import __version__


# pylint: disable=abstract-method
# This is a typical behavior for tornado
class HomePageHandler(RequestHandler):
    """Home Page Handler
    """
    SUPPORTED_METHODS = ['GET']

    def initialize(self, start_time: dt.datetime):
        """Initialization

        Args:
            start_time (dt.datetime): Program start time
        """
        # pylint: disable=attribute-defined-outside-init
        # This is the correct pattern for tornado
        self.__start_time = start_time

    async def get(self, *_, **__) -> None:
        """Handler body
        """
        self.write(
            f'Fishsense Data Processing Worker v{__version__} deployed at '
            f'{self.__start_time.isoformat()}')
        self.set_status(HTTPStatus.OK)
