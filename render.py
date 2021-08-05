#!/usr/bin/python3
import os
import time
import numpy as np
import sys


def command(p):
    if os.name == "nt":
        return ".\\" + p
    return "python3 " + p.replace("\\", "/")


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
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def init():
    a = os.system("title Waldbrandsimulation")
    del a

    # clear()


update = float(Argumente("intervall"))


feld = np.load(path("data\\gen0.npy"))
size = len(feld)


for name in os.listdir(path("data")):
    print(name)
    if os.path.isfile(os.path.join(path("data"), name)) and name.startswith("gen"):
        changes = np.load(path("data\\" + name))
        length = len(changes)

        for i in range(length):
            x = int(changes[i][1])
            y = int(changes[i][2])
            feld[x][y] = changes[i][0]

        clear()

        AusgabeTmp(feld, size)
        time.sleep(update)

if os.name == "nt":
    a = os.system("pause")
    del a
