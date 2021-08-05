#!/usr/bin/python3

import sys
import os


def command(p):
    if os.name == "nt":
        return ".\\" + p
    else:
        return "python3 " + p


def clear():
    if os.system("cls") != 0:
        os.system("clear")


args = [""]

#clear()

args.append('size=' + str(input('WIE GROSS SOLL DAS FELD SEIEN (Z.B. 30)? ')))
clear()
args.append('bcell=' + str(input('WELCHE ZELLE SOLL BRENNEN (Z.B. 15 0)? ')).replace(' ', ','))
clear()
#clear()

args.append("size=" + str(input("WIE GROSS SOLL DAS FELD SEIEN (Z.B. 30)? ")))
#clear()
args.append(
    "bcell=" + str(input("WELCHE ZELLE SOLL BRENNEN (Z.B. 15 0)? ")).replace(" ", ",")
)
#clear()
args.append(
    "schneisen="
    + str(input("WO SOLLEN SCHNEISEN EXISTIEREN (Z.B. 1 10?) ")).replace(" ", ",")
)
#clear()

inp = str(input("WELCHE WINDRICHTUNG? (NORDEN=N, SUEDEN=S, WESTEN=W, OSTEN=O)? "))
if inp != "":
    args.append("wr=" + inp)
    args.append("ws=" + "2")
#clear()

args.append("rs=" + str(input("WIE STARK SOLL ES REGNEN? (Z.B. 1)? ")))
#clear()
args.append("rb=" + str(input("WANN SOLL ES BEGINNEN ZU REGNEN? (Z.B. 10)? ")))
#clear()

if str(input("WIRD EINE GUI BENÖTIGT (Y/N) ? ")) == "N":
    args.append("nogui")
#clear()
args.append(
    "intervall="
    + str(input("WIE HOCH SOLL DAS INTERVALL FÜR DIE ANZEIGE SEIN? (IN SEKUNDEN)? "))
)
#clear()


command = command("wbs.py")

for arg in args:
    if arg != "" and arg[-1] != "=":
        command = command + " " + str(arg)

print(command)

with open("last_command", 'w') as f:
    f.write("#!/bin/sh\n" + command)

os.system(command)
