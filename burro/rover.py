import sys
import time

class Rover(object):
    '''
    Rover class
    '''

    def __init__(self):
        self.pilots = []
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
        pilot_angle, pilot_throttle = self.pilot.decide(
            self.vision_sensor.frame)

        self.mixer.update(pilot_throttle, pilot_angle)

        self.pilot_angle = pilot_angle
        self.pilot_throttle = pilot_throttle

        if self.record:
            self.recorder.record_frame(
                self.vision_sensor.image_buffer(), 
                pilot_angle, pilot_throttle)

        if self.recorder.is_recording:
            self.indicator.set_state('recording')
        elif self.record:
            self.indicator.set_state('standby')
        else:
            self.indicator.set_state('ready')
        

    def selected_pilot_index(self):
        return self.pilots.index(self.pilot)

    def set_pilot(self, pilot):
        self.pilot = self.pilots[pilot]

    def list_pilot_names(self):
        return [p.pname() for p in self.pilots]
