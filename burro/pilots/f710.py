'''

f710.py

A pilot using the F710 gamepad

'''

import os
import math
import random
import time
import logging

from threading import Thread

from operator import itemgetter
from datetime import datetime
from pilots import BasePilot

import methods
from config import config

from pilot import BasePilot

# Note: The code below could be very easily adapted to a
# F310 gamepad. See:
# https://github.com/sdickreuter/python-gamepad/blob/master/pygamepad/gamepad.py


class F710(BasePilot):
    '''
    A pilot using the F710 gamepad
    '''
    def __init__(self, **kwargs):
        self.gamepad = Gamepad()
        self.gamepad._read_gamepad()
        self.thread = Thread(target=self.loop_values)
        self.thread.daemon = True
        self.thread.start()
        super(F710, self).__init__(**kwargs)
        self.throttle = 0.0
        self.yaw = 0.0

    def decide(self, img_arr):
        st = self.gamepad._state
        direction = int(st[2])
        if direction == 1: # forward
                self.throttle = -0.095 - st[4]/255.
        elif direction == 2: # reverse
                self.throttle = 0.095 + st[4]/255.
        else:
            self.throttle = 0
        self.throttle -= (float(st[12]) - 128.0) / 128.0
        self.yaw = (float(st[10]) - 128.0) / 128.0

        return methods.yaw_to_angle(self.yaw), self.throttle

    def loop_values(self):
        while True:
            self.gamepad._read_gamepad()

    def pname(self):
        return "F710 Gamepad"


import usb
import struct

USB_VENDOR = 0x046d
USB_PRODUCT = 0xc21f
default_state = (0, 20, 0, 0, 0, 0, 123, 251, 128,
                 0, 128, 0, 128, 0, 0, 0, 0, 0, 0, 0)


class Gamepad(object):

    def __init__(self):
        self.is_initialized = False
        d = None
        busses = usb.busses()
        for bus in busses:
            devs = bus.devices
            for dev in devs:
                if dev.idVendor == 0x046d and dev.idProduct == 0xc21f:
                    d = dev
        if d is not None:
            self._dev = d.open()
            try:
                self._dev.detachKernelDriver(0)
            except usb.core.USBError:
                logging.warning("Gamepad: Error detaching kernel driver (usually no problem)")
            except AttributeError:
                pass
            self._dev.setConfiguration(1)
            self._dev.claimInterface(0)

            # This value has to be send to the gamepad, or it won't start working
            # value was determined by sniffing the usb traffic with wireshark
            # getting other gamepads to work might be a simple as changing this
            self._dev.interruptWrite(
                0x02, struct.pack(
                    '<BBB', 0x01, 0x03, 0x04))
            self.changed = False
            self._state = default_state
            self._old_state = default_state
            self.is_initialized = True
            logging.info("Gamepad initialized")
        else:
            RuntimeError("Could not initialize Gamepad")

    def _getState(self):
        try:
            data = self._dev.interruptRead(0x81, 0x20, 2000)
            data = struct.unpack('<' + 'B' * 20, data)
            return data
        except usb.core.USBError as e:
            return None

    def _read_gamepad(self):
        self.changed = False
        state = self._getState()
        if state is not None:
            self._old_state = self._state
            self._state = state
            self.changed = True

    def X_was_released(self):
        if (self._state[3] != 64) & (self._old_state[3] == 64):
            return True
        return False

    def Y_was_released(self):
        if (self._state[3] != 128) & (self._old_state[3] == 128):
            return True
        return False

    def A_was_released(self):
        if (self._state[3] != 16) & (self._old_state[3] == 16):
            return True
        return False

    def B_was_released(self):
        if (self._state[3] != 32) & (self._old_state[3] == 32):
            return True
        return False

    def get_state(self):
        return self._state[:]

    def get_LB(self):
        return self._state[3] == 1

    def get_RB(self):
        return self._state[3] == 2

    def get_A(self):
        return self._state[3] == 16

    def get_B(self):
        return self._state[3] == 32

    def get_X(self):
        return self._state[3] == 64

    def get_Y(self):
        return self._state[3] == 128

    def get_analogR_x(self):
        return self._state[10]

    def get_analogR_y(self):
        return self._state[12]

    def get_analogL_x(self):
        return self._state[6]

    def get_analogL_y(self):
        return self._state[8]

    def get_dir_up(self):
        return self._state[2] in (1, 5, 9)

    def get_dir_down(self):
        return self._state[2] in (2, 6, 10)

    def get_dir_left(self):
        return self._state[2] in (4, 5, 6)

    def get_dir_up(self):
        return self._state[2] in (8, 9, 10)

    def changed(self):
        return self.changed

    def __del__(self):
        if self.is_initialized:
            self._dev.releaseInterface()
