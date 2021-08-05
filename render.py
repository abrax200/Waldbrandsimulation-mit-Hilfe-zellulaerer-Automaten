#!/usr/bin/python3
import os
import time
import numpy as np
import sys


def path(p):
    if os.name == "nt":
        return p
    else:
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


def AusgabeTmp(feld, s):

    for i in range(s):
        out = ""

        for j in range(s):
            out = (
                out
                + str(feld[i][j])
                .replace("0", "W")
                .replace("1", "/")
                .replace("2", "-")
                .replace("3", "|")
                .replace("4", " ")
                .replace("5", "~")
                + " "
            )

        print(out)


def clear():
    if os.system("cls") != 0:
        os.system("clear")


def init():
    a = os.system("title Waldbrandsimulation")
    del a

    clear()


update = float(Argumente("intervall"))


feld = np.load(path(".\\data\\gen0.npy"))
size = len(feld)


for i in range(
    len(
        [
            name
            for name in os.listdir(path(".\\data"))
            if os.path.isfile(os.path.join(path(".\\data"), name))
        ]
    )
    - 1
):

    changes = np.load(path(".\\data\\gen" + str(i + 1) + ".npy"))
    length = len(changes)

    for i in range(length):
        x = int(changes[i][1])
        y = int(changes[i][2])
        feld[x][y] = changes[i][0]

    clear()
    AusgabeTmp(feld, size)
    time.sleep(update)

a = os.system("pause")
del a
