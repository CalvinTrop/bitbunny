#!/usr/bin/python3

# BitBunny: A cyberpunk pocket companion for general schenanegins and tomfoolery
# Shit code by Jeff Baars, project implemented 31DEC2024
# using AdaFruit's Blinka library
#
# Use this code for whatever you want, I'm not a cop... 

import math
import time
import subprocess
import board
import digitalio
import busio
import random
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_ina260
from adafruit_pm25.i2c import PM25_I2C

imagePath = "/home/bitbunny/bitbunny/images/"

# BitBunny specific definitions:
faceDetermined = "Bunz_Determined_64x64.bmp"
faceHappy = "Bunz_Happy_64x64.bmp"
faceSad = "Bunz_Determined_64x64.bmp"
facePuzzled = "Bunz_Puzzled_64x64.bmp"
faceSleepy = "Bunz_Sleepy_64x64.bmp"
faceDead = "Bunz_Dead_64x64.bmp"
faceIdleLeft = "Bunz_Idle_Left_64x64.bmp"
faceIdleRight = "Bunz_Idle_Right_64x64.bmp"

lastFace = faceDetermined # startup default face
face = lastFace # Look at me initializing my vars!
faceSpeedSetting = 2 # How long idle faces get held. Must be an int, default is 2
faceSpeed = faceSpeedSetting # I really need to make this loop a function
faceArray = [lastFace,faceIdleLeft,faceIdleRight] # Contains the array for idle animations

batt = 0
batt_remaining = 0
batt_delay = 1
min_voltage = 3.2
max_voltage = 4.05

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
# 2nd Display
oled2 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3D, reset=oled_reset)
# INA260 power monitoring PCB
ina260 = adafruit_ina260.INA260(i2c)

# For PM2.5 module, create library object, use 'slow' 100KHz frequency!
PM_i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(PM_i2c)

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

#---------------------------------------------------------------------------------------
# Mode Definitions
#---------------------------------------------------------------------------------------
def mode_stats(): # show hostname/stats

    # Draw a box to clear the image
    draw2.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
    cmd1 = "hostname"
    cmd2 = "hostname -I | cut -d' ' -f1"
    line1part1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
    line1part2 = subprocess.check_output(cmd2, shell=True).decode("utf-8")
    
    cmd1 = "top -bn1 | grep load | awk '{printf \"Load: %.2f\", $(NF-2)}'"
    cmd2 = "cat /sys/class/thermal/thermal_zone*/temp | awk 'length($0) ==5 {print substr($0,1,2) \".\" substr($0,3,1) \"°C\"}'"
    line2part1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
    line2part2 = subprocess.check_output(cmd2, shell=True).decode("utf-8")
    
    cmd = "free -m | awk 'NR==2{printf \"Memory: %.0f%%\", $3*100/$2}'"  
    line3 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %s", $5}\'' 
    line4 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = 'date +%T'
    line5 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write out all our stats on the 2nd canvas 
    draw2.text((x, top + 0),  line1part1, font=font, fill=255) # hostname
    draw2.text((x + 50, top + 0),  line1part2, font=font, fill=255) # IP address
    draw2.text((x, top + 12),  line2part1, font=font, fill=255) # load
    draw2.text((x + 74, top + 12), line2part2, font=font, fill=255) # sys temp
    draw2.text((x, top + 24), line3, font=font, fill=255) # Memory
    draw2.text((x, top + 36), line4, font=font, fill=255) # Disk
    draw2.text((x, top + 48), line5, font=font, fill=255) # local time

    # Display image. 
    oled2.image(image2)
    oled2.show()

def mode_airquality(): # Display air quality stats from PMSA003I module
    # Draw a box to clear the image
    draw2.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
    aqdata = pm25.read()
    pm10data = aqdata["pm10 standard"]
    pm25data = aqdata["pm25 standard"]
    pm100data = aqdata["pm100 standard"]

    pm03um = aqdata["particles 03um"]
    pm05um = aqdata["particles 05um"]
    pm10um = aqdata["particles 10um"]
    pm25um = aqdata["particles 25um"]
    pm50um = aqdata["particles 50um"]
    pm100um = aqdata["particles 100um"]

    draw2.text((x, top +0), "Particles > X per 0.1L air:", font=font, fill=255) # header
    draw2.text((x,top + 9), f"0.3um = {pm03um}", fill=255)
    draw2.text((x,top + 21), f"0.5um = {pm05um}", fill=255)
    draw2.text((x,top + 33), f"1.0um = {pm10um}", fill=255)
    draw2.text((x + 65,top + 9), f"2.5um = {pm25um}", fill=255)
    draw2.text((x + 65,top + 21), f"5.0um = {pm50um}", fill=255)
    draw2.text((x + 65,top + 33), f"10um = {pm100um}", fill=255)
    draw2.text((x,top + 45), f"AQI1.0 = {pm10data}", fill=255)
    draw2.text((x + 65,top + 45), f"AQI2.5 = {pm25data}", fill=255)

    if pm25data > 300:
        draw2.text((x,top + 54), "               -=DANGER=-", fill=255)
    else:
        if pm25data > 200:
            draw2.text((x,top + 54), "       -=Very Unhealthy=-", fill=255)
        else:
            if pm25data > 100:
                draw2.text((x,top + 54), "             -=Unhealthy=-", fill=255)
            else:
                if pm25data > 50:
                    draw2.text((x,top + 54), "              -=Moderate=-", fill=255)
                else:
                        draw2.text((x,top + 54), "                   -=Good=-", fill=255)

    # Display image. 
    oled2.image(image2)
    oled2.show()

#---------------------------------------------------------------------------------------

# Main loop:
while True:

    # Get battery voltage %
    batt_delay = batt_delay - 1
    if batt_delay == 0:
        batt = (ina260.voltage)
        batt_remaining = (batt - min_voltage) / (max_voltage-min_voltage) * 100
        batt_delay = 100
    
    # Draw a box to clear the image
    draw1.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Add stats screen overlay to left screen
    draw1.text((statsOffset, 0), statsTitle, font=font, fill=255, fontmode='1')
    draw1.line((65,12,128,12), fill=255, width=1)
    draw1.text((65,16), "H: 87", fill=255) # Health stat
    draw1.text((100,16), "F: 42", fill=255) # Food stat
    draw1.text((65,26), "A: 5", fill=255) # Attack stat
    draw1.text((100,26), "D: 7", fill=255) # Defense stat
    draw1.text((65,38), "Foraging", fill=255) # Current Activity
    draw1.text((65,52), f"B: {int(batt_remaining)}%", fill=255) # Battery
    draw1.text((100,52), "W: Y", fill=255) # Wifi Connected Y/N

    # Idle DoomBun face:
    if faceSpeed == 0:
        faceSpeed = faceSpeedSetting
        idleFace = random.choices(faceArray, weights=[8,2,2], k=1)
        if idleFace[0] != "lastFace":
            face = idleFace[0]
        else:
            face = lastFace
    else:
        faceSpeed = faceSpeed - 1

    # Draw the cutie lil' bun face
    image1.paste(Image.open(imagePath+face), (0,0))

    # Display image
    oled1.image(image1)
    oled1.show()

    # Test 2nd Screen
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = HEIGHT - padding
    # Move left to right keeping track of the current x position for drawing shapes
    x = 0
    
    # Draw 2nd Screen based on mode:
    mode_airquality()

    time.sleep(0.1)

