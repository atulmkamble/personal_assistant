import time
from loguru import logger


def execution_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"LLM call executed in {end_time - start_time:.2f} seconds.")
        return result
    return wrapper
