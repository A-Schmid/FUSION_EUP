import time
from .config import *

#default: seconds
def wait(sleep_time):
    time.sleep(sleep_time)

def wait_milliseconds(sleep_time):
    time.sleep(sleep_time / 1000)

def wait_seconds(sleep_time):
    time.sleep(sleep_time)

def wait_minutes(sleep_time):
    time.sleep(sleep_time * 60)

def wait_hours(sleep_time):
    time.sleep(sleep_time * 60 * 24)

def all_elements_equal(list_to_check):
    last_element = list_to_check[0]
    for element in list_to_check:
        if element != last_element:
            return False
        last_element = element
    return True
