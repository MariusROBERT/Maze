import numpy as np
import time
from matplotlib import pyplot as plt
import os
fullpath = os.path.abspath(__file__)
os.chdir(os.path.dirname(fullpath))
from generateur2 import Maze

size = 25
compteur = 1
var2 = True

map2 = Maze(size)
map2.setCase(size*2-1, size*2, 1)

debut = time.time()
while len(map2.get0()[0]) != 0:
    temp = np.copy(map2.getMap())
    compteur += 1

    for i in range(size*2):
        for j in range(size*2):
            if map2.getMap()[i,j] == 0:
                if map2.getMap()[i-1,j]>0 or map2.getMap()[i+1,j]>0 or map2.getMap()[i,j-1]>0 or map2.getMap()[i,j+1]>0:
                    temp[i,j] = compteur

    map2.setMap(np.copy(temp))

print("Calcul des chemins généré en {}s".format(time.time() - debut)) 
compteur2 = map2.getMap()[1,0]

plt.imshow(map2.getMap())
plt.show()

posX = 1
posY = 0

map2.setCase(posX, posY, size*10)

debut = time.time()

print("Distance entre le début et la fin : " + str(compteur2))

while map2.getMap()[size*2-1, size*2] != size*10:
    if map2.getMap()[posX-1, posY] == compteur2-1:
        map2.setCase(posX-1, posY, size*10)
        posX -= 1
    elif map2.getMap()[posX+1, posY] == compteur2-1:
        map2.setCase(posX+1, posY, size*10)
        posX += 1
    elif map2.getMap()[posX, posY-1] == compteur2-1:
        map2.setCase(posX, posY-1, size*10)
        posY -= 1
    elif map2.getMap()[posX, posY+1] == compteur2-1:
        map2.setCase(posX, posY+1, size*10)
        posY += 1
    compteur2-=1
    
print("Calcul du meilleur chemin généré en {}s".format(time.time() - debut)) 

plt.imshow(map2.getMap())
plt.show()