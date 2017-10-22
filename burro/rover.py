import sys
import time


class Rover(object):
    '''
    Rover class
    '''

    def __init__(self):
        self.manual_pilots = []
        self.auto_pilots = []
        self.auto_pilot_index = -1
        self.f_time = 0.
        self.pilot_yaw = 0.
        self.pilot_throttle = 0.
        self.record = False

    def run(self):
        self.indicator.set_state('warmup')
        time.sleep(0.5)
        self.vision_sensor.start()
        time.sleep(0.5)
        self.remote.start()
        self.indicator.set_state('ready')
        time.sleep(0.5)

        while True:
            start_time = time.time()
            self.step()
            stop_time = time.time()
            self.f_time = stop_time - start_time
            time.sleep(max(0.005, 0.05 - self.f_time))

    def step(self):
        final_angle = 0
        final_throttle = 0
        for pilot in self.manual_pilots:
            pilot_angle, pilot_throttle = pilot.decide(
                self.vision_sensor.frame)
            final_angle += pilot_angle
            final_throttle += pilot_throttle

        if self.auto_pilot_index > -1:
            pilot = self.auto_pilots[self.auto_pilot_index];
            pilot_angle, pilot_throttle = pilot.decide(
                self.vision_sensor.frame)
            final_angle += pilot_angle
            final_throttle += pilot_throttle

        self.mixer.update(final_throttle, final_angle)

        self.pilot_angle = final_angle
        self.pilot_throttle = final_throttle

        if self.record:
            self.recorder.record_frame(
                self.vision_sensor.image_buffer(),
                final_angle, final_throttle)

        if self.recorder.is_recording:
            self.indicator.set_state('recording')
        elif self.record:
            self.indicator.set_state('standby')
        else:
            self.indicator.set_state('ready')

    def pilot(self):
        if self.auto_pilot_index >= 0:
            return self.auto_pilots[self.auto_pilot_index]
        return None

    def list_auto_pilot_names(self):
        return [p.pname() for p in self.auto_pilots]
