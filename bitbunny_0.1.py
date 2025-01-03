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
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# BitBunny specific definitions:
faceDetermined = "images/Bunz_Determined_128x64.bmp"
faceHappy = "images/Bunz_Happy_128x64.bmp"
faceSad = "images/Bunz_Determined_128x64.bmp"
facePuzzled = "images/Bunz_Puzzled_128x64.bmp"
faceSleepy = "images/Bunz_Sleepy_128x64.bmp"
faceDead = "images/Bunz_Dead_128x64.bmp"

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

# Draw Some Test Text
#text = "Hello World!"
#bbox = font.getbbox(text)
#(font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
#draw.text(
#    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#    text,
#    font=font,
#    fill=255,
#)

# Test loop:
while True:

    # Draw bunnyface splash screen
    image1 = Image.open(faceDetermined)

    # Display image
    oled1.image(image1)
    oled1.show()

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

    # Write four lines of text. 
    draw2.text((x, top + 0),  part1, font=font, fill=255) 
    draw2.text((x + 50, top + 0),  part2, font=font, fill=255) 
    draw2.text((x, top + 12),  line2, font=font, fill=255) 
    draw2.text((x, top + 24), line3, font=font, fill=255) 
    draw2.text((x, top + 36), line4, font=font, fill=255)

    # Display image. 
    oled2.image(image2)
    oled2.show()  

    time.sleep(1)

    # Cycle through faces as a test
    image1 = Image.open(faceHappy)
    oled1.image(image1)
    oled1.show()
    time.sleep(1)

    image1 = Image.open(faceSad)
    oled1.image(image1)
    oled1.show()
    time.sleep(1)

    image1 = Image.open(facePuzzled)
    oled1.image(image1)
    oled1.show()
    time.sleep(1)

    image1 = Image.open(faceSleepy)
    oled1.image(image1)
    oled1.show()
    time.sleep(1)

    image1 = Image.open(faceDead)
    oled1.image(image1)
    oled1.show()
    time.sleep(1)

"""
#First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = HEIGHT - padding
#Move left to right keeping track of the current x position for drawing shapes.
x = 0

#show hostname/stats
while True:
    # Draw a box to clear the image
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
    
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

    # Write four lines of text. 
    draw.text((x, top + 0),  part1, font=font, fill=255) 
    draw.text((x + 50, top + 0),  part2, font=font, fill=255) 
    draw.text((x, top + 12),  line2, font=font, fill=255) 
    draw.text((x, top + 24), line3, font=font, fill=255) 
    draw.text((x, top + 36), line4, font=font, fill=255)

    # Display image. 
    oled.image(image)
    oled.show()
    time.sleep(0.1)
"""
