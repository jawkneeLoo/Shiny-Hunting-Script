import os
import pyautogui
import pydirectinput
import pytesseract
import time

def main():
    pytesseract.tesseract_cmd = r'C:\Users\liuru\anaconda3\Library\bin\tesseract.exe'
    
    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    
    #loops hunting until ended
    while True:
        shunt()
    
def holdKey(key, seconds = 1.0):
    pydirectinput.keyDown(key)
    time.sleep(seconds)
    pydirectinput.keyUp(key)
    
def imgOnScreen(fileName):
    script_dir = os.path.dirname(__file__)
    needle_path = os.path.join(
        script_dir, 
        'needles', 
        fileName
    )
    return pyautogui.locateOnScreen(needle_path)
        
def checkScreen():
    img = pyautogui.screenshot()
    px = img.getpixel((1020, 500))
    time.sleep(1)
    if not pyautogui.pixelMatchesColor(1020, 500, px):
        time.sleep(20)
        unwantedEncounter()

def isShiny():
    img = pyautogui.screenshot().crop((610, 110, 1280, 125))
    text = pytesseract.image_to_string(img)[:-1]
    return 'Shiny' in text
    
def toSandile():
    #positioning before sand
    holdKey('right', 1.88)
    holdKey('down', 7.5)
    holdKey('left', 0.5)
    holdKey('down', 0.6)
    holdKey('right', 0.24)
    holdKey('down', 0.15)
    holdKey('left', 2.3)
    holdKey('up', 3)

def unwantedEncounter():
    holdKey('right', 0.5)
    pydirectinput.press('x')
    time.sleep(1.5)
    
def swarm():
    pydirectinput.press('c')
    time.sleep(11)
    pos = imgOnScreen('battleNeedle.png')
    while pos is None:
        time.sleep(1)
        pos = imgOnScreen('battleNeedle.png')
        print(pos)
    if not isShiny():
        unwantedEncounter()
        
def shunt():
    #heal
    holdKey('x', 7)
    holdKey('down', 2.5)
    time.sleep(0.4)
    pydirectinput.keyDown('1') #outside + bike
    #route to shunting location
    toSandile()
    #check if in unwanted battle
    checkScreen()
    for i in range(6):
        swarm()
    pydirectinput.press('v')
    time.sleep(4)
        
if __name__ == '__main__':
    main()