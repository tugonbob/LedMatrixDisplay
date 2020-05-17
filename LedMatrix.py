#from rpi_ws281x import *

import neopixel
import board
import time
from characterDictionary import char_dict

pixel_pin = board.D18
num_pixels = 256

strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.02, auto_write=False)

#32 x 8 led matrix. Works like a snaking led strip

# index of led strip
# 0 15 16 31 32 47 48 63 64 79 80 95 96  111 112 127 128 143 144 159 160 175 176 191 192 207 208 223 224 239 240 255
# 1 14 17 30  v  ^  v  ^  v  ^  v  ^  v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^   v   ^    v   ^   v   ^
# 2 13 18 29 
# 3 12 19 28 
# 4 11 20 27
# 5 10 21 26
# 6 9  22 25
# 7 8  23 24 39 40 55 56 71 72 87 88 103 104 119 120 135 136 151 152 167 168 183 184 199 200 215 216 231 232 247 248
        

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

#colors
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

""" for me to copy paste
'':
    [[0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0]],
"""

    

# converts a ledstrip index to a coord
def coordOf(pos):
    x = int(pos // 8)
    if(isEven(x)):
        y = int(pos % 8)
    else:
        y = int(8 - (pos % 8))
    return (x,y)




# converts a coord to a ledstrip index
def indexOf(x,y):
    if(isEven(x)):
        return int((x * 8) + y)
    else:
        return int((x*8) + (7-y))
    
    
        
# checks if n is even
def isEven(n):
    if(n%2 == 0):
        return True
    else:
        return False

"""
#print str, scrolling through colors
def rainbowPrint(str):
    global cursorx
    global cursory
    while True:
        for color in range(1, 255):
            cursorx, cursory = (1,1)
            printStr(str, wheel(color))
            strip.show()
"""


def printChar(char):
    global cursorx
    
    charHeight = len( char_dict[char] )
    charLength = len( char_dict[char][0] )
    
    for i in range(0, charHeight):
        for j in range(0, charLength):
            if char_dict[char][i][j] == 1 and cursorx+j < MATRIX_LENGTH:
                strip[ indexOf(cursorx+j,cursory+i) ] = COLOR
                
    cursorx = cursorx + charLength + 1 #move cursorx

def printStr(str, color):
    global COLOR
    COLOR = color
    printStr(str)

def printStr(str):
    for char in str:
        if(char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '):
            printChar(char)
        else:
            printChar('null')
    



def main():
    printStr("HI SUNNY")
    if cursorx < MATRIX_LENGTH:
        strip[ indexOf(cursorx, cursory) ] = BLUE
    strip.show()

    
if(__name__ == "__main__"):
    main()

