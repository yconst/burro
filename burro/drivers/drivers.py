
class Driver:
    '''
    Base driver class
    '''
    pass


class NAVIO2PWM(Driver):
    ''' 
    NAVIO2 PWM controler. 
    '''
    def __init__(self, channel, frequency=50):
        from navio import pwm as navio_pwm
        from navio import util

        util.check_apm()

        self.pwm = navio_pwm.PWM(channel)
        self.pwm.initialize()
        self.channel = channel
        self.pwm.set_period(frequency)

    def update(self, value):
        '''
        Accepts an input [-1, 1] and applies it as
        a PWM with RC-style duty cycle [1, 2].
        '''
        assert(value <= 1 and -1 <= value)
        pwm_val = 1.5 + value * 0.5
        self.pwm.set_duty_cycle(pwm_val) 
