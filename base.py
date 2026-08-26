import CONSTANTS
import csv
from mss.windows import MSS as mss
import numpy as np
import os
import pydirectinput as pydi
from rapidocr import RapidOCR
import re
import time
from typing import Dict, Tuple

class Base:
    """A class used to represent the base functions of grinding."""

    def __init__(self, fileName: str = None):
        self.sct = mss()
        self.reader = RapidOCR()
        # change sct regions based on monitor resolution
        if self.sct.monitors[1]['height'] == 1440:
            self.regions = [{"left": 410, "top": 120, "width": 280, "height": 30, "mon": 1},
                {"left": 860, "top": 75, "width": 840, "height": 30, "mon": 1},
                {"left": 860, "top": 115, "width": 840, "height": 30, "mon": 1}]
        else:
            self.regions = [{"left": 410, "top": 120, "width": 280, "height": 30, "mon": 1},
                {"left": 860, "top": 75, "width": 840, "height": 30, "mon": 1},
                {"left": 860, "top": 115, "width": 840, "height": 30, "mon": 1}]
        if fileName:
            # placeholder pokecenter counter positions
            self.pX, self.pY, self.pColor = 0, 0, (0,0,0)
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

    def readText(self, regions: Dict[str, int]) -> str:
        """Takes screenshot defined by region and reads text."""
        text = ''
        for r in regions:
            sct_img = self.sct.grab(r)
            img = np.array(sct_img)
            result = self.reader(img, use_det=False, use_cls=False, use_rec=True)
            if result.txts:
                text += result.txts[0]
        return text

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
            pass
        pydi.keyUp(key)

    def holdKeyWhile(self, key: str, x: int, y: int,
                     color: Tuple[int, int, int]):
        """Holds a key down while pixel color is satisfied."""
        pydi.keyDown(key)
        while self.matchColor(x, y, color):
            pass
        pydi.keyUp(key)

    def teleportToPokecenter(self):
        """Leaves hunting location to where teleport is possible."""
        # teleport
        pydi.press(CONSTANTS.TELEPORT)
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)
             
    def pokecenter(self):
        """Heals and leaves Pokecenters"""
        # healing at pokecenter
        pydi.keyDown(CONSTANTS.CONFIRM)
        time.sleep(0.5) # delay to ensure healing starts
        pydi.keyDown('down')
        # leaving pokecenter
        while self.matchColor(5,815,(0,0,0)):
            pass
        pydi.keyUp(CONSTANTS.CONFIRM)
        pydi.keyUp('down')
        time.sleep(0.3) # delay to fully leave transition scene
        # outside + bike
        pydi.press(CONSTANTS.BIKE)
        
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
        time.sleep(0.3)

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
        text = self.readText(self.regions)
        print(text)
        return 'shiny' in text.lower()

    def hasPP(self):
        """Checks if encounter contains a PP."""
        regions = [{"left": 625, "top": 30, "width": 20, "height": 15, "mon": 1}]
        pp = self.readText(regions)
        pp = int(pp.strip())
        return pp > 2

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
            length = length + 2
            print(length)

    def battleProcedure(self):
        """Runs from unwanted encounters by default."""
        pydi.press('right')
        pydi.press('down')
        pydi.press(CONSTANTS.CONFIRM)

    def encounterProcedure(self):
        """Contains logic for how to handle an encounter"""
        # wait for HP to appear and then read names
        while not self.isHPVisible():
            pass
        shiny = self.isShiny()
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            pass
        # takes action when battle loads
        if not shiny:
            self.battleProcedure()
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.1)
        else:
            print('Shiny detected!')
            self.stall()

    def mainTask(self):
        """Method defining the action done as the grind for this task."""
        while self.hasPP():
            # uses sweet scent to start horde fight
            pydi.press(CONSTANTS.SWEET_SCENT)
            self.encounterProcedure()

    def hunt(self):
        """Overall method for healing, pathing, and grinding."""
        # if not at counter
        if not self.matchColor(self.pX, self.pY, self.pColor):
            self.teleportToPokecenter()
        self.pokecenter()
        self.toLocation()
        self.mainTask()
        self.teleportToPokecenter()

"""Basic functionality change classes"""
class Grind(Base):
    def __init__(self, fileName):
        super().__init__(fileName)

    def battleProcedure(self):
        # attack horde with AOE
        pydi.press(CONSTANTS.CONFIRM, presses=3)

class GrindFish(Base):
    def __init__(self, fileName):
        super().__init__(fileName)

    def isShiny(self) -> bool:
        """Checks if single encounter contains a shiny Pokemon."""
        # Pokemon name regions
        regions = [{"left": 410, "top": 120, "width": 250, "height": 25, "mon": 1}]
        text = self.readText(regions)
        return 'shiny' in text.lower()

    def hasPP(self) -> bool:
        """Checks if first move still has PP."""
        regions = [{"left": 2135, "top": 1135, "width": 55, "height": 20, "mon": 1}]
        pp = self.readText(regions)
        pp = int(re.search(r'(\d+)', pp).group())
        return pp > 0

    def fish(self):
        """Fishes until a successful encounter."""
        while True:
            pydi.press(CONSTANTS.FISHING_ROD, presses=2)
            # wait for fishing dialogue
            while not self.matchColor(1685, 270, (251, 251, 251)):
                pass
            # check if successful fish
            if self.matchColor(890, 220, (251, 251, 251)):
                pydi.press(CONSTANTS.CONFIRM)
                break
            # dismiss dialogue
            pydi.press(CONSTANTS.CONFIRM)

    def battleProcedure(self):
        # attack single encounter
        pydi.press(CONSTANTS.CONFIRM, presses=2)

    def teleportToPokecenter(self):
        """Leaves hunting location to where teleport is possible."""
        # leave bridge
        pydi.press(CONSTANTS.BIKE)
        self.holdKey('down', 1.3)
        # checks for lag during transition
        while not self.matchColor(1225,520,(57, 57, 63)):
            time.sleep(0.05)
        super().teleportToPokecenter()

    def mainTask(self):
        while self.hasPP():
            self.fish()
            self.encounterProcedure()
        time.sleep(0.1)

class Gen3(Base):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)
        self.pX = 1280
        self.pY = 520
        self.pColor = (246, 206, 183)
        
class Gen4(Base):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)
        self.pX = 1275
        self.pY = 455
        self.pColor = (246, 206, 183)

class Gen5(Base):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)
        self.pX = 1242
        self.pY = 623
        self.pColor = (243, 102, 180)

"""Combination of classes"""
class GrindGen3(Grind, Gen3):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)

class GrindGen4(Grind, Gen4):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)

class GrindGen5(Grind, Gen5):
    def __init__(self, fileName: str = None):
        super().__init__(fileName)