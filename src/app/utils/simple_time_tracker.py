from time import time
from functools import wraps


import logging
from logging.config import fileConfig
fileConfig('/src/app/logging.ini')
logger = logging.getLogger()


def _log(message):
    logger.info('[SimpleTimeTracker] {function_name} {total_time:.3f}'.format(**message))


def simple_time_tracker():
    def _simple_time_tracker(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            start_time = time()

            try:
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time() - start_time

                # log the result
                _log({
                    'function_name': fn.__name__,
                    'total_time': elapsed_time,
                })
                
            return result

        return wrapped_fn
    return _simple_time_tracker