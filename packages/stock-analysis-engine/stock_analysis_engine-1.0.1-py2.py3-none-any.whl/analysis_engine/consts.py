"""
Consts and helper functions

Stock and Analysis Environment Variables
----------------------------------------

::

    TICKER = ev(
        'TICKER',
        'SPY')
    TICKER_ID = int(ev(
        'TICKER_ID',
        '1'))
    DEFAULT_TICKERS = ev(
        'DEFAULT_TICKERS',
        'SPY,XLF,XLK,XLI,XLU').split(',')
    NEXT_EXP = analysis_engine.options_dates.option_expiration()
    NEXT_EXP_STR = NEXT_EXP.strftime('%Y-%m-%d')

Logging Environment Variables
-----------------------------

::

    APP_NAME = 'pr'
    LOG_CONFIG_PATH = ev(
        'LOG_CONFIG_PATH',
        './analysis_engine/log/logging.json')

Celery Environment Variables
----------------------------

::

    SSL_OPTIONS = {}
    TRANSPORT_OPTIONS = {}
    WORKER_BROKER_URL = ev(
        'WORKER_BROKER_URL',
        'redis://localhost:6379/13').strip()
    WORKER_BACKEND_URL = ev(
        'WORKER_BACKEND_URL',
        'redis://localhost:6379/14').strip()
    WORKER_TASKS = ev(
        'WORKER_TASKS',
        ('analysis_engine.work_tasks.get_new_pricing_data,'
         'analysis_engine.work_tasks.handle_pricing_update_task,'
         'analysis_engine.work_tasks.publish_from_s3_to_redis,'
         'analysis_engine.work_tasks.publish_pricing_update'))
    INCLUDE_TASKS = WORKER_TASKS.split(',')

Supported S3 Environment Variables
----------------------------------

::

    ENABLED_S3_UPLOAD = ev(
        'ENABLED_S3_UPLOAD',
        '0') == '1'
    S3_ACCESS_KEY = ev(
        'S3_ACCESS_KEY',
        'trexaccesskey')
    S3_SECRET_KEY = ev(
        'S3_SECRET_KEY',
        'trex123321')
    S3_REGION_NAME = ev(
        'S3_REGION_NAME',
        'us-east-1')
    S3_ADDRESS = ev(
        'S3_ADDRESS',
        'localhost:9000')
    S3_SECURE = ev(
        'S3_SECURE',
        '0') == '1'
    S3_BUCKET = ev(
        'S3_BUCKET',
        'pricing')
    S3_KEY = ev(
        'S3_KEY',
        'test_key')

Supported Redis Environment Variables
-------------------------------------

::

    ENABLED_REDIS_PUBLISH = ev(
        'ENABLED_REDIS_PUBLISH',
        '0') == '1'
    REDIS_ADDRESS = ev(
        'REDIS_ADDRESS',
        'localhost:6379')
    REDIS_KEY = ev(
        'REDIS_KEY',
        'test_redis_key')
    REDIS_PASSWORD = ev(
        'REDIS_PASSWORD',
        None)
    REDIS_DB = int(ev(
        'REDIS_DB',
        '4'))
    REDIS_EXPIRE = ev(
        'REDIS_EXPIRE',
        None)

"""

import os
import sys
import json
import analysis_engine.options_dates


def ev(
        k,
        v):
    '''ev

    :param k: environment variable key
    :param v: environment variable value
    '''
    val = os.getenv(k, v)
    if val:
        return val.strip()
    return val
# end of ev


SUCCESS = 0
FAILED = 1
ERR = 2
EX = 3
NOT_RUN = 4
INVALID = 5
NOT_DONE = 6

# version of python
IS_PY2 = sys.version[0] == '2'

APP_NAME = ev(
    'APP_NAME',
    'pr')
LOG_CONFIG_PATH = ev(
    'LOG_CONFIG_PATH',
    './analysis_engine/log/logging.json')
SSL_OPTIONS = {}
TRANSPORT_OPTIONS = {}
WORKER_BROKER_URL = ev(
    'WORKER_BROKER_URL',
    'redis://localhost:6379/13').strip()
WORKER_BACKEND_URL = ev(
    'WORKER_BACKEND_URL',
    'redis://localhost:6379/14').strip()
WORKER_TASKS = ev(
    'WORKER_TASKS',
    ('analysis_engine.work_tasks.get_new_pricing_data,'
     'analysis_engine.work_tasks.handle_pricing_update_task,'
     'analysis_engine.work_tasks.publish_from_s3_to_redis,'
     'analysis_engine.work_tasks.publish_pricing_update'))
INCLUDE_TASKS = WORKER_TASKS.split(',')

########################################
#
# Custom Variables
#
########################################
TICKER = ev(
    'TICKER',
    'SPY')
TICKER_ID = int(ev(
    'TICKER_ID',
    '1'))
DEFAULT_TICKERS = ev(
    'DEFAULT_TICKERS',
    'SPY,XLF,XLK,XLI,XLU').split(',')
NEXT_EXP = analysis_engine.options_dates.option_expiration()
NEXT_EXP_STR = NEXT_EXP.strftime('%Y-%m-%d')


########################################
#
# S3 Variables
#
########################################
ENABLED_S3_UPLOAD = ev(
    'ENABLED_S3_UPLOAD',
    '0') == '1'
S3_ACCESS_KEY = ev(
    'S3_ACCESS_KEY',
    'trexaccesskey')
S3_SECRET_KEY = ev(
    'S3_SECRET_KEY',
    'trex123321')
S3_REGION_NAME = ev(
    'S3_REGION_NAME',
    'us-east-1')
S3_ADDRESS = ev(
    'S3_ADDRESS',
    'localhost:9000')
S3_SECURE = ev(
    'S3_SECURE',
    '0') == '1'
S3_BUCKET = ev(
    'S3_BUCKET',
    'pricing')
S3_KEY = ev(
    'S3_KEY',
    'test_key')

########################################
#
# Redis Variables
#
########################################
ENABLED_REDIS_PUBLISH = ev(
    'ENABLED_REDIS_PUBLISH',
    '0') == '1'
REDIS_ADDRESS = ev(
    'REDIS_ADDRESS',
    'localhost:6379')
REDIS_KEY = ev(
    'REDIS_KEY',
    'test_redis_key')
REDIS_PASSWORD = ev(
    'REDIS_PASSWORD',
    None)
REDIS_DB = int(ev(
    'REDIS_DB',
    '4'))
REDIS_EXPIRE = ev(
    'REDIS_EXPIRE',
    None)


def get_status(
        status):
    """get_status

    Return the string label for an integer status code
    which should be one of the ones above.

    :param status: integer status code
    """
    if status == SUCCESS:
        return 'SUCCESS'
    elif status == FAILED:
        return 'FAILED'
    elif status == ERR:
        return 'ERR'
    elif status == EX:
        return 'EX'
    elif status == NOT_RUN:
        return 'NOT_RUN'
    elif status == INVALID:
        return 'INVALID'
    elif status == NOT_DONE:
        return 'NOT_DONE'
    else:
        return 'unsupported status={}'.format(
            status)
# end of get_status


def ppj(
        json_data):
    """ppj

    :param json_data: dictionary to convert to
                      a pretty-printed, multi-line string
    """
    return str(
        json.dumps(
            json_data,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')))
# end of ppj
