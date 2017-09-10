import sys, time
from navio import adafruit_pwm_servo_driver as pwm
from navio import util
import RPi.GPIO as GPIO
import math

pcaPin            = 27
servoFrequency    = 50
samplingRate      = 1;      # 1 microsecond (can be 1,2,4,5,10)
ppmInputGpio      = 4;      # PPM input on Navio's 2.54 header

def ppmOnEdge(channel):
    print("detected change")

# Set PCA Pin to low
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ppmInputGpio, GPIO.IN)

GPIO.setup(pcaPin, GPIO.OUT)
GPIO.output(pcaPin, GPIO.LOW)

# Set frequency to 50 Hz
pwm = pwm.PWM(0x40, debug=False)
pwm.setPWMFreq(servoFrequency)


GPIO.add_event_detect(ppmInputGpio, GPIO.RISING, callback=ppmOnEdge) 

while 1:
    time.sleep(1)

