'''Worker endpoints
'''
import datetime as dt
import hashlib
import json
from http import HTTPStatus
from importlib.metadata import version
from tornado.web import RequestHandler

from fishsense_data_processing_worker import __version__
from fishsense_data_processing_worker.jobs import job_ingress_queue, job_schema
from fishsense_data_processing_worker.metrics import get_counter, get_summary
# pylint: disable=abstract-method
# This is a typical behavior for tornado


class OpenAPICompatibleHandler(RequestHandler):
    """OpenAPI Compatible Handler

    Allows for CORS
    """
    # pylint: disable=abstract-method

    def prepare(self):
        request_counter = get_counter(
            name='request_call'
        )
        request_counter.labels(endpoint=self.request.path).inc()
        return super().prepare()

    def on_finish(self):
        request_counter = get_counter(
            name='request_result'
        )
        request_counter.labels(endpoint=self.request.path,
                               code=self._status_code).inc()
        return super().on_finish()

    async def _execute(self, transforms, *args, **kwargs):
        with get_summary('request_timing').labels(endpoint=self.request.path).time():
            await super()._execute(transforms, *args, **kwargs)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PUT')

        return super().set_default_headers()

    def options(self, *_, **__):
        """Options handler
        """
        self.set_status(204)
        self.finish()


class HomePageHandler(OpenAPICompatibleHandler):
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


class JobHandler(OpenAPICompatibleHandler):
    """Job Handler
    """
    SUPPORTED_METHODS = ['PUT', 'OPTIONS']

    async def put(self, *_, **__) -> None:
        """Puts a new job into the job queue
        """
        job_request = json.loads(self.request.body)
        job_schema.validate(job_request)

        jobs = job_request['job']
        cksums = []
        for job in jobs:
            cksum = hashlib.md5()
            cksum.update(json.dumps(job,
                                    separators=(',', ':'),
                                    indent=None,
                                    sort_keys=True).encode())
            digest = cksum.hexdigest()
            cksums.append(digest)
            job_ingress_queue.put((digest, job))
        result = {
            'job_ids': cksums
        }
        self.write(json.dumps(result))


class VersionHandler(OpenAPICompatibleHandler):
    """Version Handler

    """
    SUPPORTED_METHODS = ('GET', 'OPTIONS')

    async def get(self, *_, **__) -> None:
        """Gets the version information for this app
        """
        self.write(json.dumps({
            'version': version('fishsense_data_processing_worker')
        }))
