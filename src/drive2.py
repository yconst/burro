import sys
import time
import dbus
from navio import rcinput, pwm, leds, util

util.check_apm()

class Rover:

    def __init__(self):
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

        self.lf_pwm = pwm.PWM(0)
        self.lf_f = pwm.PWM(1)
        self.lf_r = pwm.PWM(2)
        self.lf_f.set_period(200)
        self.lf_r.set_period(200)
        self.lf_pwm.set_period(200)

        self.rf_pwm = pwm.PWM(5)
        self.rf_f = pwm.PWM(4)
        self.rf_r = pwm.PWM(3)
        self.rf_f.set_period(200)
        self.rf_r.set_period(200)
        self.rf_pwm.set_period(200)

        self.lr_pwm = pwm.PWM(6)
        self.lr_f = pwm.PWM(7)
        self.lr_r = pwm.PWM(8)
        self.lr_f.set_period(200)
        self.lr_r.set_period(200)
        self.lr_pwm.set_period(200)

        self.rr_pwm = pwm.PWM(11)
        self.rr_f = pwm.PWM(10)
        self.rr_r = pwm.PWM(9)
        self.rr_f.set_period(200)
        self.rr_r.set_period(200)
        self.rr_pwm.set_period(200)

        time.sleep(0.5)

        while True:
            self.led.setColor('Blue')

            if float(self.rcin.read(4)) > 1490:
                if (self.calibrated == False):

                    self.calibrate_rc(self.rcin)
                    self.calibrated = True

                self.led.setColor('Green')

                yaw = (float(self.rcin.read(0)) - self.yaw_center) / 500.0
                throttle = (float(self.rcin.read(2)) - self.throttle_center) / 500.0
                roll = (float(self.rcin.read(3)) - self.roll_center) / 500.0

                th_lf = min(1, max(-1, -throttle - yaw - roll))
                th_rf = min(1, max(-1, -throttle + yaw + roll))
                th_lr = min(1, max(-1, -throttle - yaw + roll))
                th_rr = min(1, max(-1, -throttle + yaw - roll))

                self.set_throttle(value=th_lf, pwm_in=self.lf_pwm, fore_in=self.lf_f, rear_in=self.lf_r)
                self.set_throttle(value=th_rf, pwm_in=self.rf_pwm, fore_in=self.rf_f, rear_in=self.rf_r)
                self.set_throttle(value=th_lr, pwm_in=self.lr_pwm, fore_in=self.lr_f, rear_in=self.lr_r)
                self.set_throttle(value=th_rr, pwm_in=self.rr_pwm, fore_in=self.rr_f, rear_in=self.rr_r)
            else:
                self.set_throttle(0, self.lf_pwm, self.lf_f, self.lf_r)
                self.set_throttle(0, self.rf_pwm, self.rf_f, self.rf_r)
                self.set_throttle(0, self.lr_pwm, self.lr_f, self.lr_r)
                self.set_throttle(0, self.rr_pwm, self.rr_f, self.rr_r)
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

    def set_throttle(self, value, pwm_in, fore_in, rear_in):
        if value > 0.05:
            fore_in.set_duty_cycle(5)
            rear_in.set_duty_cycle(0)
        elif value < -0.05:
            fore_in.set_duty_cycle(0)
            rear_in.set_duty_cycle(5)
        else:
            fore_in.set_duty_cycle(5)
            rear_in.set_duty_cycle(5)

        pwm_val = abs(value) * 5
        pwm_in.set_duty_cycle(pwm_val)

    def calibrate_rc(self, rcin):
        print("Please center your receiver sticks")
        self.led.setColor('Cyan')
        time.sleep(3)
        
        print("Calibrating RC Input...")
        self.led.setColor('Magenta')
        yaw = 0
        throttle = 0
        roll = 0
        
        for x in range(0, 100):
            yaw += float(rcin.read(0))
            throttle += float(rcin.read(2))
            roll += float(rcin.read(3))
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


