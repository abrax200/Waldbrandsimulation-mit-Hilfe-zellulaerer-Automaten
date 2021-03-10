#!/usr/bin/python3
#Setzt Program, mit Welchen die Datei ausgeführt wird(Linux)
#import notwendiger Bilbliotheken
import os
import time
import sys
from random import randint
import numpy as np



class Waldbrandsimulation:

        def preinit(self):
                self.clear()
                a = os.system('title Waldbrandsimulation')
                del(a)
                os.system('del data\*.* /q')
                


        def init(self, size):
                self.wald = 0
                self.brennend = 1
                self.verbrannt = 2
                self.schneise = 3
                self.leer = 4
                
                self.size = size



        def Statistik(self, feld):

                verbrannte_fläche = 0
                bewaldete_fläche = 0
                brennende_fläche = 0

                for i in range(self.size):
                        for j in range(self.size):
                                if int(feld[0][i][j]) == self.verbrannt:
                                        verbrannte_fläche = verbrannte_fläche + 1
                        
                                if int(feld[0][i][j]) == self.wald:
                                        bewaldete_fläche += 1
                        
                                if int(feld[0][i][j]) == 1:
                                        brennende_fläche += 1
                        
                return(verbrannte_fläche, bewaldete_fläche, brennende_fläche)


        def ErstelleFeld(self):

                # definiert ein zweidimensionales Array
                feld = [np.array([[self.wald for j in range(self.size)] for i in range(self.size)]), np.array([[[10, 0, 10] for j in range(self.size)] for i in range(self.size)])]#status, brennpotential, time, feuchte

                return feld



        def Brennstärke(self, f, i, j):

                if (i < 0) or (i > self.size-1) or (j > self.size-1) or (j < 0):
                        return(0)

                else:   
                        brennstoff = int(f[1][i][j][0])
                        brenndauer = int(f[1][i][j][1])
                        return(brennstoff * brenndauer)



        def SummeBrennstärke(self, f, i, j, wr, windstärke):

                windrichtung = wr.replace('W', 'Westen').replace('O', 'Osten').replace('N', 'Norden').replace('S', 'Süden')

                if windrichtung == 'Norden':
                        sum_brennstärke = (
                        self.Brennstärke(f, i-1, j) * windstärke +
                        self.Brennstärke(f, i+1, j) / windstärke +
                        self.Brennstärke(f, i, j+1) +
                        self.Brennstärke(f, i, j-1)
                        )

                if windrichtung == 'Süden':
                        sum_brennstärke = (
                        self.Brennstärke(f, i-1, j) / windstärke +
                        self.Brennstärke(f, i+1, j) * windstärke +
                        self.Brennstärke(f, i, j+1) +
                        self.Brennstärke(f, i, j-1)
                        )

                if windrichtung == 'Westen':
                        sum_brennstärke = (
                        self.Brennstärke(f, i-1, j) +
                        self.Brennstärke(f, i+1, j) +
                        self.Brennstärke(f, i, j+1)  / windstärke +
                        self.Brennstärke(f, i, j-1) * windstärke
                        )

                if windrichtung == 'Osten':
                        sum_brennstärke = (
                        self.Brennstärke(f, i-1, j) +
                        self.Brennstärke(f, i+1, j) +
                        self.Brennstärke(f, i, j+1) * windstärke +
                        self.Brennstärke(f, i, j-1) / windstärke
                        )

                return(sum_brennstärke)



        def BearbeiteZelle(self, f, i, j, wr, ws):

                status = int(f[0][i][j])
                brennstoff = int(f[1][i][j][0])
                brenndauer = int(f[1][i][j][1])
                feuchtigkeit = int(f[1][i][j][2])

                if int(f[0][i][j]) == 1 and int(f[1][i][j][0]) > 0:
                        brennstoff = int(f[1][i][j][0]) - 1
                        brenndauer = int(f[1][i][j][1]) + 1
        
                if int(f[1][i][j][0]) == 0 and int(f[0][i][j]) == 1:
                        status = 2 # -
                        brenndauer = 0
        
                if (f[0][i][j] == 0) and self.SummeBrennstärke(f, i, j, wr, ws) >= int(f[1][i][j][2]) and int(f[1][i][j][0]) > 0:
                        status = 1 # /

                if f[0][i][j] != status:
                        has_changed = [status, i, j]
        
                else: 
                        has_changed = []

                return([brennstoff, brenndauer, feuchtigkeit], status, has_changed)



        #Für Probleme mit Pfeilarithmetik
        def KopiereFeld(self, fQuell,fZiel):
                for i in range(self.size):
                        for j in range(self.size):
                                fZiel[0][i][j] = fQuell[0][i][j]
                                fZiel[1][i][j] = fQuell[1][i][j]
                return fZiel



        def clear(self):
                if os.system('cls') != 0:
                        os.system('clear')



simulation = Waldbrandsimulation()
simulation.preinit()



size = 30

inp = str(input('BITTE GRÖßE ANGEBEN (z.B. 30): '))

if inp != '':
        size = int(inp)

simulation.init(size)



#Windrichtung
simulation.clear()

windrichtung = 'W'
windstärke = 1

inp = str(input('NORDEN = N, SÜDEN = S, WESTEN = W, OSTEN = O, FREI LASSEN FÜR KEINEN WIND\nWINDRICHTUNG: '))

if inp !='':
        windstärke = 2
        windrichtung = str(inp)



#Felder werden erstellt
feld = simulation.ErstelleFeld()
feld2 = simulation.ErstelleFeld()



#Schneisen werden erzeugt
simulation.clear()

schneise_pos = input('SCHNEISEN\n(z. B. 1 3 erzeugt Schneisen in Spalte 1 und 3): ').split(' ')
print('\n', schneise_pos)

if schneise_pos != ['']:
        for i in range(size):
                for j in schneise_pos:
                        feld[1][i][int(j)] = [0, 0, 0]
                        feld[0][i][int(j)] = simulation.schneise



#Feuer erzeugen
simulation.clear()

print('BITTE NUR ZAHLEN VON 1 bis ', size, '\nz. B. 1 1')

inp = str(input('WELCHE ZELLE SOLL BRENNEN: '))

if inp != '':
        feld[0][int(inp.split(' ')[0])][int(inp.split(' ')[1])] = simulation.brennend

else:
        feld[0][15][0] = simulation.brennend



#feld speichern
np.save('.\\data\\gen0', feld[0])


#lauf 0
verbrannte_fläche, bewaldete_fläche, brennende_fläche = simulation.Statistik(feld)
generation = 0
has_changed = False
changes = []



#Hauptschleife
while brennende_fläche > 0:

        generation = generation + 1
        print('GENERATION: ',generation)

        simulation.clear()

        for i in range(size):
                for j in range(size):
                        feld2[1][i][j], feld2[0][i][j], change = simulation.BearbeiteZelle(feld, i, j, windrichtung, windstärke)

                        if change != []:
                                changes.append(change)
        
        verbrannte_fläche, bewaldete_fläche, brennende_fläche = simulation.Statistik(feld2)
        np.save('.\\data\\gen' + str(generation), np.array(changes))#speichere Array
        changes = []
        feld = simulation.KopiereFeld(feld2,feld)

print('Wird eine GUI benötigt?')
inp = str(input('Y/n: '))

if inp.upper() == 'N':
        os.system('.\\render.py')

else:
        os.system('.\\render_gui.py')
