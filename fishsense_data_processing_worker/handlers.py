'''Worker endpoints
'''
import datetime as dt
import hashlib
import json
from http import HTTPStatus

from tornado.web import RequestHandler

from fishsense_data_processing_worker import __version__
from fishsense_data_processing_worker.jobs import job_ingress_queue, job_schema


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


class JobHandler(RequestHandler):
    """Job Handler
    """
    SUPPORTED_METHODS = ['PUT']

    async def put(self, *_, **__) -> None:
        """Puts a new job into the job queue
        """
        job_request = json.loads(self.request.body)
        job_schema.validate(job_request)

        jobs = job_request['job']
        cksums = []
        for job in jobs:
            cksum = hashlib.md5()
            job_ingress_queue.put(job)
            cksum.update(json.dumps(job,
                                    separators=(',', ':'),
                                    indent=None,
                                    sort_keys=True).encode())
            cksums.append(cksum.hexdigest())
        result = {
            'job_ids': cksums
        }
        self.write(json.dumps(result))
