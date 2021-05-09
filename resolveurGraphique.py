import numpy as np
from matplotlib import pyplot as plt
import os
from colour import Color
fullpath = os.path.abspath(__file__)
os.chdir(os.path.dirname(fullpath))
from generateurGraphique import Maze

size = 25
compteur = 1
var2 = True

map2 = Maze(size)
map2.setCase(size*2-1, size*2, 1)

#Initialise code couleur pour dégradé et jaune pour le path
color0 = map2.getColorCode()[0]
colorD = "#" + color0[3:5] + color0[1:3] + color0[5:7]
colorF = "#" + color0[5:7] + color0[1:3] + color0[3:5]

#Dégradé de la couleur en 1,1 jusqu'à la couleur opposée
colorCodeSolver = list(Color(colorD).range_to(Color(colorF),
                        size*10))
colorCodeSolver = [i.hex for i in colorCodeSolver]
colorCodeSolver = {i+1:colorCodeSolver[i] for i in range(len(colorCodeSolver))}
colorCodeSolver[-2] = "#ffff00"   #Jaune du path
colorCodeSolver[-1] = "#000000"   #Noir des murs
colorCodeSolver[0] = map2.getColorCode()[0]

map2.setColorCode(colorCodeSolver)

while len(map2.get0()[0]) != 0:
    #Tant qu'il reste des 0 sur la map (donc toute la map a pas été parcourue par le solveur), on continue
    temp = np.copy(map2.getMap())
    compteur += 1

    for i in range(size*2+1):
        for j in range(size*2+1):
            if map2.getMap()[i,j] == 0:
                if map2.getMap()[i-1,j]>0 or map2.getMap()[i+1,j]>0 or map2.getMap()[i,j-1]>0 or map2.getMap()[i,j+1]>0:
                    temp[i,j] = compteur
                    map2.updateAffichage()
    map2.setMap(np.copy(temp))


map2.updateAffichage() #Dernière update nécessaire

posX = 1
posY = 0

compteur2 = map2.getMap()[1,0]
map2.setCase(posX, posY, -2)

print("Distance entre le début et la fin : " + str(compteur2))

while map2.getMap()[size*2-1, size*2] != -2:
    #Tant que la fin c'est pas un -2 (pour le path de fin), on teste les cases autour
    #on leur met -2 et on décrémente le compteur pour comparer
    if map2.getMap()[posX-1, posY] == compteur2-1:
        map2.setCase(posX-1, posY, -2)
        posX -= 1
    elif map2.getMap()[posX+1, posY] == compteur2-1:
        map2.setCase(posX+1, posY, -2)
        posX += 1
    elif map2.getMap()[posX, posY-1] == compteur2-1:
        map2.setCase(posX, posY-1, -2)
        posY -= 1
    elif map2.getMap()[posX, posY+1] == compteur2-1:
        map2.setCase(posX, posY+1, -2)
        posY += 1
    compteur2-=1
    map2.updateAffichage()

map2.fenetreMainloop()
