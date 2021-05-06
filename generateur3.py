import numpy as np
from random import *
from scipy import signal
import time
#from matplotlib import pyplot as plt
from tkinter import *

size = 50

cmpV = np.ones((1,3))
cmpV[0,1] = 0
cmpH = np.ones((3,1))
cmpH[1,0] = 0



class Maze():
    def __init__(self, size):
        self.size = size
    
        self.map = np.arange(0,(self.size*2+1)**2)
        self.map = self.map.reshape(self.size*2+1,self.size*2+1)

        self.map[::2] = -1
        self.map[::,::2] = -1

        self.map[1,0] = self.map[1,1]
        self.map[self.size*2-1, self.size*2] = self.map[self.size*2-1,self.size*2-1]

        self.ligne0, self.colonne0 = np.where(self.map == -1)

        self.Fenetre = Tk()
        self.Fenetre.title("Maze Generator by Marius")

        self.frameJeu = Frame(self.Fenetre)
        self.frameJeu.grid(row = 1, column = 1, sticky = "news")

        self.grilleJeu = Canvas(self.frameJeu, background="light grey")

        self.grilleJeu.pack()

        self.mapAffichage = dict()
        self.colorCode = dict()
        self.colorCode[-1] = "black"
        for i in range((self.size*2+1)**2):
            self.colorCode[i] = "#"+"%06x"%randint(0, 0xFFFFFF)
        
        self.genPlein()
        self.map[self.map==self.map[1,0]] = 0


    def initAffichage(self):
        self.grilleJeu.config(height=600, width=600)
        for x in range(self.size*2+1):
            for y in range(self.size*2+1):
                self.mapAffichage[(x, y)] = self.grilleJeu.create_rectangle((600/(self.size*2+1))*y,
                                                                            (600/(self.size*2+1))*x,
                                                                            (600/(self.size*2+1))*(y+1),
                                                                            (600/(self.size*2+1))*(x+1),
                                                                            fill=self.colorCode[self.map[y, x]],
                                                                            width=0,
                                                                            tags=(x, y))

    def updateAffichage(self):
        for x in range(self.size*2+1):
            for y in range(self.size*2+1):
                self.grilleJeu.itemconfig(self.grilleJeu.find_withtag(self.mapAffichage[(x, y)])[0], fill=self.colorCode[self.map[x, y]])          

    def getMap(self):
        return self.map

    def setMap(self, map):
        self.map = map

    def setCase(self, x, y, value):
        self.map[x, y] = value

    def get0(self):
        return np.where(self.map==0)

    def getFenetre(self):
        return self.Fenetre

    def cassage(self):
        nbr = randint(0,len(self.ligne0)-1)
        done = True

        if self.ligne0[nbr]%2==0 and self.colonne0[nbr]%2==0:
            done = False

        elif self.ligne0[nbr] == 0 or self.ligne0[nbr] == self.size*2 or self.colonne0[nbr] == 0 or self.colonne0[nbr] == self.size*2:
            done = False

        elif randint(0,1):
            if not self.casseH(nbr):
                if not self.casseV(nbr):
                    done = False

        else:
            if not self.casseV(nbr):
                if not self.casseH(nbr):
                    done = False

        self.ligne0 = np.delete(self.ligne0,nbr)
        self.colonne0 = np.delete(self.colonne0,nbr)

        return done


    def casseV(self, nbr):
        if signal.convolve2d(self.map, cmpV, mode="same")[self.ligne0[nbr],self.colonne0[nbr]]/2 != self.map[self.ligne0[nbr],self.colonne0[nbr]-1]:
            self.map[self.ligne0[nbr], self.colonne0[nbr]] = self.map[self.ligne0[nbr], self.colonne0[nbr]-1]
            self.map = np.where(self.map==self.map[self.ligne0[nbr], self.colonne0[nbr]+1], self.map[self.ligne0[nbr], self.colonne0[nbr]-1], self.map)
            return True

        else:
            return False


    def casseH(self,nbr):
        if signal.convolve2d(self.map, cmpH, mode="same")[self.ligne0[nbr],self.colonne0[nbr]]/2 != self.map[self.ligne0[nbr]-1,self.colonne0[nbr]]:
            self.map[self.ligne0[nbr], self.colonne0[nbr]] = self.map[self.ligne0[nbr]-1, self.colonne0[nbr]]
            self.map = np.where(self.map==self.map[self.ligne0[nbr]+1, self.colonne0[nbr]], self.map[self.ligne0[nbr]-1, self.colonne0[nbr]], self.map)
            return True
        else:
            return False


    def estFini(self):
        nb0 = len(np.where(self.map == -1))
        nbNb = len(np.where(self.map == self.map[1,1]))
        return (nb0+nbNb == (self.size+2)*2)


    def genPlein(self):
        self.initAffichage()
        self.genEtape()
    
    
    def genEtape(self):
        while not self.estFini() and self.ligne0.size!=0:
            if self.cassage():
                self.updateAffichage()
                self.Fenetre.update()
                #self.Fenetre.after(1, self.genEtape())
        self.Fenetre.mainloop()
                
        


#===================================================#


map1 = Maze(size)
#map1.getFenetre().mainloop()

"""


#map1[map==map[1,0]] = 0



plt.imshow(map1.getMap())
plt.show()

print(map1)
"""