import csv
import easyocr
import numpy as np
import os
import pyautogui as pyag
import pydirectinput as pydi
import time

class Base:
    """A class used to represent the base functions of grinding."""

    def __init__(self, fileName: str = None):
        pyag.FAILSAFE = False
        # OCR reader
        self.reader = easyocr.Reader(['en'], detector=False)
        # if provided a file name
        if fileName:
            # placeholder pokecenter counter positions
            self.pX, self.pY, self.pColor = 0, 0, (0,0,0)
            # file paths for instructions
            script_dir = os.path.dirname(__file__)
            needle_path = os.path.join(
                script_dir, 
                'paths', 
                fileName
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
        
    
    def holdKey(self, key: str, seconds: float = 1.0):
        """Holds a key down for specified number of seconds."""
        pydi.keyDown(key)
        time.sleep(seconds)
        pydi.keyUp(key)
        
    def pokecenter(self):
        """Heals and leaves Pokecenters"""
        # healing at pokecenter
        pydi.keyDown('z')
        pydi.keyDown('down')
        time.sleep(0.5) # delay to ensure healing starts
        # heal until leaving counter
        while self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)
        pydi.keyUp('z')
        # leaving pokecenter
        while self.matchColor(5,815,(0,0,0)):
            time.sleep(0.2)
        pydi.keyUp('down')
        time.sleep(0.5) # delay to fully leave transition scene
        # outside + bike
        pydi.press('1')
    
    def leave(self):
        """Leaves hunting location to where teleport is possible."""
        # teleport
        pydi.press('v')
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)
        
    def toLocation(self):
        """Follows the list of instructions to farming location."""
        for key, length in self.instructions:
            # move mouse to coords (key, value)
            if key.isdigit() and (int(key) > 10):
                pyag.moveTo(int(key), int(length))
            elif key == 'click':
                pydi.click()
            # normal key input
            elif key != 'sleep':
                self.holdKey(key, length)
            else:
                time.sleep(length)
            
    def matchColor(self, x: int, y: int, color: tuple) -> bool:
        """Checks if color is present on screen."""
        return pyag.pixelMatchesColor(x,y, color, tolerance=5)

    def isInBattle(self) -> bool:
        """Checks if battle UI is on the screen."""
        return self.matchColor(287,725, (165, 104, 217))

    def isBattleReady(self) -> bool:
        """Checks if battle UI is ready."""
        return self.matchColor(502,763, (165, 104, 217))

    def isShiny(self):
        """Checks if encounter contains a shiny Pokemon."""
        # Pokemon name regions
        regions = [(300,148,300,25), (530,98,820,25), (530,138,820,25)]
        text = ''
        for r in regions:
            img = np.array(pyag.screenshot(region=r))
            text += self.reader.recognize(img,detail=0)[0]
        print(text)
        return 'shiny' in text.lower()
            
    def unwantedEncounter(self):
        """Runs from unwanted encounters."""
        self.holdKey('right', 0.5)
        pydi.press('z')
        # waits until UI fully fades due to lag
        while self.isInBattle():
            time.sleep(0.2)
        
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
            length = length + 2
            print(length)
    
    def accidentalEncounter(self):
        """Checks if horde is encountered upon entering location."""
        time.sleep(2.5)
        # checks if battle UI has started
        if self.isInBattle():
            while not self.isBattleReady():
                time.sleep(0.2)
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
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.3)
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
        self.leave()

class Gen3(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 980
        self.pY = 437
        self.pColor = (176,176,160)
        
class Gen4(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 980
        self.pY = 436
        self.pColor = (224, 221, 224)

class Gen5(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 1203
        self.pY = 507
        self.pColor = (183, 71, 54)