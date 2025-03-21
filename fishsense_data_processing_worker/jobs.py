'''Jobs
'''
from typing import Any, Dict

import schema

from fishsense_data_processing_worker.queue import InstrumentedQueue

__preprocess_schema = schema.Schema({
    'display_name': str,
    'job_name': 'preprocess',
    'parameters': {
        'overwrite': schema.Optional(bool),
        'data': [str],
        'lens-calibration': str,
        'format': schema.Or('JPG', 'PNG'),
        'output': str
    }
})

__preprocess_laser_schema = schema.Schema({
    'display_name': str,
    'job_name': 'preprocess_with_laser',
    'parameters': {
        'overwrite': schema.Optional(bool),
        'data': [str],
        'lens-calibration': str,
        'format': schema.Or('JPG', 'PNG'),
        'output': str
    }
})

job_schema = schema.Schema({
    'job': [schema.Or(
        __preprocess_laser_schema,
        __preprocess_schema
    )]
})

job_ingress_queue: InstrumentedQueue[Dict[str, Any]] = InstrumentedQueue(
    name='job_ingress')
