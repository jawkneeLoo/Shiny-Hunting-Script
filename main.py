import base
import specialEncounter as se
import time
from pydirectinput import FailSafeException

def main():
    task = base.GrindGen5('spdEV.csv')
    #task = base.Gen3('magikarp.csv')
    #task = SE.LegendaryDog()
    #task = SE.Payday('undellaBay.csv')
    #task = SE.Thief('evergrande.csv')
    #task = SE.Ursaring()

    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        try:
            task.hunt()
        except FailSafeException:
            task.sct.close()

if __name__ == '__main__':
    main()
 