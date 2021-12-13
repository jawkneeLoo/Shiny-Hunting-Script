from base import Base
import pyautogui
import pydirectinput
import pytesseract
import time

class bfEXP(Base):
    def pokecenter(self):
        #healing at pokecenter
        self.holdKey('x', 3.5) 
        #leaving pokecenter
        self.holdKey('down', 1.3)
        time.sleep(1)
        #outside + bike
        pydirectinput.press('1')
        
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

class Sandile(Base):
    def isShiny(self):
        img = pyautogui.screenshot().crop((510, 110, 1380, 125))
        text = pytesseract.image_to_string(img)[:-1]
        print(text)
        return 'shiny' in text.lower()

    def swarm(self):
        pydirectinput.press('c')
        time.sleep(11)
        pos = self.imgOnScreen('battleNeedle.png')
        while pos is None:
            time.sleep(1)
            pos = self.imgOnScreen('battleNeedle.png')
        if not self.isShiny():
            self.unwantedEncounter()
        else:
            print('Shiny detected!')
            self.stall()