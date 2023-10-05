import base
import numpy as np
import pyautogui as pyag
import pydirectinput as pydi
import time

class grindUnova(base.Unova):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.5)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            for i in range(3):
                pydi.press('z')
            #enough time for EXP gain + level up text
            time.sleep(10)
        else:
            print('Shiny detected!')
            self.stall()

class grindSinnoh(base.Sinnoh):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.5)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            for i in range(3):
                pydi.press('z')
            #enough time for EXP gain + level up text
            time.sleep(10)
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

class grindHoenn(base.Hoenn):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isBattleReady():
            time.sleep(0.5)
        # takes action when battle loads
        if not self.isShiny():
            #attack horde with AOE
            for i in range(3):
                pydi.press('z')
            #enough time for EXP gain + level up text
            time.sleep(10)
        else:
            print('Shiny detected!')
            self.stall()
            
class Litwick(base.Unova):
    def __init__(self):
        super().__init__('litwick.csv')
        
    def hunt(self):
        self.pokecenter()
        # route to grinding location
        self.toLocation()
        # check if entering location enters battle
        self.accidentalEncounter()
        for i in range(6):
            self.horde()
        # teleport
        self.holdKey('right', 6)
        self.holdKey('down', 1)
        time.sleep(1)
        pydi.press('v')
        time.sleep(4)

class legendaryDog(base.Unova):
    def __init__(self):
        # random file name
        self.toCheck = ['shiny', 'entei', 'suicune', 'raikou']
        self.regions = [(300,148,300,25), (530,98,820,25), (530,138,820,25)]
        super().__init__('bfEXP.csv')
        
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
