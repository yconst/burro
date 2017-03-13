import sys
import time
import dbus
from navio import rcinput, pwm, leds, util, mpu9250

util.check_apm()

THROTTLE_CHANNEL = 2
YAW_CHANNEL = 0

class Rover:

    def __init__(self):
        self.drift_gain = 0.15
        
        self.throttle_center = 1500.0
        self.yaw_center = 1500.0
        self.roll_center = 1500.0
        self.calibrated = False
        self.videoRunning = False

        self.sysbus = dbus.SystemBus()
        self.systemd1 = self.sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.manager = dbus.Interface(self.systemd1, 'org.freedesktop.systemd1.Manager')

    def run(self):


        self.led = leds.Led()
        self.led.setColor('Yellow')

        self.rcin = rcinput.RCInput()

        self.th_pwm = pwm.PWM(2)
        self.th_pwm.set_period(50)

        self.st_pwm = pwm.PWM(0)
        self.st_pwm.set_period(50)

        self.imu = mpu9250.MPU9250()

        if self.imu.testConnection():
            print "Connection established: True"
        else:
            sys.exit("Connection established: False")

        self.imu.initialize()

        time.sleep(1)

        while True:
            self.led.setColor('Blue')

            if float(self.rcin.read(4)) > 1490:
                if (self.calibrated == False):

                    self.calibrate_rc(self.rcin)
                    self.calibrated = True

                self.led.setColor('Green')

                yaw = (float(self.rcin.read(YAW_CHANNEL)) - self.yaw_center) / 500.0
                throttle = (float(self.rcin.read(THROTTLE_CHANNEL)) - self.throttle_center) / 500.0

                m9a, m9g, m9m = self.imu.getMotion9()
                drift = m9g[2]

                th = min(1, max(-1, -throttle))
                st = min(1, max(-1, -yaw - drift * self.drift_gain))

                self.set_throttle(value=th, pwm_in=self.th_pwm)
                self.set_throttle(value=st, pwm_in=self.st_pwm)
            else:
                self.set_throttle(0, self.th_pwm)
                self.set_throttle(0, self.st_pwm)
                self.calibrated = False

            videoChan = float(self.rcin.read(7))
            if videoChan > 1490 and self.videoRunning == False:
                self.job = self.manager.StartUnit('wbctxd.service', 'fail')
                self.videoRunning = True
                self.led.setColor('Red')
                time.sleep(0.2)
            elif videoChan < 1490 and self.videoRunning == True:
                self.job = self.manager.StopUnit('wbctxd.service', 'fail')
                self.videoRunning = False

            time.sleep(0.02)

    def set_throttle(self, value, pwm_in):
        pwm_val = 1.5 + value * 0.5
        pwm_in.set_duty_cycle(pwm_val)

    def calibrate_rc(self, rcin):
        print("Please center your receiver sticks")
        self.led.setColor('Cyan')
        for x in range(0,100):
            self.set_throttle(0, self.th_pwm)
            self.set_throttle(0, self.st_pwm)
            time.sleep(0.03)
        
        print("Calibrating RC Input...")
        self.led.setColor('Magenta')
        yaw = 0
        throttle = 0
        roll = 0
        
        for x in range(0, 100):
            yaw += float(rcin.read(YAW_CHANNEL))
            throttle += float(rcin.read(THROTTLE_CHANNEL))
            roll += float(rcin.read(3))

            self.set_throttle(0, self.th_pwm)
            self.set_throttle(0, self.st_pwm)
            time.sleep(0.03)
        
        yaw /= 100.0
        throttle /= 100.0
        roll /= 100.0

        self.throttle_center = throttle
        self.yaw_center = yaw
        self.roll_center = roll
        
        print("Done")

if __name__ == "__main__":
    rover = Rover()
    rover.run()


