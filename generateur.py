import numpy as np
from random import *
from scipy import signal
import time
from matplotlib import pyplot as plt

size = 20
map = np.arange(0,(size*2+1)**2)
map = map.reshape(size*2+1,size*2+1)

cmpV = np.ones((1,3))
cmpV[0,1] = 0
cmpH = np.ones((3,1))
cmpH[1,0] = 0

map[::2] = -1
map[::,::2] = -1

map[1,0] = map[1,1]
map[size*2-1, size*2] = map[size*2-1,size*2-1]


ligne0, colonne0 = np.where(map == -1)


def cassage(map):
    global ligne0, colonne0
    nbr = randint(0,len(ligne0)-1)
    done = True

    if ligne0[nbr]%2==0 and colonne0[nbr]%2==0:
        done = False

    elif ligne0[nbr] == 0 or ligne0[nbr] == size*2 or colonne0[nbr] == 0 or colonne0[nbr] == size*2:
        done = False

    elif randint(0,1):
        if not casseH(nbr):
            if not casseV(nbr):
                done = False

    else:
        if not casseV(nbr):
            if not casseH(nbr):
                done = False

    ligne0 = np.delete(ligne0,nbr)
    colonne0 = np.delete(colonne0,nbr)

    return done


def casseV(nbr):
    global map
    if signal.convolve2d(map, cmpV, mode="same")[ligne0[nbr],colonne0[nbr]]/2 != map[ligne0[nbr],colonne0[nbr]-1]:
        map[ligne0[nbr], colonne0[nbr]] = map[ligne0[nbr], colonne0[nbr]-1]
        map = np.where(map==map[ligne0[nbr], colonne0[nbr]+1], map[ligne0[nbr], colonne0[nbr]-1], map)
        return True

    else:
        return False



def casseH(nbr):
    global map
    if signal.convolve2d(map, cmpH, mode="same")[ligne0[nbr],colonne0[nbr]]/2 != map[ligne0[nbr]-1,colonne0[nbr]]:
        map[ligne0[nbr], colonne0[nbr]] = map[ligne0[nbr]-1, colonne0[nbr]]
        map = np.where(map==map[ligne0[nbr]+1, colonne0[nbr]], map[ligne0[nbr]-1, colonne0[nbr]], map)
        return True
    else:
        return False



def estFini(map):
    nb0 = len(np.where(map == -1))
    nbNb = len(np.where(map == map[1,1]))
    return (nb0+nbNb == (size+2)*2)


img = plt.imshow(map)

debut = time.time()

while not estFini(map) and ligne0.size!=0:
    if cassage(map):
        img.set_data(map)

print(time.time() - debut)

map[map==map[1,0]] = 0

plt.imshow(map)
plt.show()

print(map)