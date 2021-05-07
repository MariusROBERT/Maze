import numpy as np
from random import *
from scipy import signal
from tkinter import *

size = 100

cmpV = np.ones((1,3))
cmpV[0,1] = 0
cmpH = np.ones((3,1))
cmpH[1,0] = 0



class Maze():
    def __init__(self, size):
        self.size = size
    
        #Génère map avec des nombres différents sur chaque case
        self.map = np.arange(0,(self.size*2+1)**2)
        self.map = self.map.reshape(self.size*2+1,self.size*2+1)

        self.map[::2] = -1
        self.map[::,::2] = -1

        #Entrée et Sortie
        self.map[1,1] = 0
        self.map[1,0] = self.map[1,1]
        self.map[self.size*2-1, self.size*2] = self.map[self.size*2-1,self.size*2-1]

        #Trouve tout les murs
        self.ligne0, self.colonne0 = np.where(self.map == -1)

        #Fenêtre
        self.Fenetre = Tk()
        self.Fenetre.title("Maze Generator by Marius")

        self.frameJeu = Frame(self.Fenetre)
        self.frameJeu.grid(row = 1, column = 1, sticky = "news")

        self.grilleJeu = Canvas(self.frameJeu, background="light grey")

        self.grilleJeu.pack()

        self.mapAffichage = dict()  
        #Dictionnaire pour stocker cases graphiques avec leur x, y
        self.colorCode = dict()
        self.colorCode[-1] = "black"
        for i in range((self.size*2+1)**2):
            self.colorCode[i] = "#"+"%06x"%randint(0, 0xFFFFFF)
        while self.colorCode[0] == "#ffff00":
            #Évite le jaune pur pour le garder pour le solveur 
            self.colorCode[i] = "#"+"%06x"%randint(0, 0xFFFFFF)
        
        self.genPlein()
        #self.map[self.map==self.map[1,0]] = 0


    def initAffichage(self):
        #Crée grille de base avec couleur
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
        #Check chaque case et met sa couleur à jour (à optimiser pour changer que les cases qui changent)
        for x in range(self.size*2+1):
            for y in range(self.size*2+1):
                self.grilleJeu.itemconfig(self.grilleJeu.find_withtag(self.mapAffichage[(x, y)])[0], fill=self.colorCode[self.map[x, y]])          
        self.Fenetre.update()

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
        #Essaye de casser un mur 
        nbr = randint(0,len(self.ligne0)-1)
        done = True

        if self.ligne0[nbr]%2==0 and self.colonne0[nbr]%2==0:
            #Si les 2 sont des multiples de 2, c'est un mur dans un croisement donc pas à casser
            done = False

        elif self.ligne0[nbr] == 0 or self.ligne0[nbr] == self.size*2 or self.colonne0[nbr] == 0 or self.colonne0[nbr] == self.size*2:
            #Si on est au bord, on peut pas casser
            done = False

        elif randint(0,1):
            #1 chance sur 2 : tente de casser un mur horizontale, si ça marche pas on fait verticale
            if not self.casseH(nbr):
                if not self.casseV(nbr):
                    done = False

        else:
            #1 chance sur 2 : tente de casser un mur vertical, si ça marche pas on fait horizontale
            if not self.casseV(nbr):
                if not self.casseH(nbr):
                    done = False

        #Supprime le mur qu'on vient de tester/supprimer de la liste des murs
        self.ligne0 = np.delete(self.ligne0,nbr)
        self.colonne0 = np.delete(self.colonne0,nbr)

        return done


    def casseV(self, nbr):
        #Additionne puis prend la moitié des 2 nombres de chaque côté du mur et on compare à la case de gauche, si c'est différent on casse le mur
        if signal.convolve2d(self.map, cmpV, mode="same")[self.ligne0[nbr],self.colonne0[nbr]]/2 != self.map[self.ligne0[nbr],self.colonne0[nbr]-1]:
            self.map[self.ligne0[nbr], self.colonne0[nbr]] = self.map[self.ligne0[nbr], self.colonne0[nbr]-1]
            self.map = np.where(self.map==self.map[self.ligne0[nbr], self.colonne0[nbr]+1], self.map[self.ligne0[nbr], self.colonne0[nbr]-1], self.map)
            return True
        else:
            return False


    def casseH(self,nbr):
        #Additionne puis prend la moitié des 2 nombres de chaque côté du mur et on compare à la case du dessus, si c'est différent on casse le mur
        if signal.convolve2d(self.map, cmpH, mode="same")[self.ligne0[nbr],self.colonne0[nbr]]/2 != self.map[self.ligne0[nbr]-1,self.colonne0[nbr]]:
            self.map[self.ligne0[nbr], self.colonne0[nbr]] = self.map[self.ligne0[nbr]-1, self.colonne0[nbr]]
            self.map = np.where(self.map==self.map[self.ligne0[nbr]+1, self.colonne0[nbr]], self.map[self.ligne0[nbr]-1, self.colonne0[nbr]], self.map)
            return True
        else:
            return False


    def estFini(self):
        #Si y'a que des -1 et des 0, c'est fini
        nb0 = len(np.where(self.map == -1))
        nbNb = len(np.where(self.map == self.map[1,1]))
        return (nb0+nbNb == (self.size+2)*2)


    def genPlein(self):
        #Initialise la fenêtre puis lance la boucle des étapes
        self.initAffichage()
        self.genEtape()
    
    
    def genEtape(self):
        #Tant que le labyrinthe est pas fini, on casse un mur
        while not self.estFini() and self.ligne0.size!=0:
            if self.cassage():
                #Si un mur a été cassé, on update l'affichage
                self.updateAffichage()
        self.Fenetre.mainloop()              
        


#===================================================#


map1 = Maze(size)
