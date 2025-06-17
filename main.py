import base
import specialEncounter as se
import time
from pydirectinput import FailSafeException

def main():
    #task = base.GrindGen3('bfEXP.csv')
    task = base.GrindGen4('atkEV.csv')
    # task = base.GrindGen5('spdEV.csv')
    # task = base.Gen3('magikarp.csv')
    # task = se.RoamingLegendary()
    # task = se.Payday('dragonspiral.csv')
    # task = se.Thief('evergrande.csv')
    # task = se.Ursaring()

    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        try:
            task.hunt()
        except:
            task.sct.close()

if __name__ == '__main__':
    main()
 