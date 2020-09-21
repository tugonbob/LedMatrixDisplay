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
import sys
import bs4 as bs
import pickle
import requests
import random
import digitalio
import board
import adafruit_matrixkeypad

# LED matrix setup
pixel_pin = board.D18
num_pixels = 256
strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = 0.08, auto_write = False)

# keypad setup
cols = [digitalio.DigitalInOut(x) for x in (board.D9, board.D6, board.D5)]
rows = [digitalio.DigitalInOut(x) for x in (board.D13, board.D12, board.D11, board.D10)]
keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#'))
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

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
WHITE = (255,255,255)

#global variables
cursorx = 0
cursory = 0
COLOR = RED

#constants
MATRIX_HEIGHT = 8
MATRIX_LENGTH = 32
CHAR_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 ?!&.,()_:;% @#$^*+-=[]{}|\'\"/<>~'
EMOJI_LIST= ':)  :(  <3  XD  DX  ;)  ;(  "(  "D  ,:D   :P'


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
    elif (str == 'w'):
        COLOR = WHITE
    elif (str in EMOJI_LIST):
        emoji_print(str)
        
def get_escape_pixel_length(str):
    if (str in EMOJI_LIST):
        return len(emoji_dict[str][0])
    else:
        return 0
    

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
    emoji_height = len(emoji_dict[str][0])
    emoji_length = len(emoji_dict[str][0][0])
    
    #print(emoji_dict[str][0][0][0])
    clear_matrix()
    for frame in range(0, 3):
        for y in range(0, emoji_height): #loop y
            for x in range(0, emoji_length): #loop x
                if(cursorx + x < MATRIX_LENGTH and cursorx + x >= 0): # check x bounds
                    if(cursory + y < MATRIX_HEIGHT and cursory + y >= 0): # check y bounds
                        if (emoji_dict[str][frame][y][x] == 'y'):
                            strip[index_of(cursorx + x, cursory + y)] = YELLOW
                        elif (emoji_dict[str][frame][y][x] == 'r'):
                            strip[index_of(cursorx + x, cursory + y)] = RED
                        elif (emoji_dict[str][frame][y][x] == 'g'):
                            strip[index_of(cursorx + x, cursory + y)] = GREEN
                        elif (emoji_dict[str][frame][y][x] == 'b'):
                            strip[index_of(cursorx + x, cursory + y)] = BLUE
                        elif (emoji_dict[str][frame][y][x] == 'o'):
                            strip[index_of(cursorx + x, cursory + y)] = ORANGE
                        elif (emoji_dict[str][frame][y][x] == 'p'):
                            strip[index_of(cursorx + x, cursory + y)] = PINK
                        elif (emoji_dict[str][frame][y][x] == 'w'):
                            strip[index_of(cursorx + x, cursory + y)] = WHITE
                        elif (emoji_dict[str][frame][y][x] == '0'):
                            strip[index_of(cursorx + x, cursory + y)] = OFF
        strip.show()
        time.sleep(.5)
    cursorx = cursorx + emoji_length #move cursorx
                    
    
    
    

#########################
#  TIME DATE FUNCTIONS  #
#########################

# HH:MM AM/PM
def display_time():
    clear_matrix()
    #store time info into easy to read variables
    now = datetime.datetime.today()
    hour = now.hour
    minute = now.minute
    second = now.second
        
    print("{hour: " + str(hour) + ", minute: " + str(minute) + "}")
    print("displaying time...")
    #if else to space the hour, minute, AMPM correctly
    if (len(str(minute)) == 1): #if minute is 1 digit
        if (len(str(hour)) == 1):
            align_print("`c`0" + str(hour) + ":0" + str(minute), "CENTER")
        else:
            align_print("`c`" + str(hour) + ":0" + str(minute), "CENTER")
    else: #if minute is 2 digit
        if (len(str(hour)) == 1):
            align_print("`c`0" + str(hour) + ":" + str(minute), "CENTER")
        else:
            align_print("`c`" + str(hour) + ":" + str(minute), "CENTER")
        
        

#MM.DD   no year, 1 pixel off from fitting
def display_date():
    clear_matrix()
    #store time info into easy to read variables
    now = datetime.datetime.today()
    year = str(now.year)[-2:] #last 2 digits of year
    month = now.month
    day = str(now.day)
    
    if (month == 1):
        month = "JAN"
    elif (month == 2):
        month = "FEB"
    elif (month == 3):
        month = "MAR"
    elif (month == 4):
        month = "APR"
    elif (month == 5):
        month = "MAY"
    elif (month == 6):
        month = "JUN"
    elif (month == 7):
        month = "JUL"
    elif (month == 8):
        month = "AUG"
    elif (month == 9):
        month = "SEP"
    elif (month == 10):
        month = "OCT"
    elif (month == 11):
        month = "NOV"
    else:
        month = "DEC"
    
    print("{month: " + str(month) + ", day: " + str(day) + "}")
    print("displaying date...")
    align_print("`c`" + month + "  " + day, "CENTER")

        
def save_sp100_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P_100')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[0:len(ticker)-1]
        tickers.append(ticker)
        
    with open("sp100tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

def get_five_random_tickers():
    global unvisited_tickers
    
    ls = []
    temp_unvisited_tickers = unvisited_tickers.copy()
    while (len(ls) != 5):
        rand_index = random.randint(0,len(temp_unvisited_tickers)-1) #sp100 has 101 tickers
        ls.append(temp_unvisited_tickers[rand_index])
        temp_unvisited_tickers.remove(unvisited_tickers[rand_index])
        unvisited_tickers = temp_unvisited_tickers.copy()
    if (len(unvisited_tickers) < 5):
        unvisited_tickers = sp100.copy()
        
    return ls

def detect_keypad_press():
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
        if keys[0] == 1:
            clear_matrix()
            time.sleep(4)
        time.sleep(0.15)
    
    

# Main method
def main():
    templist = []
    x = 0
        
    while True:
        try:
            #turn off for sleeping hours
            now = datetime.datetime.today()
            hour = now.hour
            minute = now.minute
            while (hour < 7): #hour >= 22 or 
                clear_matrix()
                now = datetime.datetime.today()
                hour = now.hour
                print("waiting 15 minutes...  " + str(hour) + ":" + str(minute))
                time.sleep(100)
            
            #display time
            display_time()
            time.sleep(2)
            
            
            #display 5 tickers and their percent changes
            ls = get_five_random_tickers()
            tempstr = FinnhubAPI.get_stock_prices(ls)
            clear_matrix()
            marquee_print(tempstr)
            
            #display date
            display_date()
            time.sleep(2)
            
            #display 5 tickers and their percent changes
            ls = get_five_random_tickers()
            tempstr = FinnhubAPI.get_stock_prices(ls)
            clear_matrix()
            marquee_print(tempstr)
              
        except: #sometimes the wifi won't be stable, which sometimes makes the FinnhubAPI throw and error. This just reruns the code in the try
            clear_matrix()
            print("Some sort of error occured, rerunning")
            pass
    
#stock lists, used in get_five_random_tickers() function
dow = ['MMM', 'AXP', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'XOM', 'GS', 'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PFE', 'PG', 'RTX', 'TRV', 'UNH', 'VZ', 'V', 'WMT', 'WBA', 'DIS']
sp100 = save_sp100_tickers()
unvisited_tickers = sp100.copy()

clear_matrix()
main()
