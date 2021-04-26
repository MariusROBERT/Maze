import numpy as np
from random import *
from scipy import signal
import time
from matplotlib import pyplot as plt

size = 20

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
        
        self.genPlein()

        self.map[self.map==self.map[1,0]] = 0

    def getMap(self):
        return self.map

    def setMap(self, map):
        self.map = map

    def setCase(self, x, y, value):
        self.map[x, y] = value

    def get0(self):
        return np.where(self.map==0)

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
        #global map
        if signal.convolve2d(self.map, cmpV, mode="same")[self.ligne0[nbr],self.colonne0[nbr]]/2 != self.map[self.ligne0[nbr],self.colonne0[nbr]-1]:
            self.map[self.ligne0[nbr], self.colonne0[nbr]] = self.map[self.ligne0[nbr], self.colonne0[nbr]-1]
            self.map = np.where(self.map==self.map[self.ligne0[nbr], self.colonne0[nbr]+1], self.map[self.ligne0[nbr], self.colonne0[nbr]-1], self.map)
            return True

        else:
            return False


    def casseH(self,nbr):
        #global map
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
        debut = time.time()
        while not self.estFini() and self.ligne0.size!=0:
            if self.cassage():
                pass
        print("Labyrinthe généré en {}s".format(time.time() - debut)) 
        #return map


#===================================================#
"""
map1 = Maze(size)


#map1[map==map[1,0]] = 0



plt.imshow(map1.getMap())
plt.show()

print(map1)
"""