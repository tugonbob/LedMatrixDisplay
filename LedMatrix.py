#from rpi_ws281x import *

import neopixel
import board
import time

pixel_pin = board.D18
num_pixels = 256

strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.02, auto_write=False)

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

char_dict = {
    'A':
    [[0,0,1],
     [0,1,1],
     [1,0,1],
     [0,0,1],
     [0,0,1],
     [0,0,1]],
    'B':
    [[1,1,1,0],
     [1,0,0,1],
     [1,1,1,0],
     [1,0,0,1],
     [1,0,0,1],
     [1,1,1,0]],
    'C':
    [[0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0]],
    'null':
    [[0,0,0,0,1],
     [0,1,1,1,0],
     [0,1,0,1,0],
     [0,1,0,1,0],
     [0,1,1,1,0],
     [1,0,0,0,0]]
}

# colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,50,0)
CYAN = (0,255,255)
PURPLE = (80,0,255)
PINK = (255,0,100)

cursorx = 1 # global variable
cursory = 1 # global variable
COLOR = RED # global variable

# get rid of this commented code after finishing print_char and print_str
"""
# O
# O
# O
# O
# O
# OOOO

def L():
    global cursorx
    x, y = (cursorx, cursory)

    for y in range(y, y+6):
        strip[indexOf(x,y)] = COLOR
    for x in range(x, x+4):
        strip[indexOf(x, y)] = COLOR

    cursorx = cursorx + 5





# OOO
#  O
#  O
#  O
#  O
# OOO

def I():
    global cursorx
    x, y = (cursorx, cursory)

    for x in range(x, x+3):
        strip[indexOf(x,y)] = COLOR
    x = x-1
    for y in range(y, y+6):
        strip[indexOf(x,y)] = COLOR
    x = x-1
    for x in range(x,x+3):
        strip[indexOf(x,y)] = COLOR

    cursorx = cursorx + 4





# O   O
# O   O
# O   O
# O   O
#  O O
#   O

def V():
    global cursorx
    x,y = (cursorx, cursory)


    for y in range(y, y+4):
        strip[indexOf(x,y)] = COLOR
    x += 1
    y += 1
    strip[indexOf(x,y)] = COLOR
    strip[indexOf(x+2,y)] = COLOR
    x += 1
    y += 1
    strip[indexOf(x,y)] = COLOR
    x += 2
    y -= 1
    for y in range(y-4, y):
        strip[ indexOf(x,y) ] = COLOR

    cursorx += 6




# OOOO
# O
# OOO
# O
# O
# OOOO

def E():
    global cursorx
    x,y = (cursorx, cursory)

    for x in range(x, x+4):
        strip[ indexOf(x,y) ] = COLOR
    x,y = (cursorx, cursory)
    for y in range(y, y+6):
        strip[ indexOf(x,y) ] = COLOR
    for x in range(x, x+4):
        strip[ indexOf(x,y) ] = COLOR
    y -= 3
    for x in range(x-3, x):
        strip[ indexOf(x,y) ] = COLOR

    cursorx += 5




#      O
#   OOO
#  O OO
#  OO O
#  OOO
# O
def nullChar():
    global cursorx
    x,y = (cursorx, cursory)

    x += 5
    strip[ indexOf(x,y) ] = COLOR
    y += 1
    for x in range(x-3, x):
        strip[ indexOf(x,y) ] = COLOR
    y += 1
    strip[ indexOf(x,y) ] = COLOR
    strip[ indexOf(x-1,y) ] = COLOR
    strip[ indexOf(x-3,y) ] = COLOR
    y += 1
    strip[ indexOf(x,y) ] = COLOR
    strip[ indexOf(x-2,y) ] = COLOR
    strip[ indexOf(x-3,y) ] = COLOR
    y += 1
    for x in range(x-3, x):
        strip[ indexOf(x,y) ] = COLOR
    y += 1
    strip[ indexOf(x-3,y) ] = COLOR





# converts a ledstrip index to a coord
def coordOf(pos):
    x = int(pos // 8)
    if(x % 2 == 0):
        y = int(pos % 8)
    else:
        y = int(8 - (pos % 8))
    return (x,y)

# converts a coord to a ledstrip index
def indexOf(x,y):
    if(x % 2 == 0):
        return int((x * 8) + y)
    else:
        return int((x*8) + (7-y))

#print str with color by calling individual letter function
def print(str, color):
    global COLOR
    COLOR = color

    arr = list(str)

    for i in range(len(str)):
        if   arr[i] == 'L':
            L()
        elif arr[i] == 'I':
            I()
        elif arr[i] == 'V':
            V()
        elif arr[i] == 'E':
            E()
        else:
            nullChar()
"""

# im gonna comment this out until print_char and print_str is finished because they would change these functions a lot after they work
"""
#color wheel
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
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

#print str, scrolling through colors
def rainbowPrint(str):
    global cursorx
    global cursory
    while True:
        for color in range(1, 255):
            cursorx, cursory = (1,1)
            print(str, wheel(color))
            strip.show()

#main
rainbowPrint("LIVE")
#strip[ indexOf(cursorx, cursory) ] = BLUE #just to keep track of where the cursor is
#strip.show()
"""

# prints a single character at current current cursor position
def print_char(char):
    # get current cursor position
    # print relevent matrix in the dictionary if you have space for it (check how wide character is)

# print str with color by calling individual letter function
def print_str(str, color):
    global COLOR
    COLOR = color
    for char in str:
        if(char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            print_char(char)
        else:
            print_char(null)
        # move cursor to start of next character position (so column += 2 and row = 1) if it exists and you didnt run out of space on strip
    # reset cursor back first pixel after printing every character in string

def main():
    print("LIVx", GREEN)
    # this next line shouldnt be important because after a print statement, cursor should be set back to the first pixel
    strip[ indexOf(cursorx, cursory) ] = BLUE # just to keep track of where the cursor is
    strip.show()

if(__name__ == "__main__"):
    main()
