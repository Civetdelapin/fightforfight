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
from math import sqrt
from data_map import *

class Game():
    # Constructeur, self correspond +- au 'this'
    def __init__(self,fenetre,nb_player,controlers,folderTextureP):
        self.fenetre=fenetre
        self.map = Map(folderTextureP,0)
        self.nb_player=nb_player
        self.players= []
        
        #création du plateau
        self.createGameBoard()

        #affection des mannettes
        self.controlers=controlers

        #création des joueurs
        for i in  range (0,self.nb_player):
            
            speed = [3, 3]
            speed_diagonale= [2,2]
            player = Player(speed,controlers[i],str(i+1),speed_diagonale)
            self.players.append(player);
           
    #affichage de l'image de fond
    def createGameBoard(self):
        self.fond_e = pygame.image.load("./image/blocks/"+self.map.folderTexture+"/"+"fond.png").convert()
        self.fenetre.blit(self.fond_e, (0,0))
        #affichage des blocks (elements) sur la fenetre
        for i in range (0,len(self.map.map_grid_elem)):
            self.fenetre.blit(self.map.map_grid_elem[i].get_image(), (self.map.map_grid_elem[i].pos_x,self.map.map_grid_elem[i].pos_y))
        
    def refreshGame(self):
        #refresh fond
        self.fenetre.blit(self.fond_e, (0,0))

        #refresh block
        for i in range (0,len(self.map.map_grid_elem)): 
            self.fenetre.blit(self.map.map_grid_elem[i].get_image(), (self.map.map_grid_elem[i].pos_x,self.map.map_grid_elem[i].pos_y))
            pygame.draw.rect(self.fenetre,(255,0,0), ((self.map.map_grid_elem[i].pos_x,self.map.map_grid_elem[i].pos_y),(64,64)), 1)

        #met hors jeu les joueurs morts
        for i in range (0,len(self.players)):
            if self.players[i].hp<=0:
                self.players[i].isAlive=False

        #déplace les joueurs et les fleches
        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.controlerAction(self.players[i])
            self.players[i].movement_arrow()

        #refresh joueur et fleches
        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.display_player(self.players[i])
            for j in range(0, len(self.players[i].arrows_launched)):
                pygame.draw.rect(self.fenetre,(255,0,0), ((self.players[i].arrows_launched[j].entity_coord.centerx-26,self.players[i].arrows_launched[j].entity_coord.centery-26),(52,52)), 1)
                self.fenetre.blit(self.players[i].arrows_launched[j].entity,(self.players[i].arrows_launched[j].entity_coord.centerx-26,self.players[i].arrows_launched[j].entity_coord.centery-26))

        #verification et application des effect de colision
        for i in range (0,len(self.players)):
            indexArrowDel = []
            for a in range (0,len(self.players[i].arrows_launched)):
                indexBlockDel = []
                for n in range (0,len(self.players)):
                    if n!=i:
                        if self.players[i].touchCircle(self.players[n].entity_coord.centerx, self.players[n].entity_coord.centery, 24, self.players[i].arrows_launched[a]):
                            self.players[i].arrows_launched[a].effect(self.players[n])
                            indexArrowDel.append(a)

                b=0
                suppr=0
                while b<len(self.map.map_grid_elem):
                    suppr=0
                    if self.players[i].touchRectangle(self.map.map_grid_elem[b].pos_x+32,self.map.map_grid_elem[b].pos_y+32,64,64,self.players[i].arrows_launched[a]):
                        suppr = self.map.map_grid_elem[b].touchEffect(self.players[i].arrows_launched[a])
                    if suppr==2:
                        indexBlockDel.append(b)
                    if suppr>=1:
                        indexArrowDel.append(a)
                    b=b+1

                for e in range(0,len(indexBlockDel)):
                    del self.map.map_grid_elem[indexBlockDel[e]]

            for e in range(0,len(indexArrowDel)):
                del self.players[i].arrows_launched[indexArrowDel[e]]            
                
    def controlerAction(self,player):
        #Si il a relaché le bouton et qu'il n'est plus en cd
        if (player.controler.get_axis( 2 ) < 0.600) and (pygame.time.get_ticks()-player.debutDash)>2000:
            player.canDash=True

        wantMove=True
        if not player.isDashing:
            if player.controler.get_axis( 0 ) < -0.350 and player.controler.get_axis( 1 ) < -0.350:
                 player.direction="NW"
            elif player.controler.get_axis( 0 ) < -0.350 and player.controler.get_axis( 1 ) > 0.350:
                 player.direction="SW"
            elif player.controler.get_axis( 0 ) > 0.350 and player.controler.get_axis( 1 ) < -0.350:
                 player.direction="NE"
            elif player.controler.get_axis( 0 ) > 0.350 and player.controler.get_axis( 1 ) > 0.350:
                 player.direction="SE"
            elif player.controler.get_axis( 1 ) < -0.500:
                 player.direction="N"
            elif player.controler.get_axis( 1 ) > 0.500:
                 player.direction="S"
            elif player.controler.get_axis( 0 ) > 0.500:
                 player.direction="E"
                 print "GROS PD"
            elif player.controler.get_axis( 0 )< -0.500:
                 player.direction="W"
            else:
                wantMove=False
            
        if wantMove:
            if self.canMove():
                player.movement()

        player.movement_sight()
        player.button_pressed()

        #Si le joueur essay de dasher et peut dasher
        if player.controler.get_axis( 2 ) > 0.700 and player.canDash:
            player.dash()
        
    def canMove(self):
        return True

    def display_player(self,player):
        if player.direction_sight=="NE":
            self.fenetre.blit(player.bow_NE, (player.entity_coord.centerx+5,player.entity_coord.top))
            self.fenetre.blit(player.image_NE, player.entity_coord)
        if player.direction_sight=="SE":
            self.fenetre.blit(player.bow_SE, (player.entity_coord.centerx+2,player.entity_coord.centery+4))
            self.fenetre.blit(player.image_SE, player.entity_coord)
        if player.direction_sight=="SW":
            self.fenetre.blit(player.bow_SW, (player.entity_coord.centerx-38,player.entity_coord.top+42))
            self.fenetre.blit(player.image_SW, player.entity_coord)
        if player.direction_sight=="NW":
            self.fenetre.blit(player.bow_NW, (player.entity_coord.centerx-40,player.entity_coord.top+5))
            self.fenetre.blit(player.image_NW, player.entity_coord)
        if player.direction_sight=="N":
            self.fenetre.blit(player.bow_N, (player.entity_coord.left+15,player.entity_coord.top-4))
            self.fenetre.blit(player.image_N, player.entity_coord)
        if player.direction_sight=="S":
            self.fenetre.blit(player.bow_S, (player.entity_coord.left+15,player.entity_coord.bottom-10))
            self.fenetre.blit(player.image_S, player.entity_coord)
        if player.direction_sight=="W":
            self.fenetre.blit(player.bow_W, (player.entity_coord.centerx-43,player.entity_coord.top+15))
            self.fenetre.blit(player.image_W, player.entity_coord)
        if player.direction_sight=="E":
            self.fenetre.blit(player.bow_E, (player.entity_coord.centerx+30,player.entity_coord.top+15))
            self.fenetre.blit(player.image_E, player.entity_coord)
        
######################################################################################################################################################################################################
                
class Player():
    def __init__(self,speed,controler,nplayer,speed_diagonale):
        #chargement des images dans des variables (pour le faire qu'une fois)
        self.image_S = pygame.image.load("./image/player/"+nplayer+"/player_S.png").convert_alpha()
        self.image_N = pygame.image.load("./image/player/"+nplayer+"/player_N.png").convert_alpha()
        self.image_W = pygame.image.load("./image/player/"+nplayer+"/player_W.png").convert_alpha()
        self.image_E = pygame.image.load("./image/player/"+nplayer+"/player_E.png").convert_alpha()
        self.image_NE = pygame.image.load("./image/player/"+nplayer+"/player_NE.png").convert_alpha()
        self.image_NW = pygame.image.load("./image/player/"+nplayer+"/player_NW.png").convert_alpha()
        self.image_SW = pygame.image.load("./image/player/"+nplayer+"/player_SW.png").convert_alpha()
        self.image_SE = pygame.image.load("./image/player/"+nplayer+"/player_SE.png").convert_alpha()

        self.bow_S = pygame.image.load("./image/bow/none/bow_none_S.png").convert_alpha()
        self.bow_N = pygame.image.load("./image/bow/none/bow_none_N.png").convert_alpha()
        self.bow_W = pygame.image.load("./image/bow/none/bow_none_W.png").convert_alpha()
        self.bow_E = pygame.image.load("./image/bow/none/bow_none_E.png").convert_alpha()
        self.bow_NW = pygame.image.load("./image/bow/none/bow_none_NW.png").convert_alpha()
        self.bow_NE = pygame.image.load("./image/bow/none/bow_none_NE.png").convert_alpha()
        self.bow_SE = pygame.image.load("./image/bow/none/bow_none_SE.png").convert_alpha()
        self.bow_SW = pygame.image.load("./image/bow/none/bow_none_SW.png").convert_alpha()
        
        self.entity_coord=self.image_S.get_rect()
        self.level=1
        self.exp=0
        self.hp=100
        self.speed=speed
        self.speed_diagonale = speed_diagonale
        self.controler=controler
        self.isAlive=True
        self.arrows_launched = []
        self.can_shoot = True
        self.combo_inc = []
        self.combo_add = True
        self.isDashing = False
        self.direction ="N"
        self.speed_dash = [30,30]
        self.speed_dash_diagonale = [20,20]
        self.canDash = True
        self.debutDash=-1
        self.direction_sight = "N"
        self.entity= self.image_S
        
    def movement(self):
        #si il est toujours entrain de dash
        if(pygame.time.get_ticks()-self.debutDash)<50:
            self.movement_dash()
        else:
            self.isDashing=False
            self.movement_walk()
        
    def movement_walk(self):
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

    def movement_dash(self):
        if self.direction== "N":
            self.entity_coord = self.entity_coord.move(0, -self.speed_dash[0])
        elif self.direction== "S":
            self.entity_coord = self.entity_coord.move(0, self.speed_dash[0])
        elif self.direction== "W":
            self.entity_coord = self.entity_coord.move(-self.speed_dash[0], 0)
        elif self.direction== "E":
            self.entity_coord = self.entity_coord.move(self.speed_dash[0], 0)
        elif self.direction== "NE":
            self.entity_coord = self.entity_coord.move(self.speed_dash_diagonale[0], -self.speed_dash_diagonale[0])
        elif self.direction== "NW":
            self.entity_coord = self.entity_coord.move(-self.speed_dash_diagonale[0], -self.speed_dash_diagonale[0])
        elif self.direction== "SE":
            self.entity_coord = self.entity_coord.move(self.speed_dash_diagonale[0], self.speed_dash_diagonale[0])
        elif self.direction== "SW":
            self.entity_coord = self.entity_coord.move(-self.speed_dash_diagonale[0], self.speed_dash_diagonale[0])
            
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
            
            self.shoot_arrow("SW")
            self.direction_sight="SW"
            
        elif self.controler.get_axis( 4 ) < -0.500 and self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx-20,self.entity_coord.centery-20)
            self.shoot_arrow("NW")
            self.direction_sight="NW"
            
        elif self.controler.get_axis( 4 ) > 0.500 and self.controler.get_axis( 3 ) > 0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery+20)
            self.shoot_arrow("SE")
            self.direction_sight="SE"
            
        elif self.controler.get_axis( 4 ) > 0.500 and self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery-20)
            self.shoot_arrow("NE")
            self.direction_sight="NE"
            
        elif self.controler.get_axis( 4 ) < -0.500:
            center_aim=(self.entity_coord.centerx-20,self.entity_coord.centery)
            self.shoot_arrow("W")
            self.direction_sight="W"
           
        elif self.controler.get_axis( 4 ) > 0.500:
            center_aim=(self.entity_coord.centerx+20,self.entity_coord.centery)
            self.shoot_arrow("E")
            self.direction_sight="E"
            
        elif self.controler.get_axis( 3 ) > 0.500:
            center_aim=(self.entity_coord.centerx,self.entity_coord.centery+20)
            self.shoot_arrow("S")
            self.direction_sight="S"
            
        elif self.controler.get_axis( 3 )< -0.500:
            center_aim=(self.entity_coord.centerx,self.entity_coord.centery-20)
            self.shoot_arrow("N")
            self.direction_sight="N"
            


            
    def shoot_arrow(self,direction):
        if self.controler.get_axis( 2 ) < -0.700 and self.can_shoot:
            if direction== "N":
                if(len(self.combo_inc)==2):
                    if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_N.png").convert_alpha()
                    else:
                        self.combo_inc = []
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_S.png").convert_alpha()
                    else:
                        self.combo_inc = []
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_W.png").convert_alpha()
                    else:
                        self.combo_inc = []
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_E.png").convert_alpha()
                    else:
                        self.combo_inc = []
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_NE.png").convert_alpha()
                    else:
                        self.combo_inc = []
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_NW.png").convert_alpha()
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_SE.png").convert_alpha()
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
                        arrow_entity = pygame.image.load("./image/arrow/simple/arrow_simple_SW.png").convert_alpha()
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

 
    def touchCircle(self,target_x,target_y,r,arrow):

            coord = arrow.getSpike()

            x=coord[0]
            y=coord[1]
            if sqrt((target_x-x)**2+(target_y-y)**2)<r:
                return True
            else:
                return False



    def touchRectangle(self,target_x,target_y,size_x,size_y,arrow):
        coord = arrow.getSpike()
        x=coord[0]
        y=coord[1]
        
        if abs(x-target_x)<(size_x/2) and abs(y-target_y)<(size_y/2):
            return True
        else:
            return False

    def dash(self):
            self.debutDash=pygame.time.get_ticks()
            self.isDashing = True
            self.canDash=False

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

    def getSpike(self):
                
        if self.direction== "N":
            x=self.entity_coord.centerx
            y=self.entity_coord.top
        elif self.direction== "S":
            x=self.entity_coord.centerx
            y=self.entity_coord.bottom
        elif self.direction== "W":
            x=self.entity_coord.left
            y=self.entity_coord.centery
        elif self.direction== "E":
            x=self.entity_coord.right
            y=self.entity_coord.centery
        elif self.direction== "NE":
            x=self.entity_coord.right
            y=self.entity_coord.top
        elif self.direction== "NW":
            x=self.entity_coord.left
            y=self.entity_coord.top
        elif self.direction== "SE":
            x=self.entity_coord.right
            y=self.entity_coord.bottom
        elif self.direction== "SW":
            x=self.entity_coord.left
            y=self.entity_coord.bottom

        coord=[x,y]

        return coord
        
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
    def __init__(self,folderTextureP,levelP):

        # Initialisation et affectation de l'attribut grid
        #coordonnée X Y typeBlock()   hitbox
        # 1 : blockIndestructible
        # 2 : blockDestructible
        # 3 : passThrough

        self.map_grid_elem=[]
        self.folderTexture=folderTextureP
        self.level= levelP
        
        #parcours de la map_grid du fichier
        for i in range(0, 12):
            for j in range(0, 20):
            
            
                #unbreak    0
                #void       1
                #breakGood  2
                #breakBad   3
                #breakRelBad    4
                #through    5

                #appel constructeur de chaque block
                if map_grid_AllList[self.get_Level()][i][j] == 0:
                    self.map_grid_elem.append(ElementUnbreakable(j*64,i*64,self.folderTexture))
                elif map_grid_AllList[self.get_Level()][i][j] == 2:
                    self.map_grid_elem.append(ElementBreakable(j*64,i*64,3,self.folderTexture))
                elif map_grid_AllList[self.get_Level()][i][j] == 3:
                    self.map_grid_elem.append(ElementBreakable(j*64,i*64,2,self.folderTexture))
                elif map_grid_AllList[self.get_Level()][i][j] == 4:
                    self.map_grid_elem.append(ElementBreakable(j*64,i*64,1,self.folderTexture))
                elif map_grid_AllList[self.get_Level()][i][j] == 5:
                    self.map_grid_elem.append(ElementPassThrough(j*64,i*64,self.folderTexture))
    # Retourne la grid
    def get_grid(self):
        return self.map_grid_elem

    # Retourne le next level
    def get_Level(self):
        return self.level


######################################################################################################################################################################################################

class Element():
    def __init__(self,x,y,folderTexture):
        self.pos_x = x
        self.pos_y = y
        self.image  = "temp"

    def get_image(self):
        return self.image

    def touchEffect(self,arrow):
        return 0
######################################################################################################################################################################################################

class ElementBreakable(Element):
    def __init__(self,x,y,stateP,folderTexture):
        Element.__init__(self,x,y,folderTexture)
        self.state = stateP  #HP
        self.image = pygame.image.load("./image/blocks/"+folderTexture+"/"+"break_3.png").convert()
        self.image_break_2 = pygame.image.load("./image/blocks/"+folderTexture+"/"+"break_2.png").convert()
        self.image_break_1 = pygame.image.load("./image/blocks/"+folderTexture+"/"+"break_1.png").convert()
        
    def get_state(self):
            return self.state

    def arrowHitDest(self):
        self.state = self.state-1
        if self.state>0:
            return False
        else:
            return True

    def get_image(self):
            if self.state==3 :
                return self.image
            elif self.state == 2:
                return self.image_break_2
            elif self.state == 1:
                return self.image_break_1
            else:
                return self.image

    def touchEffect(self,arrow):
        if self.arrowHitDest():
            return 2
        else:
            return 1
######################################################################################################################################################################################################

class ElementUnbreakable(Element):
    def __init__(self,x,y,folderTexture):
        Element.__init__(self,x,y,folderTexture)
        self.image = pygame.image.load("./image/blocks/"+folderTexture+"/"+"stoneUnbreak.png").convert()
    
    def touchEffect(self,arrow):
        return 1

##########################################################################################################################################################
class ElementPassThrough(Element):
    def __init__(self,x,y,folderTexture):
        Element.__init__(self,x,y,folderTexture)
        self.image = pygame.image.load("./image/blocks/"+folderTexture+"/"+"goThrough.png").convert()
        
###############################################################################################################################################
class TexturesListCheck():
    def __init__(self):
        self.texturesFolderBlock = ""
        self.listOfTextures = [ ["break_1.png","break_2.png","break_3.png","default.png","fond.png","goThrough.png","stoneUnbreak.png"],
                                ["_E.png","_N.png","_NE.png","_NW.png","_S.png","_SE.png","_SW.png","_W.png"],
                                ["bow_E.png","bow_N.png","bow_NE.png","bow_NW.png","bow_S.png","bow_SE.png","bow_SW.png","bow_W.png"]
                              ]
        self.ListMissingTexture =[]

    def checkExistBlock(self):
        path = ["./image/blocks","./image/arrow","./image/player","./image/bow"]

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
        '''
        #textures des bows
        subfolder = next(os.walk(path[3]))[1] #bow

        for folder in subfolder:
            for fileTexture in self.listOfTextures[2]: #list of bow
                if not os.path.exists(path[2]+"/"+folder+"/player"+fileTexture): #path[1]
                    self.ListMissingTexture.append(folder+"/player"+fileTexture)
        '''
        return len(self.ListMissingTexture)

    #get la liste des textures des blocks
    def get_TexturesFolderBlock(self):
        return self.texturesFolderBlock

    #get la liste des textures manquante
    def get_TexturesFolder(self):
        return self.ListMissingTexture
