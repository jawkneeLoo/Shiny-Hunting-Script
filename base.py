import csv
import easyocr
import numpy as np
import os
import pyautogui as pyag
import pydirectinput as pydi
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
        pydi.keyDown(key)
        time.sleep(seconds)
        pydi.keyUp(key)
        
    def pokecenter(self):
        raise NotImplementedError('Not Implemented')
        
    def toLocation(self):
        """Follows the list of instructions to farming location."""
        for key, length in self.instructions:
            if key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)
            
    def isInBattle(self) -> bool:
        """Checks if battle UI is on the screen."""
        return pyag.pixelMatchesColor(287,725, (166, 105, 219), tolerance=5)

    def isShiny(self):
        """Checks if encounter contains a shiny Pokemon."""
        # Pokemon name regions
        regions = [(300,148,300,25), (530,98,820,25), (530,138,820,25)]
        text = ''
        for r in regions:
            img = np.array(pyag.screenshot(region=r))
            text += self.reader.recognize(img,detail=0)[0]
        return 'shiny' in text.lower()
            
    def unwantedEncounter(self):
        """Runs from unwanted encounters."""
        self.holdKey('right', 0.5)
        pydi.press('z')
        time.sleep(1.5)
        
    def stall(self):
        """Stalls for time if user is AFK when shiny is found so user does not
        time out from being AFK. Moves left or right once every minute."""
        length = 0
        while True:
            pydi.press('left')
            time.sleep(60)
            pydi.press('right')
            time.sleep(60)
            # prints how many minutes
            length = length + 120
            print(length / 60)
    
    def accidentalEncounter(self):
        """Checks if horde is encountered upon entering location."""
        time.sleep(2.5)
        # checks if battle UI has started
        if self.isInBattle():
            time.sleep(7)
            # takes action when battle loads
            if not self.isShiny():
                self.unwantedEncounter()
            else:
                print('Shiny detected!')
                self.stall()
    
    def horde(self):
        """Automates Pokemon horde encounters."""
        # uses sweet scent to start horde fight
        pydi.press('c')
        time.sleep(10)
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isInBattle():
            time.sleep(1)
        # takes action when battle loads
        if not self.isShiny():
            self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()

    def hunt(self):
        """Overall method for healing, pathing, and grinding."""
        self.pokecenter()
        # route to grinding location
        self.toLocation()
        # check if entering location enters battle
        self.accidentalEncounter()
        for i in range(6):
            self.horde()
        # teleport
        pydi.press('v')
        time.sleep(4)

    def debug(self):
        for key, length in self.instructions:
            if key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)
        
class Hoenn(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 0.9)
        # leaving pokecenter
        self.holdKey('down', 1.3)
        time.sleep(1)
        # outside + bike
        pydi.press('1')
        
class Sinnoh(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 4) 
        # leaving pokecenter
        self.holdKey('down', 2)
        time.sleep(0.5)
        # outside + bike
        pydi.press('1')
        
class Unova(Base):
    def pokecenter(self):
        # healing at pokecenter
        self.holdKey('z', 4)
        # leaving pokecenter
        self.holdKey('down', 2.5)
        time.sleep(0.5)
        # outside + bike
        pydi.press('1')