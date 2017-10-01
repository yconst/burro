from threading import Thread
import time

class BaseSensor(object):

    def start(self):
        '''
        Start receiving values from the sensor
        '''
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        time.sleep(1)
        return self

    def update(self):
        '''
        Performs sensor update steps. This is called
        in a separate thread
        '''
        pass
