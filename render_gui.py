#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
from matplotlib.colors import ListedColormap


def path(p):
    if os.name == "nt":
        return ".\\" + p
    return p.replace("\\", "/")


def Argumente(arg):
    standards = {"intervall": 0.25}

    for i in sys.argv:
        if str(arg) in i:
            value = i.replace(str(arg) + "=", "")

            if value == str(arg):
                return True
            else:
                return value
            break

    return standards[str(arg)]


def init():
    if os.name == "nt":
        a = os.system("title Waldbrandsimulation")
        del a

    global feld
    global size
    global data_len
    global data_counter

    feld = np.load(path("data\\gen0.npy"))
    size = len(feld)
    data_len = (
        len(
            [
                name
                for name in os.listdir(path("data"))
                if os.path.isfile(os.path.join(path("data"), name))
            ]
        )
        - 1
    )
    data_counter = 0


def updatefig(*args):
    global size
    global feld
    global data_len
    global data_counter

    data_counter = data_counter + 1

    try:

        changes = np.load(path("data\\gen" + str(data_counter + 1) + ".npy"))
        length = len(changes)

        for i in range(length):
            x = int(changes[i][1])
            y = int(changes[i][2])
            feld[x][y] = changes[i][0]

        im.set_array(feld)

        return (im,)

    except:
        return (im,)


intervall = float(Argumente("intervall"))


init()


fig = plt.figure()
colormap = ["#006600", "#FF5E00", "#473001", "#C0C0C0", "#472101", "#00b8ff"]
cmap = ListedColormap(colormap)
im = plt.imshow(feld, animated=True, cmap=cmap, vmin=0, vmax=len(colormap) - 1)
plt.xticks([])
plt.yticks([])


ani = animation.FuncAnimation(fig, updatefig, blit=True, interval=intervall * 1000)


try:
    plt.show()
except:
    pass
