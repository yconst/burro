import sys
import time
from navio import rcinput, pwm, util

util.check_apm()

rcin = rcinput.RCInput()

while (True):
    period = rcin.read(7)
    print period
    time.sleep(1)
