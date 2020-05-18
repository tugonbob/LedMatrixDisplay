'''
Code for for an LED matrix

# 32 x 8 led matrix. Works like a snaking led strip
# index of led strip
# 0 15 16 31 32 47 48 63 64 79 80 95 96  111 112 127 128 143 144 159 160 175 176 191 192 207 208 223 224 239 240 255
# 1 14 17 30  v  ^  v  ^  v  ^  v  ^  v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^    v   ^   v   ^
# 2 13 18 29
# 3 12 19 28
# 4 11 20 27
# 5 10 21 26
# 6 9  22 25
# 7 8  23 24 39 40 55 56 71 72 87 88 103 104 119 120 135 136 151 152 167 168 183 184 199 200 215 216 231 232 247 248
'''

#from rpi_ws281x import *

import neopixel
import board
import time
from characterDictionary import char_dict

pixel_pin = board.D18
num_pixels = 256

strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = .02, auto_write = False)

# colors
OFF = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,50,0)
CYAN = (0,255,255)
PURPLE = (80,0,255)
PINK = (255,0,100)

#global variables
cursorx = 0
cursory = 1
COLOR = RED

#constants
MATRIX_HEIGHT = 8
MATRIX_LENGTH = 32
LEFT_ALIGN = "LEFT"
CENTER_ALIGN = "CENTER"
CHAR_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890:'

# converts a ledstrip index to a coord
def coord_of(pos):
    x = int(pos // 8)
    if(x % 2 == 0):
        y = int(pos % 8)
    else:
        y = int(8 - (pos % 8))
    return(x,y)

# converts a coord to a ledstrip index
def index_of(x, y):
    if(x % 2 == 0):
        return int((x * 8) + y)
    else:
        return int((x * 8) + (7 - y))

# counts how many pixels there are of a length of the string
def pixel_length(str):
    total_length = 0

    for char in str:
        if char in CHAR_LIST:
            char_length = len(char_dict[char][0])
            total_length += char_length + 1
    return total_length - 1

# color wheel
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if(pos < 0 or pos > 255):
        r = g = b = 0
    elif(pos < 85):
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif(pos < 170):
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

# print a single character
def print_char(char):
    global cursorx

    char_height = len(char_dict[char])
    char_length = len(char_dict[char][0])

    for i in range(0, char_height): # loop y
        for j in range(0, char_length): # loop x
            if(cursorx + j < MATRIX_LENGTH and cursorx + j >= 0): # check x bounds
                if(cursory + i < MATRIX_HEIGHT and cursory + i >= 0): # check y bounds
                    if(char_dict[char][i][j] == 1):
                        strip[index_of(cursorx + j,cursory + i)] = COLOR
                    else:
                        strip[index_of(cursorx + j, cursory + i)] = OFF # erase led's that are ON from previous print
    cursorx = cursorx + char_length #move cursorx

# print str at a specific x and y
def print_str_loc(str, color = None, x, y = None):
    global cursorx, cursory
    cursorx = x
    if(y is not None):
        cursory = y

    if(color is not None):
        global COLOR
        COLOR = color

    for char in str:
        if(char in CHAR_LIST):
            print_char(char)
        else:
            print_char('null')
    strip.show()

# print a string using given alignment
def print_str(str, color = None, align = None):
    if(align == LEFT_ALIGN):
        # change cursorx to reflect alignment
        x = 0
        print_str_loc(str, color, x)
    else:
        # use CENTER_ALIGN
        pixel_len = pixel_length(str)
        x = int((MATRIX_LENGTH - pixel_len) / 2) # find equal distance between edges and str
        print_str_loc(str, color, x)

# print str, scrolling through colors
def rainbow_print(str):
    global cursorx
    global cursory

    while True:
        for degree in range(1, 255):
            cursorx, cursory = (0,1)
            print_str(str, wheel(degree))

# scrolling print
# todo: loop the text
def marquee_print(str, color = None, speed = None):
    if(color is not None):
        global COLOR
        COLOR = color

    if(speed is None):
        speed = .04

    for x in range(32, 0 - pixel_length(str), -1):
        print_str_loc(str, COLOR, x, cursory)
        time.sleep(speed)

# Main method
if(__name__ == "__main__"):
    marquee_print("HELLO", None, .01)
    if(cursorx < MATRIX_LENGTH and cursorx > 0):
        strip[index_of(cursorx, cursory)] = BLUE
