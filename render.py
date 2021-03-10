import os
import time
import numpy as np

def AusgabeTmp(feld, s):

        for i in range(s):
                out =""

                for j in range(s):
                        out = out + str(feld[i][j]).replace('0', 'W').replace('1', '/').replace('2', '-').replace('3', '|') + " "

                print(out)

def clear():
        if os.system("cls") != 0:
                os.system("clear")

def init():
        a = os.system('title Waldbrandsimulation')
        del(a)

        clear()



update = 0.25

inp = str(input('INTERVAL (z.B. 0.25): '))

if inp != '':
        update = float(inp)
        #/update



feld = np.load('.\\data\\gen0.npy')
size = len(feld)



for i in range(len([name for name in os.listdir('.\\data') if os.path.isfile(os.path.join('.\\data', name))]) - 1):
    
    changes = np.load('.\\data\\gen' + str(i + 1) + '.npy')
    length = len(changes)

    for i in range(length):
        x = int(changes[i][1])
        y = int(changes[i][2])
        feld[x][y] = changes[i][0]
    
    clear()
    AusgabeTmp(feld, size)
    time.sleep(update)

a = os.system('pause')
del(a)