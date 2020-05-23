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
from EmojiDictionary import emoji_dict
import OpenWeatherAPI
import FinnhubAPI
import datetime


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

# converts a ledstrip index to a coord
def coord_of(pos):
    x = int(pos // 8)
    if (x % 2 == 0):
        y = int(pos % 8)
    else:
        y = int(8 - (pos % 8))
    return(x,y)

# converts a coord to a ledstrip index #function not used
def index_of(x, y):
    if(x % 2 == 0):
        return int((x * 8) + y)
    else:
        return int((x * 8) + (7 - y))

# counts how many pixels there are of a length of the string
def pixel_length(str):
    total_length = 0

    escape_found = False
    escape_string = ""
    for char in str:
        if (escape_found == False and char == '`'): #check for color change symbolized by opening '`', followed by a char, followed by closing '`'
            escape_found = True
            continue #skip opening '`' char
        if (escape_found == True and char != '`'):
            escape_string = escape_string + char
            continue #skip everything in between two '`'
        if (escape_found == True and char == '`'):
            escape_found = False
            total_length += get_escape_pixel_length(escape_string)
            escape_string = ""
            continue #skip closing '`'
        
        if(char in CHAR_LIST):
            char_length = len(char_dict[char][0])
            total_length += char_length
    return total_length - 1

#turn off all leds
def clear_matrix():
    strip.fill(OFF)
    strip.show()
    
#takes escape string and does the respective action
def handle_escape(str):
    global COLOR
    if (str == 'b'):
        COLOR = BLUE
    elif (str == 'g'):
        COLOR = GREEN
    elif (str == 'y'):
        COLOR = YELLOW
    elif (str == 'o'):
        COLOR = ORANGE
    elif (str == 'p'):
        COLOR = PURPLE
    elif (str == 'c'):
        COLOR = CYAN
    elif (str == 'r'):
        COLOR = RED
    elif (str == ':)'):
        emoji_print(':)')
        
def get_escape_pixel_length(str):
    if (str == ':)'):
        return len(emoji_dict[':)'][0])
    else:
        return 0

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

#####################
#  PRINT FUNCTIONS  #
#####################

# print a single character
def print_char(char, color):
    global cursorx
    char_height = len(char_dict[char])
    char_length = len(char_dict[char][0])
    
    for y in range(0, char_height): # loop y
        for x in range(0, char_length): # loop x
            if(cursorx + x < MATRIX_LENGTH and cursorx + x >= 0): # check x bounds
                if(cursory + y < MATRIX_HEIGHT and cursory + y >= 0): # check y bounds
                    if(char_dict[char][y][x] == 1):
                        strip[index_of(cursorx + x, cursory + y)] = color
                    else:
                        strip[index_of(cursorx + x, cursory + y)] = OFF # erase led's that are ON from previous print
    cursorx = cursorx + char_length #move cursorx

# print str at a specific x and y
def print_str(str, x, y):
    global cursorx, cursory
    cursorx = x
    cursory = y
    
    escape_found = False #flag to remember if there is a '`' signifying escape string between two '`'
    escape_string = "" #to build the string between '`'
    for char in str:
        if (escape_found == False and char == '`'): #skip opening '`'
            escape_found = True
            continue
        if (escape_found == True and char != '`'): #skip chars between '`'
            escape_string = escape_string + char #build escape_string
            continue
        if (escape_found == True and char == '`'):
            handle_escape(escape_string)
            escape_found = False
            escape_string = ""
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
    global cursory
    cursory = 1
    if(speed is None):
        speed = .01
    for x in range(32, -1 - pixel_length(str), -1): #decrement x till chars are off matrix edge
        print_str(str, x, 0)
        time.sleep(speed)

#display an emoji in emoji_dict
def emoji_print(str):
    global cursorx
    global cursory
    cursory = 0
    emoji_height = len(emoji_dict[str])
    emoji_length = len(emoji_dict[str][0])
    
    for y in range(0, emoji_height): #loop y
        for x in range(0, emoji_length): #loop x
            if(cursorx + x < MATRIX_LENGTH and cursorx + x >= 0): # check x bounds
                if(cursory + y < MATRIX_HEIGHT and cursory + y >= 0): # check y bounds
                    if (emoji_dict[str][y][x] == 'y'):
                        strip[index_of(cursorx + x, cursory + y)] = YELLOW
                    elif (emoji_dict[str][y][x] == 'r'):
                        strip[index_of(cursorx + x, cursory + y)] = RED
                    elif (emoji_dict[str][y][x] == 'p'):
                        strip[index_of(cursorx + x, cursory + y)] = PINK
                    elif (emoji_dict[str][y][x] == '0'):
                        strip[index_of(cursorx + x, cursory + y)] = OFF
    cursorx = cursorx + emoji_length #move cursorx
                    
    
    
    

#########################
#  TIME DATE FUNCTIONS  #
#########################

# HH:MM AM/PM
def display_time():
    clear_matrix()
    #store time info into easy to read variables
    now = datetime.datetime.today()
    if (now.hour > 12):
        hour = now.hour - 12
        AMPM = "PM"
    else:
        hour = now.hour
        AMPM = "AM"
    minute = now.minute
    second = now.second
        
    while True:
        #if else to space the hour, minute, AMPM correctly
        if (len(str(minute)) == 1): #if minute is 1 digit
            align_print("`r`" + str(hour) + ":0" + str(minute) + AMPM, "CENTER")
        else: #if minute is 2 digit
            align_print("`r`" + str(hour) + ":"+ str(minute) + AMPM, "CENTER")
        
        #move clock
        second = second + 1
        time.sleep(1)
        if (second == 60):
            second = 0
            minute = minute + 1

#MM.DD   no year, 1 pixel off from fitting
def display_date():
    clear_matrix()
    #store time info into easy to read variables
    now = datetime.datetime.today()
    year = str(now.year)[-2:] #last 2 digits of year
    month = str(now.month)
    day = str(now.day)
    
    align_print("`r`" + month + " / " + day, "CENTER")





# Main method
if(__name__ == "__main__"):
    #todo: parallel processing to get stock info while other things are displaying

    marquee_print( "`y`Mama is`r` the best!`:)`", .02) #works!
        
    #marquee_print( str(FinnhubAPI.get_stock_news()) )
    #marquee_print( str(FinnhubAPI.get_stock_info()) )
