#!/usr/bin/python3

# BitBunny: A cyberpunk pocket companion for general schenanegins and tomfoolery
# Shit code by Jeff Baars, project implemented 31DEC2024
# using AdaFruit's Blinka library
#
# Use this code for whatever you want, I'm not a cop...
#
# v0.3 - Refactoring face variable to change dynamically
#      - Added some random idle animations to test, ala DoomGuy
#      - Added current status area to stats screen 

import math
import time
import subprocess
import board
import digitalio
import random
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

imagePath = "/home/bitbunny/bitbunny/images/"

# BitBunny specific definitions:
faceDetermined = imagePath+"Bunz_Determined_64x64.bmp"
faceHappy = imagePath+"Bunz_Happy_64x64.bmp"
faceSad = imagePath+"Bunz_Determined_64x64.bmp"
facePuzzled = imagePath+"Bunz_Puzzled_64x64.bmp"
faceSleepy = imagePath+"Bunz_Sleepy_64x64.bmp"
faceDead = imagePath+"Bunz_Dead_64x64.bmp"
faceIdleLeft = imagePath+"Bunz_Idle_Left_64x64.bmp"
faceIdleRight = imagePath+"Bunz_Idle_Right_64x64.bmp"

face = faceDetermined # startup default face

# Random face code for funzies
faceArray = [faceDetermined,faceIdleLeft,faceIdleRight,facePuzzled,faceSleepy,faceDead,faceHappy,faceSad]

statsOffset = 75 #text offset to keep his lil face clear of text
statsTitle = "-=Stats=-"

# Define the Reset Pin
oled_reset = None

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Use for I2C.
i2c = board.I2C()  # uses board.SCL and board.SDA
oled1 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
#2nd Display
oled2 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3D, reset=oled_reset)

# Clear display
oled1.fill(0)
oled1.show()
# Clear display2
oled2.fill(0)
oled2.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image1 = Image.new("1", (oled1.width, oled1.height))
image2 = Image.new("1", (oled2.width, oled2.height))
# Get drawing object to draw on image.
draw1 = ImageDraw.Draw(image1)
draw2 = ImageDraw.Draw(image2)

# Load default font.
font = ImageFont.load_default()

# Test loop:
while True:

    # Draw bunnyface splash screen
    currentFace = Image.open(face)
    image1.paste(currentFace, (0,0))

    # Add stats screen overlay to left screen
    draw1.text((statsOffset, 0), statsTitle, font=font, fill=255, fontmode='1')
    draw1.line((65,12,128,12), fill=255, width=1)
    draw1.text((65,16), "H: 87", fill=255) # Health stat
    draw1.text((100,16), "F: 42", fill=255) # Food stat
    draw1.text((65,26), "A: 5", fill=255) # Attack stat
    draw1.text((100,26), "D: 7", fill=255) # Defense stat
    draw1.text((65,38), "Foraging", fill=255) # Current Activity
    draw1.text((65,52), "B:100", fill=255) # Battery
    draw1.text((100,52), "W: Y", fill=255) # Wifi Connected Y/N

    # Display image
    oled1.image(image1)
    oled1.show()

    # Random face cycle for testing:
    # face = faceArray[random.randint(0,7)]

    # Idle DoomBun face:
    faceArray = [faceDetermined,faceIdleLeft,faceIdleRight]
    idleFace = random.choices(faceArray, weights=[8,2,2], k=1)
    face = idleFace[0]

    # Test 2nd Screen
    #First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = HEIGHT - padding
    #Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    #show hostname/stats
    
    # Draw a box to clear the image
    draw2.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
    cmd1 = "hostname"
    cmd2 = "hostname -I | cut -d' ' -f1"
    part1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
    part2 = subprocess.check_output(cmd2, shell=True).decode("utf-8")
    
    cmd = "top -bn1 | grep load | awk '{printf \"Load: %.2f\", $(NF-2)}'" 
    line2 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = "free -m | awk 'NR==2{printf \"Memory: %.0f%%\", $3*100/$2}'"  
    line3 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %s", $5}\'' 
    line4 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = 'date +%T'
    line5 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text. 
    draw2.text((x, top + 0),  part1, font=font, fill=255) 
    draw2.text((x + 50, top + 0),  part2, font=font, fill=255) 
    draw2.text((x, top + 12),  line2, font=font, fill=255) 
    draw2.text((x, top + 24), line3, font=font, fill=255) 
    draw2.text((x, top + 36), line4, font=font, fill=255)
    draw2.text((x, top + 48), line5, font=font, fill=255)

    # Display image. 
    oled2.image(image2)
    oled2.show()  

    time.sleep(1)

