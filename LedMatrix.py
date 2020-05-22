'''
Code for for an LED matrix
32 x 8 led matrix. Works like a snaking led strip
index of led strip
0 15 16 31 32 47 48 63 64 79 80 95 96  111 112 127 128 143 144 159 160 175 176 191 192 207 208 223 224 239 240 255
1 14 17 30  v  ^  v  ^  v  ^  v  ^  v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^    v   ^   v   ^
2 13 18 29
3 12 19 28
4 11 20 27
5 10 21 26
6 9  22 25
7 8  23 24 39 40 55 56 71 72 87 88 103 104 119 120 135 136 151 152 167 168 183 184 199 200 215 216 231 232 247 248
'''

import neopixel
import board
import time
from characterDictionary import char_dict
import OpenWeatherAPI
import FinnhubAPI
#todo: time API

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
cursory = 0
COLOR = RED

#constants
MATRIX_HEIGHT = 8
MATRIX_LENGTH = 32
CHAR_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 ?!&.,()_:;% @#$^*+-=[]{}|\'\"/<>~'

####################
#  UTIL FUNCTIONS  #
####################

# converts a ledstrip index to a coord #not used
def coord_of(pos):
    x = int(pos // 8)
    if (x % 2 == 0):
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

    color_change_found = False
    for char in str:
        if (char == '`'): #check for color change symbolized by '`' followed by a char
            color_change_found = True
            continue #skip '`' char
        if (color_change_found == True):
            color_change_found = False
            continue # skip color char
        
        if(char in CHAR_LIST):
            char_length = len(char_dict[char][0])
            total_length += char_length
    return total_length - 1

#####################
#  COLOR FUNCTIONS  #
#####################

# color wheel #not used unless I fix rainbow_print()
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

#Detects color change in a str
def color_change(char):
    global COLOR
    if (char == 'b'):
        COLOR = BLUE
    elif (char == 'g'):
        COLOR = GREEN
    elif (char == 'y'):
        COLOR = YELLOW
    elif (char == 'o'):
        COLOR = ORANGE
    elif (char == 'p'):
        COLOR = PURPLE
    elif (char == 'c'):
        COLOR = CYAN
    else: #Default color
        COLOR = RED

#####################
#  PRINT FUNCTIONS  #
#####################

# print a single character
def print_char(char, color):
    global cursorx
    char_height = len(char_dict[char])
    char_length = len(char_dict[char][0])
    
    for i in range(0, char_height): # loop y
        for j in range(0, char_length): # loop x
            if(cursorx + j < MATRIX_LENGTH and cursorx + j >= 0): # check x bounds
                if(cursory + i < MATRIX_HEIGHT and cursory + i >= 0): # check y bounds
                    if(char_dict[char][i][j] == 1):
                        strip[index_of(cursorx + j,cursory + i)] = color
                    else:
                        strip[index_of(cursorx + j, cursory + i)] = OFF # erase led's that are ON from previous print
    cursorx = cursorx + char_length #move cursorx

# print str at a specific x and y
def print_str(str, x, y = None):
    global cursorx, cursory
    cursorx = x
    if(y is not None):
        cursory = y
    
    color_change_found = False #flag to remember if there is a '`' signifying color change in the next char
    for char in str:
        if(char == '`'): #skip '`'
            color_change_found = True
            continue
        if (color_change_found == True): #skip char after '`'
            color_change(char) #change color
            color_change_found = False
            continue

        if(char in CHAR_LIST): #if valid char
            print_char(char, COLOR)
        else: #print null
            print_char('null', COLOR)
    strip.show()

# print a string using given alignment
def align_print(str, align):
    if(align == "LEFT"):
        # change cursorx to reflect alignment
        x = 0
        print_str(str, x, 0)
    else:
        # use CENTER_ALIGN
        pixel_len = pixel_length(str)
        x = int((MATRIX_LENGTH - pixel_len) / 2) # find equal distance between edges and str
        print_str(str, x, 0)

""" broken function
# print str, scrolling through colors
def rainbow_print(str):
    global cursorx
    global cursory

    while True:
        for color in range(1, 255):
            align_print(str, wheel(color), CENTER)
"""

# scrolling print
def marquee_print(str, speed = None):
    if(speed is None):
        speed = .02
    for x in range(32, -1 - pixel_length(str), -1): #decrement x till chars are off matrix edge
        print_str(str, x, None)
        time.sleep(speed)

#turn off all leds
def clear_matrix():
    strip.fill(OFF)
    strip.show()




# Main method
if(__name__ == "__main__"):
    #todo: parallel processing to get stock info while other things are displaying 
    align_print( str(OpenWeatherAPI.get_temp("Houston")), "CENTER" )
    time.sleep(1)
    clear_matrix()
    
    marquee_print( str(OpenWeatherAPI.get_weather("Houston")) )
    time.sleep(1)
    
    marquee_print( str(FinnhubAPI.get_stock_info()) )
