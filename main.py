import base
import specialEncounter as SE
import time

def main():
    #task = SE.grindGen3('bfEXP.csv')
    #task = SE.grindGen4('atkEV.csv')
    #task = SE.grindGen5('spdEV.csv')
    #task = base.Gen3('magikarp.csv')
    #task = SE.LegendaryDog()
    #task = SE.Payday('undellaBay.csv')
    task = SE.Thief('evergrande.csv')
    #task = SE.Ursaring()

    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        task.hunt()

if __name__ == '__main__':
    main()
 