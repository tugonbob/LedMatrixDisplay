#from rpi_ws281x import *

import neopixel
import board
import time

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


#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,50,0)
CYAN = (0,255,255)
PURPLE = (80,0,255)
PINK = (255,0,100)

cursorx = 1 #global variable
cursory = 1 #global variable
COLOR = RED #global variable

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
        

    

#main
print("LIVx", GREEN)
strip[ indexOf(cursorx, cursory) ] = BLUE #just to keep track of where the cursor is
strip.show()

