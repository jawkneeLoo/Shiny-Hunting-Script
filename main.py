import base
import specialEncounter as SE
import time

def main():
    #task = SE.grindGen3('bfEXP.csv')
    #task = SE.grindGen4('rhydonAtkEV.csv')
    #task = SE.grindGen5('rapidashSpdEV.csv')
    #task = base.Gen5('vanillish.csv')
    #task = SE.Deino()
    #task = SE.LegendaryDog()
    task = SE.Payday('undellaBay.csv')
    
    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        task.hunt()

if __name__ == '__main__':
    main()
 