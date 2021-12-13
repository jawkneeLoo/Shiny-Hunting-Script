from base import Base
import specialEncounter
import time

def main():
    task = specialEncounter.bfEXP('bfEXP.csv')
    #task = Base('vanillish.csv')
    #task = specialEncounter.Sandile('sandile.csv')
    
    print('Script starting in 1 second...')
    time.sleep(1)
    print('Started')
    
    #loops hunting until ended
    while True:
        task.hunt()
   
if __name__ == '__main__':
    main()