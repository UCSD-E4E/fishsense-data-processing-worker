'''Jobs
'''
from queue import Queue
from typing import Dict, Any

import schema

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

job_ingress_queue: Queue[Dict[str, Any]] = Queue()
