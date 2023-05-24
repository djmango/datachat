import logging
import os
from logging.config import dictConfig

SERVICE_NAME = os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'FastAPI')
INSTANCE_ID = os.environ.get('AWS_REQUEST_ID', 'GENERIC')


class LogFilter(logging.Filter):
    def __init__(self, service=None, instance=None):
        self.service = service
        self.instance = instance

    def filter(self, record):
        record.service = self.service
        record.instance = self.instance
        return True


class GeFormater(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, aws=False):
        self.aws = aws
        super().__init__(fmt=fmt, datefmt=datefmt)

    def formatTime(self, record, datefmt=None):
        if self.aws:
            return ''
        else:
            return super().formatTime(record, datefmt)

    def format(self, record):
        record.service = SERVICE_NAME
        record.instance = INSTANCE_ID
        # NOTE I'm making it so both AWS and local logs have the same format, for now, since when I grep I can't see timestamps otherwise
        if self.aws:
            # fmt = '[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
            fmt = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        else:
            fmt = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        self._style._fmt = fmt
        return super().format(record)

# Configure Logging


def configure_logging(root_level='INFO', app_level='INFO', service=None, instance=None):
    aws = 'AWS_EXECUTION_ENV' in os.environ  # This will disable time in logs when running in AWS Lambda
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            '()': GeFormater,
            'aws': aws
        }},
        'filters': {'default': {
            '()': LogFilter,
            'service': service,
            'instance': instance
        }},
        'handlers': {'default_handler': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['default'],
            'formatter': 'default'
        }},
        'root': {
            'level': root_level,
            'handlers': ['default_handler']
        },
        'loggers': {
            'app': {
                'level': app_level,
            }
        }
    })


configure_logging(root_level='INFO', app_level='DEBUG', service=SERVICE_NAME, instance=INSTANCE_ID)
logger = logging.getLogger(__name__)
