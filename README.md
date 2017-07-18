Burro is a platform for small-scale self-driving cars. It borrows ideas and code from [Donkey](http://donkeycar.com).


### Requirements

#### Hardware

- 1/10 or 1/16 RC car with PWM connections for throttle and steering
- Raspberry Pi 2 or 3
- RaspiCam, Fisheye model (something like [this](http://www.ebay.com/itm/191723967593))
- [NAVIO2](https://emlid.com/navio/) HAT
- Either a Logitech F710 Gamepad or a PPM or SBUS-compatible RC receiver

#### Software

- Latest EMLID image installed and running on an SD card. [Here are the instructions](https://docs.emlid.com/navio2/common/ardupilot/configuring-raspberry-pi/). You will need to [expand your filesystem](http://elinux.org/RPi_raspi-config#expand_rootfs_-_Expand_root_partition_to_fill_SD_card).


### Installation

Burro includes an installation script that handles installing necessary libraries, setting up the Python virtualenv and configuring submodules. To download and run:

    wget https://raw.githubusercontent.com/yconst/burro/master/install-burro.sh
    chmod +x install-burro.sh
    ./install-burro.sh

If you would like you can take a look [here](https://github.com/yconst/burro/wiki/Installed-Packages-and-Libraries) to find out more about the libraries and packages that the script is installing.

### Running

Connect up a Logitech F710 gamepad to the RPi USB port or a RC receiver to the NAVIO2 receiver pins.
`cd` where your `install-burro.sh` script that you downloaded earlier is, and:

    cd burro/burro
    ./start.sh

Visit `http://navio.local` to bring up the web interface. Choose your driving method (by default it is either gamepad or RC). Choose if you want to save images while moving (for training models); the background color of the steering indicator will change to green to indicate standby, red once recording.


### Next Steps

Please take a look at the [Burro Wiki](https://github.com/yconst/burro/wiki) for more information, including [help on configuring](https://github.com/yconst/burro/wiki/Configuring).


### Contributing

Contributions via merge requests or opening issues are always very welcome. Please also take a look at the [Code of Conduct](https://github.com/yconst/burro/blob/master/CODE_OF_CONDUCT.md)


### License

MIT
