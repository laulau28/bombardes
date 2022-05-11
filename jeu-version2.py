# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 21:28:36 2022

@authors: Alexia, Laure
"""

from tkinter import *
from math import cos, sin, pi

class canon:
    #objet canon avec plusieurs proprietes quon peut faire varier entre le 1er et le 2e canon
    def __init__(self, canv, x, y, angle, coul_int, coul_bord, x_min, x_max, angle_min, angle_max, dir):
        self.canv = canv            # canevas
        self.appli = canv.master    # fenêtre d'application 
# self.id = id                # identifiant du canon (finalement jai plus besoin de la ligne mais je la laisse au cas ou)
        self.angle = angle          # angle de tir
        self.coul_int = coul_int    # couleur associée au dedans du canon
        self.coul_bord = coul_bord  # couleur associée au bord du canon
        self.x, self.y = x, y       # centre du canon
        self.x_min = x_min          # extremite de gauche de l ilot
        self.x_max = x_max          # extremite de droite de l ilot
        self.angle_min = angle_min  # angle minimal du tube
        self.angle_max = angle_max  # angle maximal du tube
        self.dir = dir              # direction dans laquelle pointe le tube (vers la gauche ou vers la droite)

        self.rc = 15                # rayon de la base du canon (pas besoin de le donner en entree a l objet canon, car il est le meme pour les deux canons)
        self.ro = 4                 # rayon de l obus (pareil, cest le meme pour tous les obus)
        self.vitesse = 90           # vitesse initiale de l obus
        self.dt = .2                # intervalle de temps pour la trajectoire
        self.vx = 10                # vitesse horizontale initiale
        self.vy = 0                 # vitesse verticale initiale
        self.obus_x = -10           # coord x centre obus
        self.obus_y = -10           # coord y centre obus
        self.obus_en_vol = False    # test s il y a deja un obus en vol


        #on definit la base (disque noir) et le tube (ligne noire epaisse) du canon        
        self.tube = canv.create_line(x, y, x + dir*2*self.rc*cos(angle), y - 2*self.rc*sin(angle), width = 10)
        self.base = canv.create_oval(x -self.rc, y -self.rc, x +self.rc, y +self.rc, fill =coul_int, outline=coul_bord)
        
        #on cree l obus qu on cache hors de la fenetre de jeu tant qu on ne le lance pas
        self.obus = canv.create_oval(self.obus_x-self.ro, self.obus_y-self.ro, self.obus_x+self.ro, self.obus_y+self.ro, fill = "black")
        
    def tir(self,event=None):
    #fonction qui initialise le tir (met l obus en bonne position avant le deplacement)
        if self.obus_en_vol == False:
            self.obus_en_vol = True
            self.obus_x = self.x + self.dir*2*self.rc*cos(self.angle) 
            self.obus_y = self.y - 2*self.rc*sin(self.angle)
            self.vx = self.vitesse * cos(self.angle)
            self.vy = -self.vitesse * sin(self.angle)
            self.canv.coords(self.obus, self.obus_x-self.ro, self.obus_y-self.ro, self.obus_x+self.ro, self.obus_y+self.ro)
            self.canv.after(50, self.deplace_obus)
        
    def deplace_obus(self,event=None):
    #fonction du deplacement de l obus
        self.obus_x = self.obus_x + self.dir*self.vx*self.dt 
        self.obus_y = self.obus_y + self.vy*self.dt
        if self.obus_x > w or self.obus_x < 0:
            self.obus_en_vol = False
            self.canv.coords(self.obus, -10-self.ro, -10-self.ro, -10+self.ro, -10+self.ro)
        elif self.obus_y > 3*h//4:
            if self.obus_x < w//3 or self.obus_x > 2*w//3:
                self.obus_en_vol = False
                self.canv.coords(self.obus, -10-self.ro, -10-self.ro, -10+self.ro, -10+self.ro)
            elif self.obus_y > 7*h//8:
                self.obus_en_vol = False
                self.canv.coords(self.obus, -10-self.ro, -10-self.ro, -10+self.ro, -10+self.ro)
            else :
                self.vy = self.vy + 9.81*self.dt
                self.canv.coords(self.obus, self.obus_x-self.ro, self.obus_y-self.ro, self.obus_x+self.ro, self.obus_y+self.ro)
                self.canv.after(40, self.deplace_obus)
        else :
            self.vy = self.vy + 9.81*self.dt
            self.canv.coords(self.obus, self.obus_x-self.ro, self.obus_y-self.ro, self.obus_x+self.ro, self.obus_y+self.ro)
            self.canv.after(40, self.deplace_obus)
        
    def left(self,event=None):
    #fonction qui deplace vers la gauche le disque
        if self.x > self.x_min:     #on teste que l objet ne sort pas de l ecran
            self.canv.move(self.tube, -10, 0)      #on deplace le tube
            self.canv.move(self.base, -10, 0)      #on deplace la base
            self.x = self.x-10      #on definit la nouvelle position
            
    def right(self,event=None):
    #fonction qui deplace vers la droite le disque
        if self.x < self.x_max:     #on teste que l objet ne sort pas de l ecran
            self.canv.move(self.tube, 10, 0)      #on deplace le tube
            self.canv.move(self.base, 10, 0)      #on deplace la base
            self.x = self.x+10      #on definit la nouvelle position

    def up(self,event=None):
    #fonction qui tourne le tube vers le haut
        self.angle = self.angle + pi/30      #on definit le nouvel angle
        if self.angle > self.angle_max:     #on teste que le tube ne tourne pas trop loin
            self.angle = self.angle_max
        self.canv.coords(self.tube, self.x, self.y, self.x + self.dir*2*self.rc*cos(self.angle), self.y - 2*self.rc*sin(self.angle)) #on tourne le tube
            
    def down(self,event=None):
    #fonction qui deplace vers la gauche le disque
        self.angle = self.angle - pi/30      #on definit la nouvelle position
        if self.angle < self.angle_min:     #on teste que l objet ne sort pas de l ecran
            self.angle = self.angle_min
        self.canv.coords(self.tube, self.x, self.y, self.x + self.dir*2*self.rc*cos(self.angle), self.y - 2*self.rc*sin(self.angle))      #on deplace le tube


w = 1200
h = 800
x_cg = w//6 #coord x centre canon de gauche
y_cg = 3*h//4-15 #coord y centre canon de gauche
x_cd = 5*w//6 #coord x centre canon de droite
y_cd = 3*h//4-15 #coord y centre canon de droite

class Application(Frame):
    #appli principale (canvas, objets, touches, etc)
    def __init__(self):
        Frame.__init__(self)
        self.master.title('Jeu des bombardes') #titre
        self.pack() #VOIR DOCUMENTATION (utilisé dans les codes sur internet)
        self.jeu = Canvas(self, width =w, height =h, bg ='lightskyblue') #surface du jeu

        #creation des ilots et de l eau
        self.jeu.create_rectangle(1,3*h//4+1,w//3+1,h+1,fill="gold",outline="gold")
        self.jeu.create_rectangle(2*w//3+1,3*h//4+1,w+1,h+1,fill="gold",outline="gold")
        self.jeu.create_rectangle(w//3+2,7*h//8,2*w//3,h+1,fill="cornflowerblue",outline="cornflowerblue")
        
        self.jeu.pack(padx =15, pady =15, side =TOP)  #bordure de la fenetre de jeu
        self.jeu.focus_set()  #VOIR DOCUMENTATION ??

        #creation des deux canons
        self.j1 = canon(self.jeu, x_cg, y_cg, 0, "red", "black",20,w//3-20, 0, pi/2, 1)
        self.j2 = canon(self.jeu, x_cd, y_cd, 0, "green2", "black",2*w//3+20,w-20, 0, pi/2, -1)
        
        #attribution des touches
        self.jeu.bind('<Left>', self.j2.left)  #touche fleche vers la gauche
        self.jeu.bind('<a>', self.j1.left)     #touche "A" du clavier 
        self.jeu.bind('<Right>', self.j2.right)
        self.jeu.bind('<d>', self.j1.right)
        self.jeu.bind('<Up>', self.j2.up)
        self.jeu.bind('<w>', self.j1.up)
        self.jeu.bind('<Down>', self.j2.down)
        self.jeu.bind('<s>', self.j1.down)
        self.jeu.bind('<0>', self.j2.tir)      #touche 0 du pavé numérique
        self.jeu.bind('<x>', self.j1.tir)

if __name__ =='__main__':
    Application().mainloop()