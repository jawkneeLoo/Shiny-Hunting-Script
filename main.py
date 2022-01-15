import base
import specialEncounter
import time

def main():
    #task = specialEncounter.evEXP('bfEXP.csv')
    #task = specialEncounter.evEXP('spAtkEV.csv')
    #task = base.Unova('vanillish.csv')
    #task = base.Unova('mienfoo.csv')
    #task = base.Hoenn('magikarp.csv')
    #task = specialEncounter.Litwick()
    #task = specialEncounter.Sandile()
    task = base.Sinnoh('swablu.csv')
    #task = specialEncounter.Ralts()
    #task = base.Unova('duosion.csv')
    
    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    #loops hunting until ended
    while True:
        task.hunt()
   
if __name__ == '__main__':
    main()
 