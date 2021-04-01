import sys
import os

def path(p):
    if os.name == 'nt':return(p)
    else:return(p.replace('\\', '/'))

def clear():
                if os.system('cls') != 0:
                        os.system('clear')

args = ['']

clear()

if str(input("SOLL EIN FELD MIT EINEM FLUSS VERWENDET WERDEN (Y/N)? ")) == 'Y':
    clear()
    args.append('fluss')
    args.append('size=100')
clear()

args.append('size=' + str(input('WIE GROSS SOLL DAS FELD SEIEN (Z.B. 30)? ')))
clear()
args.append('bcell=' + str(input('WELCHE ZELLE SOLL BRENNEN (Z.B. 15 0)? ')).replace(' ', ','))
clear()
args.append('schneisen=' + str(input('WO SOLLEN SCHNEISEN EXISTIEREN (Z.B. 1 10?) ')).replace(' ', ','))
clear()

inp = str(input('WELCHE WINDRICHTUNG? (NORDEN=N, SUEDEN=S, WESTEN=W, OSTEN=O)? '))
if  inp != '':
    args.append('wr=' + inp)
    args.append('ws=' + '2')
clear()

args.append('rs=' + str(input('WIE STARK SOLL ES REGNEN? (Z.B. 1)? ')))
clear()
args.append('rb=' + str(input('WANN SOLL ES BEGINNEN ZU REGNEN? (Z.B. 10)? ')))
clear()

if str(input("WIRD EINE GUI BENÖTIGT (Y/N) ? ")) == 'N':args.append('nogui')
clear()
args.append('intervall=' + str(input('WIE HOCH SOLL DAS INTERVALL FÜR DIE ANZEIGE SEIN? (IN SEKUNDEN)? ')))
clear()



command = ".\\wbs.py"

for i in args:
    if i != '' and i[-1] != '=':
        command = command + " " + str(i)

print(command)



os.system(path(command))