#!/bin/sh -

echo "\nBurro Installer: Installing necessary libraries\n"
sudo apt-get update
sudo apt-get install --assume-yes libtiff5-dev libjpeg-dev zlib1g-dev \
  libfreetype6-dev liblcms2-dev \
  libwebp-dev tcl8.5-dev tk8.5-dev python-tk
sudo apt-get install --assume-yes python-numpy python-scipy python-pillow \
  libhdf5-dev python-h5py
sudo apt-get install --assume-yes python-smbus i2c-tools

echo "\nBurro Installer: Creating environment\n"
sudo pip install virtualenv
virtualenv --system-site-packages burro
cd burro

echo "\nBurro Installer: Preparing Burro\n"
git clone https://github.com/yconst/burro
cd burro
../bin/pip install -r requirements.txt

echo "\nBurro Installer: Installing submodules\n"
echo "Burro Installer: (this can take some time..)\n"
git submodule update --init --recursive
../bin/pip install -r Navio2/Python/requirements.txt

echo "\nBurro Installer: Creating symlinks\n"
DIR="$( cd "$( dirname "$0" )" && pwd )"
ln -s $DIR/Navio2/Python/navio2 $DIR/burro/navio

echo "\nBurro Installer: Done. Run sudo start.sh to start Burro\n"
