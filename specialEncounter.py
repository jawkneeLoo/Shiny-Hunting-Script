import base
import numpy as np
import pyautogui as pyag
import pydirectinput as pydi
import re
import time

class grindGen5(base.Gen5):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.2)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            pydi.press('z', presses = 3)
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.2)
        else:
            print('Shiny detected!')
            self.stall()

class grindGen4(base.Gen4):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.2)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            pydi.press('z', presses = 3)
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.2)
        else:
            print('Shiny detected!')
            self.stall()

    def hunt(self):
        self.pokecenter()
        # route to grinding location
        self.toLocation()
        # check if entering location enters battle
        self.accidentalEncounter()
        for i in range(6):
            self.horde()
        # teleport
        self.holdKey('down', 0.3)
        time.sleep(1)
        pydi.press('v')
        time.sleep(4)

class grindGen3(base.Gen3):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.2)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            pydi.press('z', presses = 3)
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.2)
        else:
            print('Shiny detected!')
            self.stall()

class Thief(base.Gen3):
    def __init__(self, fileName: str):
        super().__init__(fileName)

    def isShiny(self) -> int:
        """Checks if single encounter contains a shiny Pokemon."""
        # Pokemon name regions
        img = np.array(pyag.screenshot(region = (300,148,300,25)))
        text = self.reader.recognize(img,detail=0)[0]
        return 'shiny' in text.lower()
        
    def hasPP(self) -> bool:
        """Checks if first move still has PP."""
        img = pyag.screenshot(region=(1495,825,57,15))
        pp = self.reader.recognize(np.array(img),detail=0)[0]
        pp = re.search('\d+', pp).group()
        return int(pp) > 0
    
    def fish(self):
        """Fishes until a successful encounter."""
        encounter = False
        # while fishing isn't successful
        while not encounter:
            # fish
            pydi.press('shiftleft')
            # wait for fishing dialogue
            while not self.matchColor(1362,212,(251, 251, 251)):
                time.sleep(0.2)
            # check if successful fish
            if self.matchColor(562,154,(251, 251, 251)):
                encounter = True
            # dismiss dialogue
            pydi.press('z')
    
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
                pydi.press('z', presses = 2)
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

class Payday(base.Gen5):
    def __init__(self, fileName: str):
        super().__init__(fileName)

    def isShiny(self) -> bool:
        """Checks if single encounter contains a shiny Pokemon."""
        # Pokemon name regions
        img = np.array(pyag.screenshot(region = (300,148,300,25)))
        text = self.reader.recognize(img,detail=0)[0]
        return 'shiny' in text.lower()

    def hasPP(self) -> bool:
        """Checks if first move still has PP."""
        img = pyag.screenshot(region=(1495,825,57,15))
        pp = self.reader.recognize(np.array(img),detail=0)[0]
        pp = re.search('\d+', pp).group()
        return int(pp) > 0
        
    def fish(self):
        """Fishes until a successful encounter."""
        encounter = False
        # while fishing isn't successful
        while not encounter:
            # fish
            pydi.press('shiftleft')
            # wait for fishing dialogue
            while not self.matchColor(1362,212,(251, 251, 251)):
                time.sleep(0.2)
            # check if successful fish
            if self.matchColor(562,154,(251, 251, 251)):
                encounter = True
            # dismiss dialogue
            pydi.press('z')
    
    def battle(self):
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.2)
        # takes action when battle loads
        if not self.isShiny():
            pydi.press('z', presses = 2)
            while self.isInBattle():
                time.sleep(0.2)
        else:
            print('Shiny detected!')
            self.stall()
    """
    def leave(self):
        # leave bridge
        pydi.press('1')
        self.holdKey('down', 1)
        # checks for lag during transition
        while self.matchColor(900,415,(251, 251, 251)):
            time.sleep(0.2)
        time.sleep(1)
        pydi.press('v')
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)
    """

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

class LegendaryDog(base.Gen3):
    def __init__(self):
        # random file name
        self.toCheck = ['shiny', 'entei', 'suicune', 'raikou']
        self.regions = [(300,148,300,25), (530,98,820,25), (530,138,820,25)]
        super().__init__()
        
    def isImportant(self):
        """Checks if encounter contains a shiny Pokemon."""
        # Pokemon name regions
        text = ''
        for r in self.regions:
            img = pyag.screenshot(region=r)
            img = np.array(img)
            text += self.reader.recognize(img,detail=0)[0]
        text = text.strip()
        print(text)
        for check in self.toCheck:
            if check in text.lower():
                return True
        return False

    def encounter(self):
        while not self.isBattleReady():
            time.sleep(0.5)
        if not self.isImportant():
            self.unwantedEncounter()
        else:
            print('Shiny or legendary detected!')
            self.stall()
    
    def hunt(self):
        # runs back and forth
        self.holdKey('right', 0.4)
        if self.isInBattle():
            self.encounter()
        self.holdKey('left', 0.2)
        if self.isInBattle():
            self.encounter()
