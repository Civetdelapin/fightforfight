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
    def __init__(self,fenetre,cursors,controlers,map_choose):
        pygame.mixer.music.stop()
        self.fenetre=fenetre
        self.map = map_choose
        self.cursors=cursors
        self.players= []
        self.nb_player=len(cursors)
        self.image_pause = pygame.image.load("./image/pause.png").convert_alpha()
        self.myfont = pygame.font.SysFont("monospace", 35)
        self.players_dead = []
        self.win = pygame.image.load("./image/win.png").convert_alpha()
        self.debuff_slowed = pygame.image.load("./image/debuff/debuff_slowed.png").convert_alpha()
        self.debuff_fire = pygame.image.load("./image/debuff/debuff_fire.png").convert_alpha()
        self.debuff_stun = pygame.image.load("./image/debuff/debuff_stun.png").convert_alpha()
       
        #création du plateau
        self.createGameBoard()

        #affection des mannettes
        self.controlers=controlers

        #création des joueurs
        for i in  range (0,self.nb_player):
            
            speed = [3, 3]
            speed_diagonale= [2,2]
            player = Player(speed,controlers[i],str(cursors[i].choix+1),speed_diagonale)
            self.players.append(player);
           
    #affichage de l'image de fond
    def createGameBoard(self):
        self.fond_e = pygame.image.load("./image/blocks/"+self.map.folderTexture+"/"+"fond.png").convert()
        self.hud_hp_bar = pygame.image.load("./image/hud/hud.png").convert_alpha()
        self.hud_1 = pygame.image.load("./image/hud/hud_1.png").convert_alpha()
        self.hud_2 = pygame.image.load("./image/hud/hud_2.png").convert_alpha()
        self.hud_3 = pygame.image.load("./image/hud/hud_3.png").convert_alpha()
        self.hud_4 = pygame.image.load("./image/hud/hud_4.png").convert_alpha()
        self.hud_dead = pygame.image.load("./image/hud/dead.png").convert_alpha()
        self.hud_dead_2 = pygame.image.load("./image/hud/dead_2.png").convert_alpha()
        
        self.fenetre.blit(self.fond_e, (0,0))
        #affichage des blocks (elements) sur la fenetre
        for i in range (0,len(self.map.map_grid_elem)):
            self.fenetre.blit(self.map.map_grid_elem[i].get_image(), (self.map.map_grid_elem[i].pos_x,self.map.map_grid_elem[i].pos_y))

    def refresh_hp_bar(self):
        for i in range(0,len(self.players)):
            percentage=int((float(self.players[i].hp)/float(100))*float(286))
            if int(self.players[i].nplayer)==1:
                self.fenetre.blit(self.hud_1,(6,1))
                if self.players[i].isAlive:
                    pygame.draw.rect(self.fenetre,(255,0,0),(78,14,int(percentage),35),0)
                else:
                    self.fenetre.blit(self.hud_dead,(6,1))
            elif int(self.players[i].nplayer)==2:
                self.fenetre.blit(self.hud_2,(781,705))
                if self.players[i].isAlive:
                    pygame.draw.rect(self.fenetre,(255,0,0),(916,719,int(percentage),35),0)
                else:
                    self.fenetre.blit(self.hud_dead_2,(910,705))
            elif int(self.players[i].nplayer)==3:
                self.fenetre.blit(self.hud_3,(781,1))
                if self.players[i].isAlive:
                    pygame.draw.rect(self.fenetre,(255,0,0),(916,14,int(percentage),35),0)
                else:
                    self.fenetre.blit(self.hud_dead_2,(910,1))
            elif int(self.players[i].nplayer)==4:
                self.fenetre.blit(self.hud_4,(6,705))
                if self.players[i].isAlive:
                    pygame.draw.rect(self.fenetre,(255,0,0),(78,719,int(percentage),35),0)
                else:
                    self.fenetre.blit(self.hud_dead,(6,705))

    def refresh_player_score(self):
        for i in range(0,len(self.players)):
            label = self.myfont.render(str(self.players[i].score), 1, (255,0,0))
            
            if int(self.players[i].nplayer)==1:
                self.fenetre.blit(label, (398, 23))
            if int(self.players[i].nplayer)==3:
                self.fenetre.blit(label, (800, 23))
            if int(self.players[i].nplayer)==2:
                self.fenetre.blit(label, (800, 728))
            if int(self.players[i].nplayer)==4:
                self.fenetre.blit(label, (398, 728))
            
                
         
    
    def refreshGame(self):
        player_dead = 0
        for i in self.players:
            if not i.isAlive:
                   player_dead=player_dead+1
        if player_dead==(len(self.players)-1):
            for i in self.players:
                if i.isAlive:
                    player_win=i
            while True :
                        for event in pygame.event.get():
                            if event.type == QUIT:      #si l'utilisateur clique sur la croix
                                pygame.quit()
                                sys.exit()
                        self.fenetre.blit(self.win, (0,0))
                        self.fenetre.blit(player_win.image_S,(500,400))
                        pygame.display.flip()
                        pygame.time.wait(5)
        
        #refresh fond
        self.fenetre.blit(self.fond_e, (0,0))

        #refresh block
        for i in range (0,len(self.map.map_grid_elem)): 
            self.fenetre.blit(self.map.map_grid_elem[i].get_image(), (self.map.map_grid_elem[i].pos_x,self.map.map_grid_elem[i].pos_y))
        
        
        #met hors jeu les joueurs morts
        for i in range (0,len(self.players)):
            if self.players[i].hp<=0:
                self.players[i].isAlive=False
                self.players_dead.append(self.players[i])

        #déplace les joueurs et les fleches
        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.controlerAction(self.players[i])
            self.players[i].movement_arrow()

        #refresh joueur et fleches
        for i in range(0, len(self.players)):
            if self.players[i].isAlive:
                self.display_player(self.players[i])
                if self.players[i].iceState:
                    self.fenetre.blit(self.debuff_slowed,self.players[i].entity_coord)
                if self.players[i].fireState:
                    self.fenetre.blit(self.debuff_fire,self.players[i].entity_coord)
                if self.players[i].earthState:
                    self.fenetre.blit(self.debuff_stun,self.players[i].entity_coord)
            for j in range(0, len(self.players[i].arrows_launched)):
                self.fenetre.blit(self.players[i].arrows_launched[j].entity,(self.players[i].arrows_launched[j].entity_coord.centerx-26,self.players[i].arrows_launched[j].entity_coord.centery-26))

        #verification et application des effect de colision
        for i in range (0,len(self.players)):
            indexArrowDel = []      #liste de fleches a supprimer
            for a in range (0,len(self.players[i].arrows_launched)):
                indexBlockDel = []  #Liste de blocs de supprimer
                for n in range (0,len(self.players)):
                    if n!=i and self.players[n].isAlive:        #Pour eviter de vérifier si un joueur se touche lui même
                        #si la fleche "a" du joueur "i" touche le jouer "n"
                        if self.players[i].touchCircle(self.players[n].entity_coord.centerx, self.players[n].entity_coord.centery, 24, self.players[i].arrows_launched[a]):
                            self.players[i].score=self.players[i].score+100
                            self.players[n].score=self.players[n].score-50
                            self.players[i].arrows_launched[a].effect(self.players[n])  #applique les effets de la fleche sur le joueur "n"
                            if not a in indexArrowDel:
                                
                                indexArrowDel.append(a)

                #le for() ne marche pas a essayer plus tard
                b=0  
                suppr=0             #variable permetant de connaitre les effet de la fleche sur la cible
                #parcour des blocs de la map
                while b<len(self.map.map_grid_elem):
                    suppr=0         #remise a 0 -> n'a aucun effet
                    spikeArrow = self.players[i].arrows_launched[a].getSpike()
                    #si la fleche "a" touche le bloc "b"
                    if self.players[i].touchRectangle(self.map.map_grid_elem[b].pos_x+32,self.map.map_grid_elem[b].pos_y+32,64,64,spikeArrow[0],spikeArrow[1]):
                        suppr = self.map.map_grid_elem[b].touchEffect(self.players[i].arrows_launched[a])   #renvoi de la valeur suppr pour connaitre les effect du bloc sur la fleche
                    #si le bloc doit etre supprimé
                    if suppr==2:
                        indexBlockDel.append(b)
                    #si la fleche doit etre supprimé
                    if suppr>=1:
                        
                        indexArrowDel.append(a)
                    b=b+1

                #parcour et supression des blocs dont l'indice est dans la liste indexBlockDel
                for e in range(len(indexBlockDel)-1,-1,-1):
                    del self.map.map_grid_elem[indexBlockDel[e]]

            indexArrowDelFirst = []
            
            if len(indexArrowDel)>0:
                indexArrowDelFirst.append(indexArrowDel[0])
                
            #parcour et supression des fleches dont l'indice est dans la liste indexArrowDel
            for e in range(len(indexArrowDelFirst)-1,-1,-1):
                del self.players[i].arrows_launched[indexArrowDelFirst[e]]
                                                    
            #test appuie sur START
            for c in self.players:
                if c.controler.get_button(7)==1:
                    while c.controler.get_button(1)==0 :
                        for event in pygame.event.get():
                            if event.type == QUIT:      #si l'utilisateur clique sur la croix
                                pygame.quit()
                                sys.exit()
                        rect = pygame.Surface((1280,768), pygame.SRCALPHA, 32)
                        rect.fill((0, 0, 0, 50))
                        self.fenetre.blit(rect, (0,0))
                        self.fenetre.blit(self.image_pause,(0,0))
                        pygame.display.flip()
                        pygame.time.wait(5)

            self.players[i].statementEffect()


            
        #affichage bar de vie :
        self.refresh_hp_bar()
        #affiche score
        self.refresh_player_score()


        
    def controlerAction(self,player):


        #Si il a relaché le bouton de dash (lt) et qu'il n'est plus en cd
        if (player.controler.get_axis( 2 ) < 0.600) and (pygame.time.get_ticks()-player.debutDash)>3000:
            player.canDash=True

        wantMove=True   # variable permettant de savoir si un joueur bouge son analogue de gauche (celui de déplacement)

        #si il n'est pas entrain de dasher METTRE DANS UNE METHODE PLAYER
        if not player.isDashing and player.direction_modif:
            #affectation de la direction voulue par le joueur
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
            elif player.controler.get_axis( 0 )< -0.500:
                 player.direction="W"
            else:       #si il ne dirige pas son analogue
                wantMove=False

        player.movement_sight() #gere l'orientation du joueur (visée)
        player.button_pressed() #gere les boutons préssés (combo etc)

        #Si le joueur essay de dasher et peut dasher
        if player.controler.get_axis( 2 ) > 0.700 and player.canDash:
            player.dash()
            
        if player.speedCount in player.speedManag:
            #si il veut bouger et qu'il peut bouger
            if wantMove and self.canMove(player):
                player.movement()
                
        player.speedCount=player.speedCount+1

        if player.speedCount==10:
            player.speedCount=0

    def possibleDirection(self,player,points,pointsList,playerMove,blocks):
        #blocage de direction (avancement bloqué)
        
        if player.isDashing:
            player.isDashing=False
            return False
        else:
            
            for i in range (0,len(points)):
                
                #P1
                if playerMove:
                    if points[i]==pointsList[0]:
                        if blocks[i].pos_y+64 >= points[i][1] and (player.direction=="N" or player.direction=="NE" or player.direction=="NW"):
                            if player.direction=="NW":
                                player.direction="W"
                                playerMove= True
                            elif player.direction=="NE":
                                player.direction="E"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_x+64 >= points[i][0] and (player.direction=="W" or player.direction=="SW" or player.direction=="NW" or player.direction=="N" or player.direction=="NE"):
                            if player.direction=="SW":
                                player.direction="S"
                                playerMove= True
                            elif player.direction=="NE":
                                player.direction="E"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_x <= points[i][0] and (player.direction=="E" or player.direction=="SE" or player.direction=="NE" or player.direction=="N" or player.direction=="NW"):
                            if player.direction=="NW":
                                player.direction="W"
                                playerMove= True
                            elif player.direction=="SE":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True


                    #P2
                    elif points[i]==pointsList[1]:
                        if (blocks[i].pos_y+64 >= points[i][1] or blocks[i].pos_x <= points[i][0]) and (player.direction=="N" or player.direction=="NE" or player.direction=="NW" or player.direction=="E" or player.direction=="SE"):
                            if player.direction=="NW":
                                player.direction="W"
                                playerMove= True
                            elif player.direction=="SE":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True


                    #P3
                    elif points[i]==pointsList[2]:
                        if blocks[i].pos_x <= points[i][0] and (player.direction=="E" or player.direction=="NE" or player.direction=="SE"):
                            if player.direction=="NE":
                                player.direction="N"
                                playerMove= True
                            elif player.direction=="SE":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_y+64 >= points[i][1] and (player.direction=="E" or player.direction=="SE" or player.direction=="NW" or player.direction=="N" or player.direction=="NE"):
                            if player.direction=="NW":
                                player.direction="W"
                                playerMove= True
                            elif player.direction=="SE":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_y <= points[i][1] and (player.direction=="S" or player.direction=="SE" or player.direction=="SW" or player.direction=="E" or player.direction=="NE"):
                            if player.direction=="NE":
                                player.direction="N"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="W"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

                    #P4
                    elif points[i]==pointsList[3]:
                        if (blocks[i].pos_x <= points[i][0] or blocks[i].pos_y <= points[i][1]) and (player.direction=="E" or player.direction=="NE" or player.direction=="SW" or player.direction=="S" or player.direction=="SE"):
                            if player.direction=="NE":
                                player.direction="N"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="W"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

                    #P5
                    elif points[i]==pointsList[4]:
                        if blocks[i].pos_y <= points[i][1] and (player.direction=="S" or player.direction=="SE" or player.direction=="SW"):
                            if player.direction=="SE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="W"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_x <= points[i][0] and (player.direction=="E" or player.direction=="SE" or player.direction=="NE" or player.direction=="S" or player.direction=="SW"):
                            if player.direction=="NE":
                                player.direction="N"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="W"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_x+64 >= points[i][0] and (player.direction=="S" or player.direction=="SE" or player.direction=="SW" or player.direction=="W" or player.direction=="NW"):
                            if player.direction=="SE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="NW":
                                player.direction="N"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

                    #P6
                    elif points[i]==pointsList[5]:
                        if (blocks[i].pos_y <= points[i][1] or blocks[i].pos_x+64 >= point[0])and (player.direction=="S" or player.direction=="SE" or player.direction=="SW" or player.direction=="W" or player.direction=="NW"):
                            if player.direction=="SE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="NW":
                                player.direction="N"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

                    #P7
                    elif points[i]==pointsList[6]:
                        if blocks[i].pos_x+64 >= points[i][0] and (player.direction=="W" or player.direction=="SW" or player.direction=="NW"):
                            if player.direction=="SW":
                                player.direction="S"
                                playerMove= True
                            elif player.direction=="NW":
                                player.direction="N"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_y <= points[i][1] and (player.direction=="W" or player.direction=="SW" or player.direction=="NW" or player.direction=="S" or player.direction=="SE"):
                            if player.direction=="SE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="NW":
                                player.direction="N"
                                playerMove= True
                            else:
                                playerMove= False
                        elif blocks[i].pos_y+64 >= points[i][1] and (player.direction=="W" or player.direction=="SW" or player.direction=="NW" or player.direction=="N" or player.direction=="NE"):
                            if player.direction=="NE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

                    #P8
                    elif points[i]==pointsList[7]:
                        if (blocks[i].pos_x+64 >= points[i][0] or blocks[i].pos_y+64 >= points[i][1] )and (player.direction=="W" or player.direction=="SW" or player.direction=="NW" or player.direction=="N" or player.direction=="NE"):
                            if player.direction=="NE":
                                player.direction="E"
                                playerMove= True
                            elif player.direction=="SW":
                                player.direction="S"
                                playerMove= True
                            else:
                                playerMove= False
                        else:
                            playerMove = True

            
            return playerMove


    def canMove(self,player):
        speedx = 0
        speedy = 0
        playerMove = True

        if not player.isDashing:
            speed_playerx=player.speed[0]
            speed_playery=player.speed[1]
        else:
            speed_playerx = player.speed_dash[0]
            speed_playery = player.speed_dash[1]
            if player.direction=="NW" or player.direction== "SW" or player.direction== "SE" or player.direction== "NE":
                speed_playerx = player.speed_dash_diagonale[0]
                speed_playery = player.speed_dash_diagonale[1]

        if player.direction== "E" or player.direction== "NE" or player.direction== "SE" :
            speedx=speed_playerx

        if player.direction== "S" or player.direction== "SE" or player.direction== "SW" :
            speedy=speed_playery
        
        if player.direction== "W" or player.direction== "NW" or player.direction== "SW" :
            speedx=-speed_playerx
            
        if player.direction== "N" or player.direction== "NW" or player.direction== "NE":
            speedy=-speed_playery
        
        x = player.entity_coord.centerx+speedx
        y = player.entity_coord.centery+speedy

        r = 24
        root = sqrt(2)/2
        p1 = [x,y-r]
        p2 = [x+r*root,y-r*root] 
        p3 = [x+r,y]
        p4 = [x+r*root,y+r*root]
        p5 = [x,y+r]
        p6 = [x-r*root,y+r*root]
        p7 = [x-r,y]
        p8 = [x-r*root,y-r*root]
        pointsList = [p1,p2,p3,p4,p5,p6,p7,p8]

        
        playerMove = True

        
        touchPointsList = []
        touchBlocksList = []
        for point in range (0,len(pointsList)):
            
            block = 0
            #
            while block < len(self.map.map_grid_elem) and not pointsList[point] in touchPointsList:
                if player.touchRectangle(self.map.map_grid_elem[block].pos_x+32,self.map.map_grid_elem[block].pos_y+32,64,64,pointsList[point][0],pointsList[point][1]):  #detection du bloc
                    touchPointsList.append(pointsList[point])
                    touchBlocksList.append(self.map.map_grid_elem[block])
                block=block+1

        if touchPointsList:
            points = []
            if player.direction== "N":
                if p1 in touchPointsList:
                    points.append(p1)
                elif p8 in touchPointsList:
                    points.append(p8)
                elif p2 in touchPointsList:
                    points.append(p2)
                elif p7 in touchPointsList:
                    points.append(p7)
                elif p3 in touchPointsList:
                    points.append(p3)
            elif player.direction== "S":
                if p5 in touchPointsList:
                    points.append(p5)
                elif p4 in touchPointsList:
                    points.append(p4)
                elif p6 in touchPointsList:
                    points.append(p6)
                elif p3 in touchPointsList:
                    points.append(p3)
                elif p7 in touchPointsList:
                    points.append(p7)
            elif player.direction== "W":
                if p7 in touchPointsList:
                    points.append(p7)
                elif p6 in touchPointsList:
                    points.append(p6)
                elif p8 in touchPointsList:
                    points.append(p8)
                elif p5 in touchPointsList:
                    points.append(p5)
                elif p1 in touchPointsList:
                    points.append(p1)
            elif player.direction== "E":
                if p3 in touchPointsList:
                    points.append(p3)
                elif p2 in touchPointsList:
                    points.append(p2)
                elif p4 in touchPointsList:
                    points.append(p4)
                elif p1 in touchPointsList:
                    points.append(p1)   
                elif p5 in touchPointsList:
                    points.append(p5)
            elif player.direction== "NE":
                if p2 in touchPointsList:
                    points.append(p2)
                    
                if p1 in touchPointsList:
                    
                    points.append(p1)
                if p3 in touchPointsList:
                    
                    points.append(p3)
                if p8 in touchPointsList:
                    points.append(p8)
                if p4 in touchPointsList:
                    points.append(p4)
            elif player.direction== "NW":
                if p8 in touchPointsList:
                    points.append(p8)
                if p7 in touchPointsList:
                    points.append(p7)
                if p1 in touchPointsList:
                    points.append(p1)
                if p6 in touchPointsList:
                    points.append(p6)
                if p2 in touchPointsList:
                    points.append(p2)
            elif player.direction== "SE":
                if p4 in touchPointsList:
                    points.append(p4)
                if p3 in touchPointsList:
                    points.append(p3)
                if p5 in touchPointsList:
                    points.append(p5)
                if p2 in touchPointsList:
                    points.append(p2)
                if p6 in touchPointsList:
                    points.append(p6)
            elif player.direction== "SW":
                if p6 in touchPointsList:
                    points.append(p6)
                if p5 in touchPointsList:
                    points.append(p5)
                if p7 in touchPointsList:
                    points.append(p7)
                if p4 in touchPointsList:
                    points.append(p4)
                if p8 in touchPointsList:
                   points.append(p8)

            blocks = []  
            for i in range (0, len(touchPointsList)):
                for j in range (0, len(points)):
                    if (touchPointsList[i]==points[j]):
                        blocks.append(touchBlocksList[i])
            
            playerMove=self.possibleDirection(player,points,pointsList,playerMove,blocks)
                
        return playerMove


    def display_player(self,player):
        if player.direction_sight=="NE":
            self.fenetre.blit(player.bow_NE, (player.entity_coord.centerx+5,player.entity_coord.top))
            self.fenetre.blit(player.image_NE, player.entity_coord)
        elif player.direction_sight=="SE":
            self.fenetre.blit(player.bow_SE, (player.entity_coord.centerx+2,player.entity_coord.centery+4))
            self.fenetre.blit(player.image_SE, player.entity_coord)
        elif player.direction_sight=="SW":
            self.fenetre.blit(player.bow_SW, (player.entity_coord.centerx-38,player.entity_coord.top+42))
            self.fenetre.blit(player.image_SW, player.entity_coord)
        elif player.direction_sight=="NW":
            self.fenetre.blit(player.bow_NW, (player.entity_coord.centerx-40,player.entity_coord.top+5))
            self.fenetre.blit(player.image_NW, player.entity_coord)
        elif player.direction_sight=="N":
            self.fenetre.blit(player.bow_N, (player.entity_coord.left+15,player.entity_coord.top-4))
            self.fenetre.blit(player.image_N, player.entity_coord)
        elif player.direction_sight=="S":
            self.fenetre.blit(player.bow_S, (player.entity_coord.left+15,player.entity_coord.bottom-10))
            self.fenetre.blit(player.image_S, player.entity_coord)
        elif player.direction_sight=="W":
            self.fenetre.blit(player.bow_W, (player.entity_coord.centerx-43,player.entity_coord.top+15))
            self.fenetre.blit(player.image_W, player.entity_coord)
        elif player.direction_sight=="E":
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

        self.score = 0
        
        self.entity= self.image_S
        
        if int(nplayer)==1: 
            pos_spawn = (64+32,64+32)
        elif int(nplayer)==2:
            pos_spawn = (1152+32,640+32)
        elif int(nplayer)==3:
            pos_spawn = (1152+32,64+32)
        elif int(nplayer)==4:
            pos_spawn = (64+32,640+32)

        self.nplayer=nplayer
        self.entity_coord=self.entity.get_rect(center=pos_spawn)
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
        self.direction_modif = True 
        self.speed_dash = [30,30]
        self.speed_dash_diagonale = [20,20]
        self.canDash = True
        self.debutDash=-1
        self.direction_sight = "N"
        self.speedManag=[0,2,4,6,8]
        self.speedCount=0
        self.debutSlow=-1
        self.debutRoot=-1
        self.debutFire=-1
        self.iceState=False
        self.earthState=False
        self.fireState=False
        self.stateDot=0
        self.DamageDotTaken=False
        
    def speedGestion(self, ratio):
        if ratio==0:
            self.speedManag=[]
        elif ratio==1:
            self.speedManag=[5]
        elif ratio==2:
            self.speedManag=[2,7]
        elif ratio==3:
            self.speedManag=[2,5,8]
        elif ratio==4:
            self.speedManag=[1,4,6,8]
        elif ratio==5:
            self.speedManag=[0,2,4,6,8]
        elif ratio==6:
            self.speedManag=[0,2,4,6,7,9]
        elif ratio==7:
            self.speedManag=[0,2,4,5,6,7,8]
        elif ratio==8:
            self.speedManag=[0,1,2,4,5,7,8,9]
        elif ratio==9:
            self.speedManag=[0,1,2,3,4,5,7,8,9]
        
    def movement(self):
        #si il est toujours entrain de dash
        if self.isDashing and (pygame.time.get_ticks()-self.debutDash)<50:
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
        
        if self.controler.get_axis( 4 ) < -0.350 and self.controler.get_axis( 3 ) > 0.350:
            
            
            self.shoot_arrow("SW")
            self.direction_sight="SW"
            
        elif self.controler.get_axis( 4 ) < -0.350 and self.controler.get_axis( 3 )< -0.350:
            
            self.shoot_arrow("NW")
            self.direction_sight="NW"
            
        elif self.controler.get_axis( 4 ) > 0.350 and self.controler.get_axis( 3 ) > 0.350:
            
            self.shoot_arrow("SE")
            self.direction_sight="SE"
            
        elif self.controler.get_axis( 4 ) > 0.350 and self.controler.get_axis( 3 )< -0.350:
            
            self.shoot_arrow("NE")
            self.direction_sight="NE"
            
        elif self.controler.get_axis( 4 ) < -0.500:
            
            self.shoot_arrow("W")
            self.direction_sight="W"
           
        elif self.controler.get_axis( 4 ) > 0.500:
            
            self.shoot_arrow("E")
            self.direction_sight="E"
            
        elif self.controler.get_axis( 3 ) > 0.500:
            
            self.shoot_arrow("S")
            self.direction_sight="S"
            
        elif self.controler.get_axis( 3 )< -0.500:
            
            self.shoot_arrow("N")
            self.direction_sight="N"
        else:
            self.direction_sight=self.direction
            self.shoot_arrow(self.direction)
            
            
            
    def shoot_arrow(self,direction):
        if self.controler.get_axis( 2 ) < -0.700 and self.can_shoot:
            if(len(self.combo_inc)==2):
                if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X"):
                    arrow = Arrow(self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                else:
                   self.combo_inc = []
            elif(len(self.combo_inc)==3):
                if(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="B"):
                    arrow = Arrow_fire(self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="X"):
                    arrow = Arrow_ice(self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="A"):
                    arrow = Arrow_earth(self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                elif(self.combo_inc[0]=="Y" and self.combo_inc[1]=="X" and self.combo_inc[2]=="Y"):
                    arrow = Arrow_thunder(self.entity.get_rect(center=(self.entity_coord.centerx,self.entity_coord.centery)),direction)
                else:
                   self.combo_inc = []
            else:
                self.combo_inc = []
                #arrow_entity = pygame.transform.scale(arrow_entity,(64,64))
            if (len(self.combo_inc)==2 or len(self.combo_inc)==3):
                

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
            if sqrt((target_x-x)**2+(target_y-y)**2)<=r:
                return True
            else:
                return False



    def touchRectangle(self,target_x,target_y,size_x,size_y,x,y):
               
        if abs(x-target_x)<=(size_x/2) and abs(y-target_y)<=(size_y/2):
            return True
        else:
            return False

    def dash(self):
            self.debutDash=pygame.time.get_ticks()
            self.isDashing = True
            self.canDash=False

    def statementEffect(self):
        
        if self.debutSlow!=-1:
            if self.iceState:
                if self.debutSlow+2000<pygame.time.get_ticks():
                    self.speedGestion(5)
                    self.iceState=False
                else:
                    self.speedGestion(3)
                    
        if self.debutRoot!=-1:           
            if self.earthState:
                if self.debutRoot+1000<pygame.time.get_ticks():
                    self.speedGestion(5)
                    self.earthState=False
                else:
                    self.speedGestion(0)

        if self.debutFire!=-1:
            if self.fireState:
                sec=5
                if pygame.time.get_ticks()<self.debutFire+sec*1000:
                    
                    if self.debutFire+self.stateDot*1000<pygame.time.get_ticks():
                        self.DamageDotTaken=True
                    else:
                        self.DamageDotTaken=False
                    if pygame.time.get_ticks()<self.debutFire+(self.stateDot+1)*1000 and self.DamageDotTaken:
                        self.hp=self.hp-1
                        self.stateDot=self.stateDot+1
                        self.DamageDotTaken=False
                    else:
                        self.DamageDotTaken=True
                else:
                    self.stateDot=0
                    self.fireState=False    
                       
                    
######################################################################################################################################################################################################

class Arrow():
    def __init__(self,entity_coord_temp,direction):
        self.damage=10
        self.entity=pygame.image.load("./image/arrow/simple/arrow_simple_" + direction + ".png").convert_alpha()
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
    def __init__(self,entity_coord_temp,direction):
        self.damage=8
        Arrow.__init__(self,entity_coord_temp,direction)
        self.entity=pygame.image.load("./image/arrow/fire/arrow_fire_" + direction + ".png").convert_alpha()

    def effect(self, player):
        player.hp=player.hp-self.damage
        player.debutFire=pygame.time.get_ticks()
        player.fireState=True
        

######################################################################################################################################################################################################

class Arrow_ice(Arrow):
    def __init__(self,entity_coord_temp,direction):
        self.damage=5
        Arrow.__init__(self,entity_coord_temp,direction)
        self.entity=pygame.image.load("./image/arrow/ice/arrow_ice_" + direction + ".png").convert_alpha()

    def effect(self, player):
        player.hp=player.hp-self.damage
        player.debutSlow=pygame.time.get_ticks()
        player.iceState=True
        
    
######################################################################################################################################################################################################

class Arrow_earth(Arrow):
    def __init__(self,entity_coord_temp,direction):
        self.damage=5
        Arrow.__init__(self,entity_coord_temp,direction)
        self.entity=pygame.image.load("./image/arrow/earth/arrow_earth_" + direction + ".png").convert_alpha()

    def effect (self, player):
        player.hp=player.hp-self.damage
        player.debutRoot=pygame.time.get_ticks()
        player.earthState=True

######################################################################################################################################################################################################

class Arrow_thunder(Arrow):
    def __init__(self,entity_coord_temp,direction):
        self.damage=6
        Arrow.__init__(self,entity_coord_temp,direction)
        self.entity=pygame.image.load("./image/arrow/thunder/arrow_thunder_" + direction + ".png").convert_alpha()
        self.speed=(9,9)
        self.speed_diagonale=(6,6)
    

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
        self.map_mini_grid_elemn = []
        
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
    
                if map_grid_AllList[self.get_Level()][i][j] == 0:
                    self.map_mini_grid_elemn.append(ElementUnbreakable(319+j*32,192+i*32,"mini"))
                elif map_grid_AllList[self.get_Level()][i][j] == 2:
                    self.map_mini_grid_elemn.append(ElementBreakable(319+j*32,192+i*32,3,"mini"))
                elif map_grid_AllList[self.get_Level()][i][j] == 3:
                    self.map_mini_grid_elemn.append(ElementBreakable(319+j*32,192+i*32,2,"mini"))
                elif map_grid_AllList[self.get_Level()][i][j] == 4:
                    self.map_mini_grid_elemn.append(ElementBreakable(319+j*32,192+i*32,1,"mini"))
                elif map_grid_AllList[self.get_Level()][i][j] == 5:
                    self.map_mini_grid_elemn.append(ElementPassThrough(319+j*32,192+i*32,"mini"))
    # Retourne la grid
    def get_grid(self):
        return self.map_grid_elem

    # Retourne le next level
    def get_Level(self):
        return self.level

    def map_mini_grid_elemn(self):
        return self.map_mini_grid_elemn


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
