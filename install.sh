#!/bin/sh -

sudo apt-get update
sudo apt-get install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
  libwebp-dev tcl8.5-dev tk8.5-dev python-tk
sudo apt-get install python-numpy python-scipy

sudo pip install virtualenv
virtualenv --system-site-packages burro
cd burro
git clone ...
