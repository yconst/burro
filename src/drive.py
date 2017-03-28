import sys
import time
from navio import rcinput, pwm, util

util.check_apm()

rcin = rcinput.RCInput()

lf_pwm = pwm.PWM(0)
lf_f = pwm.PWM(1)
lf_r = pwm.PWM(2)
lf_f.set_period(200)
lf_r.set_period(200)
lf_pwm.set_period(200)

rf_pwm = pwm.PWM(5)
rf_f = pwm.PWM(4)
rf_r = pwm.PWM(3)
rf_f.set_period(200)
rf_r.set_period(200)
rf_pwm.set_period(200)

lr_pwm = pwm.PWM(6)
lr_f = pwm.PWM(7)
lr_r = pwm.PWM(8)
lr_f.set_period(200)
lr_r.set_period(200)
lr_pwm.set_period(200)

rr_pwm = pwm.PWM(11)
rr_f = pwm.PWM(10)
rr_r = pwm.PWM(9)
rr_f.set_period(200)
rr_r.set_period(200)
rr_pwm.set_period(200)

while (True):
    yaw = float(rcin.read(1))
    throttle = float(rcin.read(2))
    roll = float(rcin.read(3))

    if throttle > 1550:
        lf_f.set_duty_cycle(5)
        lf_r.set_duty_cycle(0)
        rf_f.set_duty_cycle(5)
        rf_r.set_duty_cycle(0)
        lr_f.set_duty_cycle(5)
        lr_r.set_duty_cycle(0)
        rr_f.set_duty_cycle(5)
        rr_r.set_duty_cycle(0)

    elif throttle < 1450:
        lf_f.set_duty_cycle(0)
        lf_r.set_duty_cycle(5)
        rf_f.set_duty_cycle(0)
        rf_r.set_duty_cycle(5)
        lr_f.set_duty_cycle(0)
        lr_r.set_duty_cycle(5)
        rr_f.set_duty_cycle(0)
        rr_r.set_duty_cycle(5)
    else:
        lf_f.set_duty_cycle(5)
        lf_r.set_duty_cycle(5)
        rf_f.set_duty_cycle(5)
        rf_r.set_duty_cycle(5)
        lr_f.set_duty_cycle(5)
        lr_r.set_duty_cycle(5)
        rr_f.set_duty_cycle(5)
        rr_r.set_duty_cycle(5)

    pwm_val = max(0, abs(throttle-1500)-50) * 0.01
    lf_pwm.set_duty_cycle(pwm_val)
    rf_pwm.set_duty_cycle(pwm_val)
    lr_pwm.set_duty_cycle(pwm_val)
    rr_pwm.set_duty_cycle(pwm_val)
    time.sleep(0.02)

