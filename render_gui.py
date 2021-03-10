import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
from matplotlib.colors import ListedColormap

def clear():
        if os.system("cls") != 0:
                os.system("clear")

def init():
        a = os.system('title Waldbrandsimulation')
        del(a)

        global feld
        global size
        global data_len
        global data_counter
        global update

        feld = np.load('.\\data\\gen0.npy')
        size = len(feld)
        data_len = len([name for name in os.listdir('.\\data') if os.path.isfile(os.path.join('.\\data', name))]) - 1
        data_counter = 0

        #update (wie schnell wird die Simulation abgespielt)

        clear()

        update = 0.25

        inp = str(input('INTERVAL (z.B. 0.25): '))

        if inp != '':
                update = float(inp)
        
        clear()



def updatefig(*args):
        global size
        global feld
        global data_len
        global data_counter

        data_counter = data_counter + 1
        
        try:
        
                changes = np.load('.\\data\\gen' + str(data_counter + 1) + '.npy')
                length = len(changes)

                for i in range(length):
                        x = int(changes[i][1])
                        y = int(changes[i][2])
                        feld[x][y] = changes[i][0]

                im.set_array(feld)
                
                return im,

        
        except:
                return im,



init()



fig = plt.figure()
colormap = ['#006600', '#FF5E00', '#473001', '#C0C0C0', '#472101']
cmap = ListedColormap(colormap)
im = plt.imshow(feld , animated=True, cmap=cmap, vmin=0, vmax=len(colormap) - 1)
plt.xticks([])
plt.yticks([])



ani = animation.FuncAnimation(fig, updatefig,  blit=True, interval = update * 1000)



try:
        plt.show()
except:
        pass