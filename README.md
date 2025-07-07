# bitBunny - A DIY Cyberpunk Style Digital Companion
![bitBunny logo image](https://github.com/CalvinTrop/bitbunny/blob/ecb95f06eaddae4525e7298fd253b8b337d3cf19/CyberBun.png)
----------------------------------------------------
This project was inspired by several conversations/projects @ the [Cyberdeck Cafe Discord](https://discord.gg/EnC4padt7z)
Thanks all!

bitBunny is my take on something I could cobble together out of mostly spare parts around my bench and some plastic off
my 3d printers. The goal is specifically NOT to have a billion features planned right off the bat, but to start slow and
simple, learn some OLED libraries/pixel art techniques, and generally just have fun hacking around with something I
could throw in my pocket headed out for a slow day in the field or poke at on the couch in the evenings. Maybe someday
it'll have a few of the fun features I would like to make that would be *useful*, but until then all you'll find here is
a scrap tamagotchi wannabe. And that's just fine with me. :)

Also need to get out of the way here that I'm in dire need of updating my git/python skills, and I generally work in a
very messy way on the command line, so there may be a lot of questionable code practice and some cleanup work to do in
the repo. You'll live.

ToDo: Finish this README, I'm tired and need a drink.

### Hardware:
  - Raspberry Pi Zero W2 (or equivalent, this is the only hardware tested on so far)
  - 2xSSD1306 based 64x128px OLED displays (I used the Hosyond ones [here](https://www.amazon.com/dp/B0BFD4X6YV)
  - Basic soldering skills

### Software requirements (as far as I can recall... :/):
  - i2ctools
  - python3-full
  - python3-smbus
  - python3-setuptools
  - pip
  - [pillow](https://pillow.readthedocs.io/en/stable/)
  - Adafruit-circuitpython-ssd1306 lib
  - Adafruit-ina-260 lib
  - Adafruit-Blinka lib

### Pinouts:
  - OLED Displays:
      - Connect all headers 1:1 on both displays to each other
      - GND to Pin 6
      - VCC to Pin 1 (Use the 3.3V from the RPi to drive the displays, it's less for them to manage)
      - SDA to Pin 3
      - SCL to Pin 5

The service related files and .env are here as backups and because I'm very lazy.

Random WIP photos:

![Circuits and Stuff](https://i.ibb.co/ngcHpcN/bitbunny-WIP-3-JAN25.png)
![WIP Housing while I test](https://i.ibb.co/Ldzm3pR0/bbWIP.jpg)
