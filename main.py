import base
import specialEncounter
import time

def main():
    #task = specialEncounter.grindHoenn('bfEXP.csv')
    #task = specialEncounter.grindUnova('rapidashSpdEV.csv')
    task = specialEncounter.grindSinnoh('rhydonAtkEV.csv')
    #task = base.Unova('vanillish.csv')
    #task = specialEncounter.Litwick()

    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        task.hunt()

if __name__ == '__main__':
    main()
 