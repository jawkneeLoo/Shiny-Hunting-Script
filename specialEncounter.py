import base
import pyautogui
import pydirectinput
import pytesseract
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
                pydirectinput.press('x')
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

class Ralts(base.Sinnoh):
    def __init__(self):
        super().__init__('ralts.csv')
        
    def isShiny(self):
        img = pyautogui.screenshot().crop((600, 110, 1380, 125))
        gry = img.convert('L')
        bw = gry.point(lambda x: 255 if x<128 else 0, '1')
        text = pytesseract.image_to_string(bw)[:-1]
        print(text)
        return 'shiny' in text.lower()

class Sandile(base.Unova):
    def __init__(self):
        super().__init__('sandile.csv')
        
    def isShiny(self):
        img = pyautogui.screenshot().crop((600, 110, 1380, 125))
        gry = img.convert('L')
        bw = gry.point(lambda x: 255 if x<128 else 0, '1')
        text = pytesseract.image_to_string(bw)[:-1]
        print(text)
        return 'shiny' in text.lower()