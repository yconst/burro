#!/bin/sh -

echo "\nBurro Trainer Installer\n"

echo "\nFor security and compatibility reasons this installer will not install any system-wide packages.\n"
echo "\nIf you do not yet have your preferred Tensorflow version, you will have to install it yourself.\n"

sudo apt-get install realpath

echo "\nBurro Trainer Installer: Creating environment\n"
pip install virtualenv
virtualenv --system-site-packages burro-trainer
cd burro-trainer

echo "\nBurro Trainer Installer: Preparing Burro\n"
git clone https://github.com/yconst/burro
cd burro
git checkout training
../bin/pip install -r requirements-trainer.txt

echo "\nBurro Trainer Installer: Done.\n"
