import csv
from mss.windows import MSS as mss
import numpy as np
import os
import pydirectinput as pydi
from rapidocr import RapidOCR
import time
from typing import Tuple

class Base:
    """A class used to represent the base functions of grinding."""

    def __init__(self, fileName: str = None):
        # screen capture tool
        self.sct = mss()
        # OCR reader
        self.reader = RapidOCR()
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

    def matchColor(self, x: int, y: int, color: Tuple[int, int, int]) -> bool:
        """Checks if color is present on screen."""
        region = {
            "left": x,
            "top": y,
            "width": 1,
            "height": 1,
            "mon": 1,
        }
        sct_img = self.sct.grab(region)
        pixel = sct_img.pixel(0, 0)
        dist = sum(map(lambda x, y: abs(x - y), color, pixel))
        return dist < 25

    @staticmethod
    def holdKey(key: str, seconds: float = 1.0):
        """Holds a key down for specified number of seconds."""
        pydi.keyDown(key)
        time.sleep(seconds)
        pydi.keyUp(key)

    def holdKeyUntil(self, key: str, x: int, y: int,
                     color: Tuple[int, int, int]):
        """Holds a key down until pixel color is satisfied."""
        pydi.keyDown(key)
        while not self.matchColor(x, y, color):
            time.sleep(0.05)
        pydi.keyUp(key)

    def holdKeyWhile(self, key: str, x: int, y: int,
                     color: Tuple[int, int, int]):
        """Holds a key down while pixel color is satisfied."""
        pydi.keyDown(key)
        while self.matchColor(x, y, color):
            time.sleep(0.05)
        pydi.keyUp(key)

    def teleportToPokecenter(self):
        """Leaves hunting location to where teleport is possible."""
        # teleport
        pydi.press('v')
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)
             
    def pokecenter(self):
        """Heals and leaves Pokecenters"""
        # healing at pokecenter
        pydi.keyDown('z')
        time.sleep(0.5) # delay to ensure healing starts
        pydi.keyDown('down')
        # leaving pokecenter
        while self.matchColor(5,815,(0,0,0)):
            time.sleep(0.01)
        pydi.keyUp('z')
        pydi.keyUp('down')
        time.sleep(0.3) # delay to fully leave transition scene
        # outside + bike
        pydi.press('1')
        
    def toLocation(self):
        """Follows the list of instructions to farming location."""
        for key, length in self.instructions:
            # move mouse to coords (key, value)
            if key.isdigit() and (int(key) > 10):
                pydi.moveTo(int(key), int(length))
            elif key == 'click':
                pydi.click()
            # normal key input
            elif key != 'sleep':
                Base.holdKey(key, length)
            else:
                time.sleep(length)

    def isInBattle(self) -> bool:
        """Checks if battle UI is on the screen."""
        return self.matchColor(383,975, (165, 104, 217))
    
    def isHPVisible(self) -> bool:
        """Checks if encounter HP is on the screen."""
        horde = self.matchColor(895, 105, (128, 220, 37))
        single = self.matchColor(415, 155, (128, 220, 37))
        return horde or single

    def isBattleReady(self) -> bool:
        """Checks if battle selection UI is ready."""
        return self.matchColor(395,1015, (165, 104, 217))

    def isShiny(self):
        """Checks if encounter contains a shiny Pokemon."""
        # Pokemon name regions
        regions = [{"left": 410, "top": 120, "width": 250, "height": 25, "mon": 1},
            {"left": 880, "top": 75, "width": 820, "height": 25, "mon": 1},
            {"left": 880, "top": 115, "width": 820, "height": 25, "mon": 1}]
        text = ''
        for r in regions:
            sct_img = self.sct.grab(r)
            img = np.array(sct_img)
            result = self.reader(img)
            if result.txts: # if OCR reads anything
                text += ' '.join(result.txts)
        print(text)
        return 'shiny' in text.lower()
            
    def battleProcedure(self):
        """Runs from unwanted encounters by default."""
        pydi.press('right')
        pydi.press('down')
        pydi.press('z')

    @staticmethod
    def stall():
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

    def encounterProcedure(self):
        """Contains logic for how to handle an encounter"""
        # wait for HP to appear and then read names
        while not self.isHPVisible():
            time.sleep(0.05)
        shiny = self.isShiny()
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.05)
        # takes action when battle loads
        if not shiny:
            self.battleProcedure()
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.1)
        else:
            print('Shiny detected!')
            self.stall()

    def accidentalEncounter(self):
        """Checks if horde is encountered upon entering location."""
        time.sleep(2.5)
        # checks if battle UI has started
        if self.isInBattle():
            self.encounterProcedure()
    
    def horde(self):
        """Automates Pokemon horde encounters."""
        # uses sweet scent to start horde fight
        pydi.press('c')
        self.encounterProcedure()

    def hunt(self, accident = True):
        """Overall method for healing, pathing, and grinding."""
        # if not at counter
        if not self.matchColor(self.pX, self.pY, self.pColor):
            self.teleportToPokecenter()
        # heals and leaves
        self.pokecenter()
        # route to grinding location
        self.toLocation()
        # check if entering location enters battle
        if accident:
            self.accidentalEncounter()
        for i in range(6):
            self.horde()
        self.teleportToPokecenter()

"""Basic functionality change classes"""
class Grind(Base):
    def __init__(self, fileName):
        super().__init__(fileName)

    def battleProcedure(self):
        # attack horde with AOE
        pydi.press('z', presses=3)

class Gen3(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 1085
        self.pY = 557
        self.pColor = (246, 127, 111)
        
class Gen4(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 970
        self.pY = 510
        self.pColor = (224, 221, 224)

class Gen5(Base):
    def __init__(self, fileName):
        super().__init__(fileName)
        self.pX = 1242
        self.pY = 623
        self.pColor = (243, 102, 180)

"""Combination of classes"""
class GrindGen5(Grind, Gen5):
    def __init__(self, fileName):
        super().__init__(fileName)

class GrindGen4(Grind, Gen4):
    def __init__(self, fileName):
        super().__init__(fileName)

class GrindGen3(Grind, Gen3):
    def __init__(self, fileName):
        super().__init__(fileName)