'''Core logic
'''
import contextlib
import json
import logging
import sqlite3
from pathlib import Path
from queue import Empty
from threading import Event, Thread

from fishsense_data_processing_worker.jobs import job_ingress_queue
from fishsense_data_processing_worker.metrics import add_thread_to_monitor, get_counter
from fishsense_data_processing_worker.sql import do_query, do_script

class UnknownJobTypeException(RuntimeError):
    """Unknown Job Type Exception
    """
class Core:
    """Core logic
    """
    TABLE_MAPPING = {
        'preprocess': Path('sql/insert_new_preprocess_job.sql'),
        'preprocess_with_laser': Path('sql/insert_new_preprocess_with_laser_job.sql')
    }
    def __init__(self, db: Path = Path('./data/jobs.db')):
        self.stop_event = Event()
        self.__db = db
        db.parent.mkdir(parents=True, exist_ok=True)

        self.__initialize_db()
        self.__ingest_thread = Thread(
            target=self.ingest_thread,
            name='Job Ingest Thread'
        )
        add_thread_to_monitor(self.__ingest_thread)

        self.__process_thread = Thread(
            target=self.process_thread,
            name='Job Process Thread'
        )
        add_thread_to_monitor(self.__process_thread)

    def __initialize_db(self):
        with contextlib.closing(sqlite3.connect(self.__db)) as con, \
                contextlib.closing(con.cursor()) as cur:
            do_script(
                path='sql/initialize_db.sql',
                cur=cur
            )
            con.commit()

    def start(self):
        """Starts core threads
        """
        self.__ingest_thread.start()
        self.__process_thread.start()

    def stop(self):
        """Stops core threads
        """
        self.stop_event.set()
        self.__process_thread.join()
        self.__ingest_thread.join()

    def process_thread(self) -> None:
        """Processes jobs
        """
        __log = logging.getLogger('Job Process Thread')
        try:
            while not self.stop_event.is_set():
                pass
        except Exception as exc: # pylint: disable=broad-except
            __log.exception('Job Process Thread failed due to %s', exc)
            get_counter('errors').labels(exception_type=type(exc).__name__,
                                         context='Job Process Thread').inc()
    def ingest_thread(self) -> None:
        """Ingests jobs
        """
        __log = logging.getLogger('Job Ingest Thread')
        try:
            while not self.stop_event.is_set():
                try:
                    digest, job = job_ingress_queue.get(timeout=5)
                except Empty:
                    continue
                job_type = job['job_name']
                if job_type not in self.TABLE_MAPPING:
                    raise UnknownJobTypeException
                with contextlib.closing(sqlite3.connect(self.__db)) as con, \
                        contextlib.closing(con.cursor()) as cur:
                    do_query(
                        path=self.TABLE_MAPPING[job_type],
                        cur=cur,
                        params={
                            'cksum': digest,
                            'parameters': json.dumps(job,
                                                    separators=(',', ':'),
                                                    indent=None,
                                                    sort_keys=True)
                        }
                    )
                    con.commit()
        except Exception as exc: # pylint: disable=broad-except
            __log.exception('Job Ingest Thread failed due to %s', exc)
            get_counter('errors').labels(exception_type=type(exc).__name__,
                                         context='Job Ingest Thread').inc()