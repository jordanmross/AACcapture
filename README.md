AACcapture


Installation 
-----------------------------------------------

raspi-config

    Enable Camera:

       5 Interfacing Options -->
            P1 Camera -->
                Yes

    Change Memory Split:

        7 Advanced Options -->
            A3 Memory Split
                256


            
Install the dependencies:

sudo apt update

sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev

Install pip dependencies:

python -m pip install --upgrade --user pip setuptools
python -m pip install --upgrade --user Cython==0.29.10 pillow

Install Kivy to Python globally

You can install it like a normal python package with:

# to get the last release from pypi
python -m pip install --user kivy

Add to  ~/.kivy/config.ini

[input]
mouse = mouse
mtdev_%(name)s = probesysfs,provider=mtdev
hid_%(name)s = probesysfs,provider=hidinput



Python libraries required:

    Kivy
    Kivy-Garden
    picamera
    Pillow
    plyer
    wifi