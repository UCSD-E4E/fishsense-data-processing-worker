'''Queues
'''
from queue import Queue

from fishsense_data_processing_worker.metrics import get_counter


class InstrumentedQueue(Queue):
    """Instrumented Queue

    Args:
        Queue (_type_): _description_
    """
    def __init__(self, name: str, maxsize = 0):
        self.__put_counter = get_counter(
            name='queue_put'
        )
        self.__get_counter = get_counter(
            name='queue_get'
        )
        self.__name = name
        super().__init__(maxsize)

    def _put(self, item):
        self.__put_counter.labels(queue=self.__name).inc()
        return super()._put(item)

    def _get(self):
        self.__get_counter.labels(queue=self.__name).inc()
        return super()._get()
