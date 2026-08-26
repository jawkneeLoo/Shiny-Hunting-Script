import CONSTANTS
import base
import numpy as np
import pydirectinput as pydi
import re
import time

class Thief(base.Gen3):
    def __init__(self, fileName: str):
        super().__init__(fileName)
    
    def fish(self):
        """Fishes until a successful encounter."""
        encounter = False
        # while fishing isn't successful
        while not encounter:
            # fish
            pydi.press(CONSTANTS.FISHING_ROD)
            # wait for fishing dialogue
            while not self.matchColor(1362,212,(251, 251, 251)):
                time.sleep(0.2)
            # check if successful fish 882 220
            if self.matchColor(562,154,(251, 251, 251)):
                encounter = True
            # dismiss dialogue
            pydi.press(CONSTANTS.CONFIRM)
    
    def takeItem(self):
        #self.matchColor(1902, 436, (79, 173, 24))
        pydi.moveTo(1902, 436)
        pydi.click()
        pydi.moveTo(1820, 490)
        pydi.click()

    def battle(self):
        # checks if UI is on screen to confirm battle is not lagging
        item = self.matchColor(501, 582, (165, 104, 217))
        battle = self.isBattleReady()
        # wait until battle UI appears
        while not battle:
            time.sleep(0.05)
            # if item isn't detected
            if not item:
                item = self.matchColor(501, 582, (165, 104, 217))
            battle = self.isBattleReady()
        # takes action when battle loads
        if not self.isShiny():
            # if item is found
            if item:
                pydi.press(CONSTANTS.CONFIRM, presses = 2)
                while self.isInBattle():
                    time.sleep(0.2)
                self.takeItem()
            else:
                self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()

    def hunt(self):
        """Overall method for healing, pathing, and grinding."""
        if self.matchColor(self.pX, self.pY, self.pColor):
            # heals and leaves
            self.pokecenter()
            # route to grinding location
            self.toLocation()
        while self.hasPP():
            self.fish()
            self.battle()
        self.leave()

class Payday(base.GrindFish, base.Gen5):
    def __init__(self, fileName: str):
        super().__init__(fileName)

class Deino(base.Gen5):
    def __init__(self):
        super().__init__('deino.csv')

    def toLocation(self):
        super(Deino, self).toLocation()
        self.holdKeyUntil('up', 5,815,(0,0,0))
        time.sleep(0.5)

    def leave(self):
        # leave cave
        self.holdKeyUntil('down', 5,815,(0,0,0))
        time.sleep(1)
        # teleport
        super(Deino, self).leave()

    def hunt(self):
        super(Deino, self,).hunt(False)

class Litwick(base.Gen5):
    def __init__(self):
        super().__init__('litwick.csv')

    def leave(self):
        # leave tower
        self.holdKeyUntil('right', 1000, 780, (242, 242, 242))
        self.holdKeyWhile('down', 5, 815, (0,0,0))
        time.sleep(0.5)
        super(Litwick, self).leave()
        
    def toLocation(self):
        """Follows the list of instructions to farming location."""
        super(Litwick, self).toLocation()
        # go up stairs
        self.holdKeyUntil('left', 1700, 125, (0, 0, 0))
        time.sleep(0.5)

    def hunt(self):
        """Overall method for healing, pathing, and grinding."""
        super(Litwick, self,).hunt(False)
    
    def debug(self):
        self.holdKeyUntil('right', 1273, 481, (58, 132, 189))

class Ursaring(base.Gen4):
    def __init__(self):
        super().__init__('ursaring.csv')

    def toLocation(self):
        super(Ursaring, self).toLocation()
        self.holdKeyUntil('up', 5,815,(0,0,0))
        time.sleep(1)
        self.holdKeyWhile('up', 955, 1050, (0,0,0))
        self.holdKeyUntil('up', 955, 1050, (0,0,0))
        time.sleep(2)
        pydi.press('up')

    def leave(self):
        # leave cave
        self.holdKeyWhile('down', 5,815,(0,0,0))
        time.sleep(1)
        # teleport
        super(Ursaring, self).leave()

class RoamingLegendary(base.Gen3):
    def __init__(self):
        super().__init__()
        self.toCheck = ['shiny', 'entei', 'suicune', 'raikou', 'zapdos', 'articuno', 'moltres']
        
    def isShiny(self):
        """Checks if encounter contains an important Pokemon."""
        text = self.readText(self.regions)
        print(text)
        for check in self.toCheck:
            if check in text.lower():
                return True
        return False
    
    def hunt(self):
        # runs back and forth
        self.holdKey('right', 0.35)
        if self.isInBattle():
            self.encounterProcedure()
        self.holdKey('left', 0.3)
        if self.isInBattle():
            self.encounterProcedure()
