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
        raise NotImplementedError('Not Implemented')
        
    def toLocation(self):
        for key, length in self.instructions:
            if key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)
    def temp(self):
        img = pyautogui.screenshot()
        gry = img.convert('L')
        bw = gry.point(lambda x: 255 if x<128 else 0, '1')
        bw.show()
    def isShiny(self):
        """ horde of 5 by default """
        text = ''
        img = pyautogui.screenshot()
        gry = img.convert('L')
        bw = gry.point(lambda x: 255 if x<128 else 0, '1')
        poke1 = bw.crop((600, 110, 860, 125))
        text += pytesseract.image_to_string(poke1)[:-1]
        poke2 = bw.crop((860, 110, 1120, 125))
        text += pytesseract.image_to_string(poke2)[:-1]
        poke3 = bw.crop((1120, 110, 1380, 125))
        text += pytesseract.image_to_string(poke3)[:-1]
        poke4 = bw.crop((600, 150, 860, 165))
        text += pytesseract.image_to_string(poke4)[:-1]
        poke5 = bw.crop((1120, 150, 1380, 165))
        text += pytesseract.image_to_string(poke5)[:-1]
        print(text)
        return 'shiny' in text.lower()
            
    def unwantedEncounter(self):
        self.holdKey('right', 0.5)
        pydirectinput.press('x')
        time.sleep(1.5)
        
    def stall(self):
        length = 0
        while True:
            pydirectinput.press('left')
            time.sleep(60)
            pydirectinput.press('right')
            time.sleep(60)
            length = length + 120
            print(length / 60)
    
    def checkScreen(self):
        time.sleep(0.1)
        if not pyautogui.pixelMatchesColor(900, 200, (28,35,40), tolerance = 20):
            time.sleep(11)
            pos = self.imgOnScreen('battleNeedle.png')
            while pos is None:
                time.sleep(1)
                pos = self.imgOnScreen('battleNeedle.png')
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
        time.sleep(10)
        if not self.isShiny():
            pos = self.imgOnScreen('battleNeedle.png')
            while pos is None:
                time.sleep(1)
                pos = self.imgOnScreen('battleNeedle.png')
            self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()

            
    def hunt(self):
        self.pokecenter()
        #route to shunting location
        self.toLocation()
        pydirectinput.press('c')
        self.checkScreen()
        for i in range(6):
            self.horde()
        pydirectinput.press('v')
        time.sleep(4)
        
class Hoenn(Base):
    def pokecenter(self):
        #healing at pokecenter
        self.holdKey('x', 3.7) 
        #leaving pokecenter
        self.holdKey('down', 1.3)
        time.sleep(1)
        #outside + bike
        pydirectinput.press('1')
        
class Sinnoh(Base):
    def pokecenter(self):
        #healing at pokecenter
        self.holdKey('x', 7.3) 
        #leaving pokecenter
        self.holdKey('down', 2)
        time.sleep(0.5)
        #outside + bike
        pydirectinput.press('1')
        
class Unova(Base):
    def pokecenter(self):
        #heal
        self.holdKey('x', 7)
        self.holdKey('down', 2.5)
        time.sleep(0.5)
        pydirectinput.press('1') #outside + bike