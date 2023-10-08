import base
import specialEncounter
import time

def main():
    #task = specialEncounter.grindGen3('bfEXP.csv')
    #task = specialEncounter.grindGen4('rhydonAtkEV.csv')
    task = specialEncounter.grindGen5('rapidashSpdEV.csv')
    #task = base.Gen5('vanillish.csv')
    #task = specialEncounter.Deino()
    #task = specialEncounter.legendaryDog()

    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        task.hunt()

if __name__ == '__main__':
    main()
 