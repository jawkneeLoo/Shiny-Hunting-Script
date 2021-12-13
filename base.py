import csv
import os
import pyautogui
import pydirectinput
import pytesseract
import time

class Base:
    def __init__(self, fileName):
        pytesseract.tesseract_cmd = r'C:\Users\liuru\anaconda3\Library\bin\tesseract.exe'
        
        script_dir = os.path.dirname(__file__)
        needle_path = os.path.join(
            script_dir, 
            'paths', 
            fileName
        )
        
        self.instructions = []
        with open(needle_path, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            for pair in reader:
                pair = pair[0].split(',')
                key = pair[0]
                length = float(pair[1])
                self.instructions.append((key, length))
        
    
    def holdKey(self, key, seconds = 1.0):
        pydirectinput.keyDown(key)
        time.sleep(seconds)
        pydirectinput.keyUp(key)
        
    def pokecenter(self):
        """ Unova pokecenter by default"""
        #heal
        self.holdKey('x', 7)
        self.holdKey('down', 2.5)
        time.sleep(0.5)
        pydirectinput.press('1') #outside + bike
        
    def toLocation(self):
        for key, length in self.instructions:
            if key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)
        
    def isShiny(self):
        """ horde of 5 by default """
        text = ''
        img = pyautogui.screenshot()
        poke1 = img.crop((510, 110, 800, 125))
        text += pytesseract.image_to_string(poke1)[:-1]
        poke2 = img.crop((800, 110, 1090, 125))
        text += pytesseract.image_to_string(poke2)[:-1]
        poke3 = img.crop((1090, 110, 1380, 125))
        text += pytesseract.image_to_string(poke3)[:-1]
        poke4 = img.crop((510, 150, 800, 165))
        text += pytesseract.image_to_string(poke4)[:-1]
        poke5 = img.crop((1090, 150, 1380, 165))
        text += pytesseract.image_to_string(poke5)[:-1]
        print(text)
        return 'shiny' in text.lower()
            
    def unwantedEncounter(self):
        self.holdKey('right', 0.5)
        pydirectinput.press('x')
        time.sleep(1.5)
        
    def stall(self):
        while True:
            pydirectinput.press('left')
            time.sleep(60)
            pydirectinput.press('right')
            time.sleep(60)
    
    def checkScreen(self):
        img = pyautogui.screenshot()
        px1 = img.getpixel((1020, 500))
        time.sleep(1)
        px2 = img.getpixel((1020, 500))
        if px1 != px2:
            time.sleep(20)
            if not self.isShiny():
                self.unwantedEncounter()
            else:
                print('Shiny detected!')
                self.stall()
    
    def imgOnScreen(self, fileName):
        script_dir = os.path.dirname(__file__)
        needle_path = os.path.join(
            script_dir, 
            'needles', 
            fileName
        )
        return pyautogui.locateOnScreen(needle_path)
    
    def horde(self):
        pydirectinput.press('c')
        time.sleep(11)
        if not self.isShiny():
            self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()
            
    def hunt(self):
        self.pokecenter()
        #route to shunting location
        self.toLocation()
        #check if in unwanted battle
        self.checkScreen()
        for i in range(6):
            self.horde()
        pydirectinput.press('v')
        time.sleep(4)