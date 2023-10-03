import base
import pyautogui
import pydirectinput
import easyocr
import time

class evEXP(base.Hoenn):
    def __init__(self, fileName):
        super().__init__(fileName)
        
    def horde(self):
        #sweet scent
        pydirectinput.press('c')
        #wait for encounter animations
        time.sleep(11) #14 for ttar, 11(?) for most
        if not self.isShiny():
            #attack horde with AOE
            for i in range(3):
                pydirectinput.press('z')
            #enough time for EXP gain + level up text
            time.sleep(12)
        else:
            print('Shiny detected!')
            self.stall()
            
class Litwick(base.Unova):
    def __init__(self):
        super().__init__('litwick.csv')
        
    def hunt(self):
        self.pokecenter()
        #route to shunting location
        self.toLocation()
        for i in range(6):
            self.horde()
        self.holdKey('right', 6)
        self.holdKey('down', 1)
        time.sleep(1)
        pydirectinput.press('v')
        time.sleep(4)