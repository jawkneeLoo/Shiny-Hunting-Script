import base
import pyautogui as pyag
import pydirectinput as pydi
import time

class grindUnova(base.Unova):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        # uses sweet scent to start horde fight
        pydi.press('c')
        time.sleep(10)
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isInBattle():
            time.sleep(1)
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
        time.sleep(11)
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isInBattle():
            time.sleep(1)
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
        time.sleep(10)
        # checks if UI is on screen to confirm battle is not lagging
        while not self.isInBattle():
            time.sleep(1)
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