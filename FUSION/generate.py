import random
from datetime import datetime
from decimal import Decimal
import numpy

def noise(minimum = 0, maximum = 1):
    return (random.random() * (maximum - minimum)) + minimum

def PWM(duty_cycle = 0.5, frequency = 1):
    if(duty_cycle > 1):
        duty_cycle = 1
    dt = datetime.now()
    if(frequency < 1):
        raise Exception("no frequencies < 1 allowed!")
    if(numpy.mod((dt.microsecond / 1000000.0), (1.0 / frequency)) > duty_cycle / frequency):
        return 0
    else:
        return 1
