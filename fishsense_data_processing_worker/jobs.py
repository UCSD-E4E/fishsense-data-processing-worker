'''Jobs
'''
import schema

job_schema = schema.Schema({
    'job': [{
        'display_name': str,
        'job_name': ['preprocess'],
        'parameters': {
            'overwrite': schema.Optional(bool),
            'data': [str],
            'lens-calibration': str,
            'format': schema.Or('JPG', 'PNG'),
            'output': str
        }
    }]
})
