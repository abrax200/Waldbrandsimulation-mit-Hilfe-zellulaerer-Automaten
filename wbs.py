#!/usr/bin/python3
#Setzt Program, mit Welchen die Datei ausgeführt wird(Linux)
#import notwendiger Bilbliotheken
import os
import time
import sys
from random import randint
import numpy as np



class Waldbrandsimulation:

        def path(self, p):
                if os.name == 'nt':return(p)
                else:return(p.replace('\\', '/'))



        def Argumente(self, arg):

                argumente = []
                argumente[:] = sys.argv[:]
                del argumente[0]

                self.standards = {
                        'size':30, 
                        'fluss':False, 
                        'bcell':"15,0", 
                        'schneisen':'', 
                        "wr":'W', 
                        'ws':1, 
                        'nogui':False,
                        'intervall':0.25,
                        'rs':0,
                        'rb':0,
                        'rnd':False
                        }

                for i in argumente:
                        if str(arg) in i:
                                value = i.replace(str(arg) + '=', '')

                                if value == str(arg):return(True)
                                else:return(value)
                                break
                
                return(self.standards[str(arg)])



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



        def ErstelleFeld(self, rnd):

                # definiert ein zweidimensionales Array

                if rnd == True:feld = [np.array([[randint(0, randint(0, 1)) * 4 for j in range(self.size)] for i in range(self.size)]), np.array([[[10, 0, 10] for j in range(self.size)] for i in range(self.size)])]#status, brennpotential, time, feuchte
                else:feld = [np.array([[0 for j in range(self.size)] for i in range(self.size)]), np.array([[[10, 0, 10] for j in range(self.size)] for i in range(self.size)])]#status, brennpotential, time, feuchte

                return feld



        def Brennstärke(self, f, i, j):

                if (i < 0) or (i > self.size-1) or (j > self.size-1) or (j < 0):
                        return(0)

                else:   
                        brennstoff = float(feld[1][i][j][0])
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


        
        def BearbeiteZelle(self, f, i, j, wr, ws, rs, rmoisture):

                status = int(f[0][i][j])
                brennstoff = float(feld[1][i][j][0])
                brenndauer = int(f[1][i][j][1])
                feuchtigkeit = int(f[1][i][j][2])

                if int(f[0][i][j]) == 1 and float(feld[1][i][j][0]) > 0:
                        brennstoff = float(feld[1][i][j][0]) - (1 + rs)
                        brenndauer = int(f[1][i][j][1]) + 1
        
                if float(feld[1][i][j][0]) <= 0 and int(f[0][i][j]) == 1:
                        status = 2 # -
                        brenndauer = 0
                        brennstoff = 0
        
                if (f[0][i][j] == 0) and (self.SummeBrennstärke(f, i, j, wr, ws) - rmoisture) >= int(f[1][i][j][2]) and float(feld[1][i][j][0]) > 0:
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
                                fZiel[1][i][j] = fQuell[1][i][j]
                                fZiel[0][i][j] = fQuell[0][i][j]
                return fZiel



        def clear(self):
                if os.system('cls') != 0:
                        os.system('clear')



simulation = Waldbrandsimulation()
simulation.preinit()


#größe festlegen
size = int(simulation.Argumente('size'))



# Instanz erzeugen
simulation.init(size)



#Windrichtung
windrichtung = str(simulation.Argumente('wr'))
windstärke = float(simulation.Argumente('ws'))



#Regen
regenstärke = float(simulation.Argumente('rs'))
regenbeginn = int(simulation.Argumente('rb'))



#Regen
rnd = simulation.Argumente('rnd')



#Felder werden erstellt
feld = simulation.ErstelleFeld(rnd)
feld2 = simulation.ErstelleFeld(False)



#Fluss
if simulation.Argumente('fluss') == True:
        feld[0] = np.load(simulation.path('.\\fluss\\stati_fluss.npy'))
        feld[1] = np.load(simulation.path('.\\fluss\\parameter_fluss.npy'))
        size = 100



#Schneisen werden erzeugt
schneise_pos = simulation.Argumente('schneisen').split(',')

if schneise_pos != ['']:
        for i in range(size):
                for j in schneise_pos:
                        feld[1][i][int(j)] = [0, 0, 0]
                        feld[0][i][int(j)] = simulation.schneise



#Feuer erzeugen
bcell = simulation.Argumente('bcell')
feld[0][int(bcell.split(',')[0])][int(bcell.split(',')[1])] = simulation.brennend



#feld speichern
np.save(simulation.path('.\\data\\gen0'), feld[0])


#lauf 0
verbrannte_fläche, bewaldete_fläche, brennende_fläche = simulation.Statistik(feld)
generation = 0
has_changed = False
changes = []
regenfeuchte = 0



#Hauptschleife
while brennende_fläche > 0:

        generation = generation + 1
        print('GENERATION: ',generation)

        simulation.clear()

        for i in range(size):
                for j in range(size):

                        if generation >= regenbeginn:
                                regenfeuchte += 0.1 * regenstärke
                                feld2[1][i][j], feld2[0][i][j], change = simulation.BearbeiteZelle(feld, i, j, windrichtung, windstärke, regenstärke, regenfeuchte)
                        
                        else:
                                feld2[1][i][j], feld2[0][i][j], change = simulation.BearbeiteZelle(feld, i, j, windrichtung, windstärke, 0, 0)

                        if change != []:
                                changes.append(change)
        
        verbrannte_fläche, bewaldete_fläche, brennende_fläche = simulation.Statistik(feld2)
        np.save(simulation.path('.\\data\\gen' + str(generation)), np.array(changes))#speichere Array
        changes = []
        
        feld = simulation.KopiereFeld(feld2, feld)



intervall = str(simulation.Argumente('intervall'))



if simulation.Argumente('nogui') == True:os.system(simulation.path('.\\render.py intervall=' + intervall))
else:os.system(simulation.path('.\\render_gui.py intervall=' + intervall))
