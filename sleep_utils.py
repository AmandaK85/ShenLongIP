import time
import random

def random_sleep(min_seconds=2, max_seconds=5):
    """
    Sleep for a random amount of time between min_seconds and max_seconds.
    Default: 2-5 seconds
    """
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)
    return sleep_time

def short_random_sleep(min_seconds=1, max_seconds=3):
    """
    Sleep for a shorter random amount of time between min_seconds and max_seconds.
    Default: 1-3 seconds (for shorter waits)
    """
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)
    return sleep_time 