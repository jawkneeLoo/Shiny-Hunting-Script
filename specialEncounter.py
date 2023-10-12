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
            for i in range(3):
                pydi.press('z')
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
            for i in range(3):
                pydi.press('z')
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
            for i in range(3):
                pydi.press('z')
            # waits until UI fully fades due to lag
            while self.isInBattle():
                time.sleep(0.2)
        else:
            print('Shiny detected!')
            self.stall()

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
        """Checks if first move still have PP."""
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
            #attack with payday
            for i in range(2):
                pydi.press('z')
            # waits until UI fully fades due to lag
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
        # victory road color difference
        self.pColor = (158,71,60)

    def leave(self):
        # leave cave
        self.holdKey('down', 0.3)
        while self.matchColor(5,815,(0,0,0)):
            time.sleep(0.2)
        time.sleep(1)
        # teleport
        pydi.press('v')
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)

class Litwick(base.Gen5):
    def __init__(self):
        super().__init__('litwick.csv')

    def leave(self):
        # teleport
        self.holdKey('right', 6)
        self.holdKey('down', 1)
        time.sleep(1)
        pydi.press('v')
        # sleep until pokecenter counter is visible
        while not self.matchColor(self.pX, self.pY, self.pColor):
            time.sleep(0.2)

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
