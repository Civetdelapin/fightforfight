# -*- coding:Utf-8 -*-
#ligne permettant l'utilisateur des accents

#importation de pygame
import pygame
from pygame.locals import *
#importation de la bibliothèque system
import sys
import os
#importation du mixer pour gérer la musique
import pygame.mixer

from data_map import *

class Game():
    # Constructeur, self correspond +- au 'this'
    def __init__(self,fenetre,nb_player,controlers,folderTextureP):


        self.fenetre=fenetre
        self.map = Map(2)  #param level
        self.nb_player=nb_player
        self.players= []
        self.folderTexture=folderTextureP

        #création du plateau
        self.createGameBoard()

        #affection des mannettes
        self.controlers=controlers
        for i in  range (0,self.nb_player):
            entity = pygame.image.load("./image/player/1/player_S.png").convert_alpha()
            speed = [2, 2]
            player = Player(entity,entity.get_rect(),speed,controlers[i])
            self.players.append(player);
            self.fenetre.blit(self.players[i].entity,(0,0))
    # Retourne la grid
    def get_grid(self):
        return self.grid

    def affectElement(self,x,y,damage):
        self.grid[x][y].hp-damage


    def createGameBoard(self):
        self.fond_e = pygame.image.load("./image/blocks/"+self.folderTexture+"/"+"fond.png").convert()
        self.fenetre.blit(self.fond_e, (0,0))
        grid = self.map.get_grid()

        for i in range (0,len(self.map.get_grid())):
            grid[i].image = pygame.image.load("./image/blocks/"+self.folderTexture+"/"+grid[i].get_image()).convert()
            self.fenetre.blit(grid[i].image, (grid[i].pos_y,grid[i].pos_x))
    def movementGame(self):
        self.refreshGame()
        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.players[i].mouvement()
            self.players[i].movement_arrow()

    def refreshGame(self):
        #refresh fond
        self.fenetre.blit(self.fond_e, (0,0))

        #refresh block
        grid = self.map.get_grid()
        for i in range (0,len(self.map.get_grid())):
            self.fenetre.blit(grid[i].image, (grid[i].pos_y,grid[i].pos_x))


        for i in range (0,len(self.players)):
            for n in range (0,len(self.players)):
                if n!=i:
                    for a in range (0,len(self.players[n].arrows_launched)):
                        if self.players[i].isHited(self.players[n].arrows_launched[a]):
                            self.players[n].arrows_launched[a].effect(self.players[i])
                            del self.players[n].arrows_launched[a]

        for i in range (0,len(self.players)):
            print(self.players[i].hp<=0)
            if self.players[i].hp<=0:
                self.players[i].isAlive=False

        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.fenetre.blit(self.players[i].entity, self.players[i].entity_coord)
            for j in range(0, len(self.players[i].arrows_launched)):
                self.fenetre.blit(self.players[i].arrows_launched[j].entity,(self.players[i].arrows_launched[j].entity_coord.centerx-16,self.players[i].arrows_launched[j].entity_coord.centery-16))


######################################################################################################################################################################################################

class Player():
    def __init__(self,entity_temp,entity_coord_temp,speed,controler):
        self.entity=entity_temp
        self.entity_coord=entity_coord_temp
        self.level=1
        self.exp=0
        self.hp=100
        self.speed=speed
        self.controler=controler
        self.isAlive=True
        self.arrows_launched = []
        self.can_shoot = True
        self.combo_inc = []
        self.combo_add = True
        self.isDashing = False
        self.direction_dash ="N"
        self.speed_dash = [30,30]
        self.speed_dash_diagonale = [20,20]
        self.canDash = True
        self.debutDash=-1

    def mouvement(self):
        if self.isDashing and (pygame.time.get_ticks()-self.debutDash)<50:
            self.movement_dash()
        else:
            self.isDashing=False
            self.movement_coord()
        self.movement_sight()
        self.button_pressed()

    def movement_coord(self) :
        if (self.controler.get_axis( 2 ) < 0.600) and (pygame.time.get_ticks()-self.debutDash)>2000:
            self.canDash=True

        if self.controler.get_axis( 1 ) < -0.350 and self.entity_coord.top>0 and self.controler.get_axis( 0 ) > 0.350 and self.entity_coord.right<950:
            speedHero = [2, 2]
            self.entity_coord = self.entity_coord.move(speedHero[0], -speedHero[0])
            self.dash("NE")
        elif self.controler.get_axis( 1 ) < -0.350 and self.entity_coord.top>0 and self.controler.get_axis( 0 )< -0.350 and self.entity_coord.left>0:
            speedHero = [2, 2]
            self.entity_coord = self.entity_coord.move(-speedHero[0], -speedHero[0])
            self.dash("NW")
        elif self.controler.get_axis( 1 ) > 0.350 and self.entity_coord.bottom<530 and self.controler.get_axis( 0 ) > 0.350 and self.entity_coord.right<950:
            speedHero = [2, 2]
            self.entity_coord = self.entity_coord.move(speedHero[0], speedHero[0])
            self.dash("SE")
        elif self.controler.get_axis( 1 ) > 0.350 and self.entity_coord.bottom<530 and self.controler.get_axis( 0 )< -0.350 and self.entity_coord.left>0:
            speedHero = [2, 2]
            self.entity_coord = self.entity_coord.move(-speedHero[0], speedHero[0])
            self.dash("SW")
        elif self.controler.get_axis( 1 ) < -0.500 and self.entity_coord.top>0:
            speedHero = [3, 3]
            self.entity_coord = self.entity_coord.move(0, -speedHero[0])
            self.dash("N")
        elif self.controler.get_axis( 1 ) > 0.500 and self.entity_coord.bottom<950:
            speedHero = [3, 3]
            self.entity_coord = self.entity_coord.move(0, speedHero[0])
            self.dash("S")
        elif self.controler.get_axis( 0 ) > 0.500 and self.entity_coord.right<1000:
            speedHero = [3, 3]
            self.entity_coord = self.entity_coord.move(speedHero[0], 0)
            self.dash("E")
        elif self.controler.get_axis( 0 )< -0.500 and self.entity_coord.left>0:
            speedHero = [3, 3]
            self.entity_coord = self.entity_coord.move(-speedHero[0], 0)
            self.dash("W")

    def button_pressed(self):
        if(self.controler.get_button(0)==0 and self.controler.get_button(1)==0 and self.controler.get_button(2)==0 and self.controler.get_button(3)==0):
            self.combo_add=True
        if (self.combo_add):
            if(self.controler.get_button(0)==1):
                self.combo_inc.append("A")
                self.combo_add=False
            elif(self.controler.get_button(1)==1):
                self.combo_inc.append("B")
                self.combo_add=False
            elif(self.controler.get_button(2)==1):
                self.combo_inc.append("X")
                self.combo_add=False
            elif(self.controler.get_button(3)==1):
                self.combo_inc.append("Y")
                self.combo_add=False

    def movement_sight(self):
        center_aim=self.entity_coord.center

        if self.controler.get_axis( 4 ) < -0.500 and self.controler.get_axis( 3 ) > 0.500:
            center_aim=(self.entity_coord.centerx-20,self.entity_coord.centery+20)
            #self.entity=pygame.image.load("arrow.png").convert_alpha()
            self.shoot_arrow("SW")

        elif self.controler.get_axis( 4 ) < -0.500 and self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx-20,self.entity_coord.centery-20)
            self.shoot_arrow("NW")

        elif self.controler.get_axis( 4 ) > 0.500 and self.controler.get_axis( 3 ) > 0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery+20)
            self.shoot_arrow("SE")

        elif self.controler.get_axis( 4 ) > 0.500 and self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery-20)
            self.shoot_arrow("NE")

        elif self.controler.get_axis( 4 ) < -0.500:
            center_aim=(self.entity_coord.centerx-20,self.entity_coord.centery)
            self.shoot_arrow("W")

        elif self.controler.get_axis( 4 ) > 0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery)
            self.shoot_arrow("E")

        elif self.controler.get_axis( 3 ) > 0.500:
            center_aim=(self.entity_coord.centerx,self.entity_coord.centery+20)
            self.shoot_arrow("S")

        elif self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx,self.entity_coord.centery-20)
            self.shoot_arrow("N")

        #pygame.draw.circle(self.fenetre, (255,0,0), center_aim, 5, 1)

    def shoot_arrow(self,direction):

        if self.controler.get_axis( 2 ) < -0.700 and self.can_shoot:
            if direction== "N":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_N.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_N.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_N.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_N.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []
            elif direction== "S":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_S.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_S.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_S.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_S.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []
            elif direction== "W":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_W.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_W.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_W.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_W.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []
            elif direction== "E":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_E.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_E.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_E.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_E.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []

            elif direction== "NE":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_NE.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_NE.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_NE.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_NE.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []

            elif direction== "NW":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_NW.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_NW.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_NW.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_NW.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []

            elif direction== "SE":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_SE.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_SE.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_SE.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_SE.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []

            elif direction== "SW":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_SW.png").convert_alpha()
                elif(len(self.combo_inc)==3):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                        arrow_entity = pygame.image.load("./image/arrow/fire/arrow_fire_SW.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/ice/arrow_ice_SW.png").convert_alpha()
                    elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                        arrow_entity = pygame.image.load("./image/arrow/earth/arrow_earth_SW.png").convert_alpha()
                    else:
                        self.combo_inc = []
                else:
                    self.combo_inc = []
                #arrow_entity = pygame.transform.scale(arrow_entity,(64,64))
            if (len(self.combo_inc)==2 or len(self.combo_inc)==3):

                arrow = Arrow(arrow_entity,self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                self.arrows_launched.append(arrow)
                self.can_shoot = False
            self.combo_inc = []
        if self.controler.get_axis( 2 ) > -0.200 and self.controler.get_axis( 2 )!= 0.0:
            self.can_shoot = True

    def movement_arrow(self):
        for i in self.arrows_launched:
            i.movement()

    def isHited(self,arrow):
        if arrow.direction== "N":
            x=arrow.entity_coord.centerx
            y=arrow.entity_coord.top
        elif arrow.direction== "S":
            x=arrow.entity_coord.centerx
            y=arrow.entity_coord.bottom
        elif arrow.direction== "W":
            x=arrow.entity_coord.left
            y=arrow.entity_coord.centery
        elif arrow.direction== "E":
            x=arrow.entity_coord.right
            y=arrow.entity_coord.centery
        elif arrow.direction== "NE":
            x=arrow.entity_coord.right
            y=arrow.entity_coord.top
        elif arrow.direction== "NW":
            x=arrow.entity_coord.left
            y=arrow.entity_coord.top
        elif arrow.direction== "SE":
            x=arrow.entity_coord.bottom
            y=arrow.entity_coord.right
        elif arrow.direction== "SW":
            x=arrow.entity_coord.bottom
            y=arrow.entity_coord.left

        if abs(x-self.entity_coord.centerx)<48 and abs(y-self.entity_coord.centery)<48:
            return True
        else:
            return False

    def dash(self,direction):
        if self.controler.get_axis( 2 ) > 0.700 and self.canDash:
            self.debutDash=pygame.time.get_ticks()
            self.isDashing = True
            self.canDash=False
            self.direction_dash = direction

    def movement_dash(self):
        if self.direction_dash== "N":
            self.entity_coord = self.entity_coord.move(0, -self.speed_dash[0])
        elif self.direction_dash== "S":
            self.entity_coord = self.entity_coord.move(0, self.speed_dash[0])
        elif self.direction_dash== "W":
            self.entity_coord = self.entity_coord.move(-self.speed_dash[0], 0)
        elif self.direction_dash== "E":
            self.entity_coord = self.entity_coord.move(self.speed_dash[0], 0)
        elif self.direction_dash== "NE":
            self.entity_coord = self.entity_coord.move(self.speed_dash_diagonale[0], -self.speed_dash_diagonale[0])
        elif self.direction_dash== "NW":
            self.entity_coord = self.entity_coord.move(-self.speed_dash_diagonale[0], -self.speed_dash_diagonale[0])
        elif self.direction_dash== "SE":
            self.entity_coord = self.entity_coord.move(self.speed_dash_diagonale[0], self.speed_dash_diagonale[0])
        elif self.direction_dash== "SW":
            self.entity_coord = self.entity_coord.move(-self.speed_dash_diagonale[0], self.speed_dash_diagonale[0])

######################################################################################################################################################################################################

class Arrow():
    def __init__(self,entity_temp,entity_coord_temp,direction):
        self.damage=40
        self.entity=entity_temp
        self.entity_coord=entity_coord_temp
        self.speed=(6,6)
        self.speed_diagonale=(4,4)
        self.direction=direction

    def movement(self):
        if self.direction== "N":
            self.entity_coord = self.entity_coord.move(0, -self.speed[0])
        elif self.direction== "S":
            self.entity_coord = self.entity_coord.move(0, self.speed[0])
        elif self.direction== "W":
            self.entity_coord = self.entity_coord.move(-self.speed[0], 0)
        elif self.direction== "E":
            self.entity_coord = self.entity_coord.move(self.speed[0], 0)
        elif self.direction== "NE":
            self.entity_coord = self.entity_coord.move(self.speed_diagonale[0], -self.speed_diagonale[0])
        elif self.direction== "NW":
            self.entity_coord = self.entity_coord.move(-self.speed_diagonale[0], -self.speed_diagonale[0])
        elif self.direction== "SE":
            self.entity_coord = self.entity_coord.move(self.speed_diagonale[0], self.speed_diagonale[0])
        elif self.direction== "SW":
            self.entity_coord = self.entity_coord.move(-self.speed_diagonale[0], self.speed_diagonale[0])

    def effect(self, player):
        player.hp=player.hp-self.damage

######################################################################################################################################################################################################


class Arrow_fire(Arrow):
    def __init__(self,entity_temp,entity_coord_temp,direction):
        Arrow.__init__(entity_temp,entity_coord_temp,direction)

######################################################################################################################################################################################################

class Arrow_ice(Arrow):
    def __init__(self,entity_temp,entity_coord_temp,direction):
        Arrow.__init__(entity_temp,entity_coord_temp,direction)

    def effect(self, player):
        Arrow.effect(player)


######################################################################################################################################################################################################


class Map():
    # Constructeur, self correspond +- au 'this'
    def __init__(self,levelP):

        # Initialisation et affectation de l'attribut grid
        #coordonnée X Y typeBlock()   hitbox
        # 1 : blockIndestructible
        # 2 : blockDestructible
        # 3 : passThrough

        self.map_grid_elem=[]
        self.level= levelP

        #parcours de la map_grid du fichier
        for i in range(0, 12):
            for j in range(0, 20):
                #unbreak 	0
                #void		1
                #breakGood	2
                #breakBad	3
                #breakRelBad	4
                #through	5

                #appel constructeur de chaque block
                if map_grid_AllList[self.get_Level()][i][j] == 0:
                    self.map_grid_elem.append(Element(i*64,j*64,1,"stoneUnbreak.png"))
                elif map_grid_AllList[self.get_Level()][i][j] == 2:
                    self.map_grid_elem.append(ElementDestructible(i*64,j*64,3,1))
                elif map_grid_AllList[self.get_Level()][i][j] == 3:
                    self.map_grid_elem.append(ElementDestructible(i*64,j*64,2,1))
                elif map_grid_AllList[self.get_Level()][i][j] == 4:
                    self.map_grid_elem.append(ElementDestructible(i*64,j*64,1,1))
                elif map_grid_AllList[self.get_Level()][i][j] == 5:
                    self.map_grid_elem.append(ElementPassThrough(i*64,j*64,1,"goThrough.png"))


    # Retourne la grid
    def get_grid(self):
        return self.map_grid_elem

    # Retourne le next level
    def get_Level(self):
        return self.level

######################################################################################################################################################################################################

class Element():
    def __init__(self,x,y,hitBox,image):
        self.pos_x = x
        self.pos_y = y
        self.hitBox = hitBox
        self.image  = image

    def get_image(self):
        return self.image

######################################################################################################################################################################################################

class ElementDestructible(Element):
    def __init__(self,x,y,stateP,hitBox):
        Element.__init__(self,x,y,hitBox,"default.png")
        self.state = stateP  #HP

    def get_state(self):
            return self.state

    def arrowHitDest(self):
        if self.state>0:
                    self.state = self.state-1

    def get_image(self):
            if self.state>=3 :
                return "break_0.png"
            elif self.state == 2:
                return "break_1.png"
            elif self.state == 1:
                return "break_2.png"
            else:
                return "default.png"   #impossible

######################################################################################################################################################################################################

class ElementPassThrough(Element):
    def __init__(self,x,y,hitBox,image):
        Element.__init__(self,x,y,hitBox,image)




class TexturesListCheck():
    def __init__(self):
        self.texturesFolderBlock = ""
        self.listOfTextures = [ ["break_1.png","break_2.png","break_3.png","default.png","fond.png","goThrough.png","stoneUnbreak.png"],
                                ["_E.png","_N.png","_NE.png","_NW.png","_S.png","_SE.png","_SW.png","_W.png"]
                              ]
        self.ListMissingTexture =[]

    def checkExistBlock(self):
        path = ["./image/blocks","./image/arrow","./image/player"]

        #textures des blocks
        self.texturesFolderBlock=  next(os.walk(path[0]))[1]

        for folder in self.texturesFolderBlock:
            for fileTexture in self.listOfTextures[0]: #list of blocs
                if not os.path.exists(path[0]+"/"+folder+"/"+fileTexture): #path[0]
                    self.ListMissingTexture.append(folder+"/"+fileTexture)




        #textures des arrows
        subfolder = next(os.walk(path[1]))[1] #arrows/ice fire ...

        for folder in subfolder:
            for fileTexture in self.listOfTextures[1]: #list of arrow
                if not os.path.exists(path[1]+"/"+folder+"/arrow_"+folder+fileTexture): #path[1]
                    self.ListMissingTexture.append(folder+"/arrow_"+folder+fileTexture)

        #textures des players
        subfolder = next(os.walk(path[2]))[1] #player 1 2 3 4

        for folder in subfolder:
            for fileTexture in self.listOfTextures[1]: #list of player
                if not os.path.exists(path[2]+"/"+folder+"/player"+fileTexture): #path[1]
                    self.ListMissingTexture.append(folder+"/player"+fileTexture)

        return len(self.ListMissingTexture)

    #get la liste des textures des blocks
    def get_TexturesFolderBlock(self):
        return self.texturesFolderBlock

    #get la liste des textures manquante
    def get_TexturesFolder(self):
        return self.ListMissingTexture
