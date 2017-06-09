Burro is software for small-scale self-driving cars. It borrows ideas and code from [Donkey](http://donkeycar.com).


### Requirements

#### Hardware

- 1/10 or 1/16 RC car with PWM connections for throttle and steering
- Raspberry Pi 2 or 3
- [NAVIO2](https://emlid.com/navio/) HAT
- Either a Logitech F710 Gamepad or a PPM or SBUS-compatible RC receiver

#### Software

- Latest EMLID image installed and running on an SD card. [Here are the instructions](https://docs.emlid.com/navio2/common/ardupilot/configuring-raspberry-pi/). It is also advised that you [expand your filesystem](http://elinux.org/RPi_raspi-config#expand_rootfs_-_Expand_root_partition_to_fill_SD_card).


### Installation

Burro includes an installation script that handles installing necessary libraries, setting up the Python virtualenv and configuring submodules. To download and run:

    wget https://raw.githubusercontent.com/yconst/burro/master/install-burro.sh
    chmod +x install-burro.sh
    ./install-burro.sh


### Running

Connect up a Logitech F710 gamepad to the RPi USB port or a RC receiver to the NAVIO2 receiver pins.
`cd` where your `install-burro.sh` script that you downloaded earlier is, and:

    cd burro/burro
    ./start.sh

Visit `http://navio.local` to bring up the web interface. Choose your driving method (by default it is either gamepad or RC). Choose if you want to save images while moving (for training models).


### Configuring

All configuration options reside in `burro/src/config.py`.

By default Burro outputs throttle on channel 2 of the NAVIO2 rail, and steering on channel 0. These are channel 3 and one correspondingly, as marked on the NAVIO2 board.  You may wish to change this depending on your config.

Depending on your vehicle servo and motor, you may wish/need to calibrate the PWM output ranges, as well as the steering angle and camera horizontal FOV. The last two are currently not important but may become in the future.

RC Input channels are as follows: 0 - Yaw (i.e. steering), 2 - Throttle, 4 - Arm. Yaw and throttle are configurable via `config.py`, but Arm is hardwired to ch. 4 (TODO: make it configurable). Each time the RC controller is armed, a neutral point calibration is performed. Thus, you only need to make sure that your sticks are center before arming the car.

You may also wish to configure the throttle threshold value above which images are recorded.


### License

MIT, like [Donkey](http://donkeycar.com).
