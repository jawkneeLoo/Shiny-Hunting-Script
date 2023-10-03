import csv
import easyocr
import numpy as np
import os
import pyautogui
import pydirectinput
import time

class Base:
    """A class used to represent the base functions of PokeMMO grinding."""

    def __init__(self, fileName: str):
        # OCR reader
        self.reader = easyocr.Reader(['en'], detector=False)
        # file paths for instructions
        script_dir = os.path.dirname(__file__)
        needle_path = os.path.join(
            script_dir, 
            'paths', 
            fileName
        )
        
        # image of bag to check if in battle
        self.battle_needle = os.path.join(
            script_dir, 
            'needles', 
            'battleNeedle.png'
        )
        # list of key presses and time delay
        self.instructions = []
        with open(needle_path, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            # reads list of key inputs
            for pair in reader:
                pair = pair[0].split(',')
                key = pair[0]
                length = float(pair[1])
                self.instructions.append((key, length))
        
    
    def holdKey(self, key: str, seconds:float = 1.0):
        """Holds a key down for specified number of seconds."""
        pydirectinput.keyDown(key)
        time.sleep(seconds)
        pydirectinput.keyUp(key)
        
    def pokecenter(self):
        raise NotImplementedError('Not Implemented')
        
    def toLocation(self):
        """Follows the list of instructions to farming location."""
        for key, length in self.instructions:
            if key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)

    def debug(self):
        """Method for debug testing."""
        img = pyautogui.screenshot()
        gry = img.convert('L')
        bw = gry.point(lambda x: 255 if x<128 else 0, '1')
        bw.show()

    def isShiny(self):
        """Checks if encounter contains a shiny Pokemon."""
        # Pokemon name regions
        regions = [(300,125,300,25), (530,75,820,25), (530,115,820,25)]
        text = ''
        for r in regions:
            img = np.array(pyautogui.screenshot(region=r))
            text += self.reader.recognize(img,detail=0)[0]
        return 'shiny' in text.lower()
            
    def unwantedEncounter(self):
        """Runs from unwanted encounters."""
        self.holdKey('right', 0.5)
        pydirectinput.press('z')
        time.sleep(1.5)
        
    def stall(self):
        """Stalls for time if user is AFK when shiny is found so user does not
        time out from being AFK. Moves left or right once every minute."""
        length = 0
        while True:
            pydirectinput.press('left')
            time.sleep(60)
            pydirectinput.press('right')
            time.sleep(60)
            length = length + 120
            print(length / 60)
            
    def imgOnScreen(self, fileName: str):
        """Checks if specified image is found on the screen."""
        return pyautogui.locateOnScreen(fileName)
    
    def checkScreen(self):
        """Checks if horde is encountered upon entering location."""
        time.sleep(11)
        # checks if in battle
        bag = self.imgOnScreen(self.battle_needle)
        if bag is not None:
            # takes action when battle loads
            if not self.isShiny():
                self.unwantedEncounter()
            else:
                print('Shiny detected!')
                self.stall()
    
    def horde(self):
        """Automates Pokemon horde encounters."""
        # uses sweet scent to start horde fight
        pydirectinput.press('c')
        time.sleep(10)
        # checks if bag icon is on screen to confirm battle is not lagging
        bag = self.imgOnScreen(self.battle_needle)
        while bag is None:
            time.sleep(1)
            bag = self.imgOnScreen(self.battle_needle)
        # takes action when battle loads
        if not self.isShiny():
            self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()

            
    def hunt(self):
        """Overall hunt method for healing, pathing, and grinding."""
        self.pokecenter()
        # route to grinding location
        self.toLocation()
        # check if entering location enters battle
        self.checkScreen()
        for i in range(6):
            self.horde()
        # teleport
        pydirectinput.press('v')
        time.sleep(4)
        
class Hoenn(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 0.7) 
        # leaving pokecenter
        self.holdKey('down', 1.3)
        time.sleep(1)
        # outside + bike
        pydirectinput.press('1')
        
class Sinnoh(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 4) 
        # leaving pokecenter
        self.holdKey('down', 2)
        time.sleep(0.5)
        # outside + bike
        pydirectinput.press('1')
        
class Unova(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 4)
        # leaving pokecenter
        self.holdKey('down', 2.5)
        time.sleep(0.5)
        # outside + bike
        pydirectinput.press('1')