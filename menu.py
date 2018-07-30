# -*- coding:Utf-8 -*-
from class_file import *
from menu import *
from classes import *
#importation de pygame
import pygame
from pygame.locals import *
#importation de la bibliothï¿½que system
import sys
import random

#importation du mixer pour gï¿½rer la musique
import pygame.mixer

class Menu():
    def __init__(self,screen,controler):
        self.image_menu= pygame.image.load("./image/main_menu/menu.png").convert_alpha()
        self.screen=screen
        self.controler=controler[0]
        screen.blit(self.image_menu,(0,0))
        self.image_cursor = pygame.image.load("./image/main_menu/cursor.png").convert_alpha()
        screen.blit(self.image_cursor,(328,328))
        self.pos=0
        self.button_up = True
        self.joysticks=controler
        
        
    def refresh_menu(self):
        self.screen.blit(self.image_menu,(0,0))
        self.screen.blit(self.image_cursor,(328,328+(self.pos*110)))
        self.controler_action()   
    def controler_action(self):
        if (self.controler.get_hat( 0 )[1]==0):
            self.button_up = True
        
        elif(self.controler.get_hat( 0 )[1]==-1 and self.button_up):
            if(self.pos==2):
                self.pos=0
            else: 
                self.pos=self.pos+1
            self.button_up = False
        elif self.controler.get_hat( 0 )[1]==1 and self.button_up:
            if(self.pos==0):
                self.pos=2
            else: 
                self.pos=self.pos-1
            self.button_up = False

    
    def button_pressed(self,old):
        if self.controler.get_button(0)==1:
            if self.pos==0:
                return 0
            elif self.pos==1:
                return 1
            elif self.pos==2:
                return 2
            elif self.pos==3:
                return 3
        elif self.controler.get_button(1)==1:
            return -1
        else:
            return old
            
    def rules(self):
        image_rules= pygame.image.load("./image/main_menu/rules.png").convert_alpha()
        self.screen.blit(image_rules,(0,0))
        
    def credit(self):
        image_credit= pygame.image.load("./image/main_menu/credit.png").convert_alpha()
        self.screen.blit(image_credit,(0,0))



    

    
    def quit_game(self):
        pygame.quit()
        sys.exit()
            
    def caracter_selection(self):
        caracter_selection = Caracter_selection(self.screen)
        while True :
            
            for event in pygame.event.get():
                if event.type == QUIT:      #si l'utilisateur clique sur la croix
                    pygame.quit()
                    sys.exit()
            
            if self.joysticks[0].get_button(1)==1 and caracter_selection.cursors[0].lock==False and caracter_selection.cursors[0].button_B_up:  
                return-1
            else:
                caracter_selection.caracter_selection_refresh()
            
            pygame.display.flip()
            pygame.time.wait(5)
            
        
            
            

class Caracter_selection():
    def __init__(self,screen):
        self.joysticks= self.load_controller()
        self.cursors = self.caracter_selection_load_cursor_player(len(self.joysticks))
        self.image_selection= pygame.image.load("./image/main_menu/caracter_selection.png").convert_alpha()
        self.list_skin = [True,True,True,True]
        self.screen=screen
        self.image_cross=pygame.image.load("./image/main_menu/red_cross.png")
        self.image_all_ready=pygame.image.load("./image/main_menu/image_all_ready.png")
        
    def caracter_selection_load_cursor_player(self,nb_player):
        cursors = []
        for i in range (0,nb_player):
            cursors.append(Cursor_player_selection(i))
        return cursors
    
    def load_controller(self):
        joysticks = []
        pygame.joystick.init()
        for i in range(0, pygame.joystick.get_count()):
            joysticks.append(pygame.joystick.Joystick(i))
            joysticks[-1].init()
        return joysticks
    
    def caracter_selection_refresh(self):
        self.screen.blit(self.image_selection,(0,0))
        for i in self.cursors:
            self.screen.blit(i.image,i.get_pos())
        for i in range (0,4):
            if not self.list_skin[i]:
                self.screen.blit(self.image_cross,(270+i*270,255))
        if self.is_all_lock():
                self.screen.blit(self.image_all_ready,(0,650))
        self.controler_action_player_selection(self.cursors,self.joysticks)

    def is_all_lock(self):
        nb_lock=0
        for i in range (0,len(self.cursors)):
            if self.cursors[i].lock :
                nb_lock=nb_lock+1
        return nb_lock==len(self.cursors)
        

    def controler_action_player_selection(self,cursors,joysticks):
        for i in cursors:
            if (joysticks[i.indice].get_hat( 0 )[0]==0):
                i.button_up = True
        
            if (joysticks[i.indice].get_button(0)==0):
                i.button_A_up = True
                
            if (joysticks[i.indice].get_button(1)==0):
                i.button_B_up = True
                
            if(joysticks[i.indice].get_hat( 0 )[0]==1 and i.button_up and not i.lock):
                
                i.choix= (i.choix+1)%4
                
                while not self.list_skin[(i.choix)%4] :
                    
                    i.choix= (i.choix+1)%4
                
                i.button_up = False
            elif joysticks[i.indice].get_hat( 0 )[0]==-1 and i.button_up and not i.lock: 
                
                i.choix= i.choix-1
                if i.choix==-1:
                    i.choix=3
                    
                while not self.list_skin[(i.choix)] :
                    i.choix= i.choix-1
                    if i.choix==-1:
                        i.choix=3
                
                i.button_up = False
            if joysticks[i.indice].get_button(0)==1 and not i.lock and i.button_A_up and self.list_skin[i.choix]:
                i.lock=True
                self.list_skin[i.choix]=False
                i.button_A_up = False
            elif joysticks[i.indice].get_button(1)==1 and i.lock and i.button_B_up:
                i.lock=False
               
                i.button_B_up=False
                self.list_skin[i.choix]=True
            elif joysticks[i.indice].get_button(7)==1 and self.is_all_lock():
                map_selection = Map_selection(self.screen,self.cursors,self.joysticks)
                while self.joysticks[0].get_button(1)==0 :
                    for event in pygame.event.get():
                        if event.type == QUIT:      #si l'utilisateur clique sur la croix
                            pygame.quit()
                            sys.exit()
                    map_selection.map_selection_refresh()
                    pygame.display.flip()
                    pygame.time.wait(5)
                
            

            
    

class Map_selection():
    def __init__(self,screen,cursors,joysticks):
        self.joysticks=joysticks
        self.screen=screen
        self.cursors=cursors
        self.img_background=pygame.image.load("./image/main_menu/map_selection.png")
        self.texture = TexturesListCheck()
        nbErreur = self.texture.checkExistBlock()
        self.packTexture = self.texture.get_TexturesFolderBlock()
        self.nb_choix = 0
        self.map_choose=Map(self.packTexture[0],self.nb_choix)


    def map_selection_refresh(self):
        self.screen.blit(self.img_background,(0,0))
        for i in range (0,len(self.map_choose.map_grid_elem)): 
            self.screen.blit(self.map_choose.map_mini_grid_elemn[i].get_image(), (self.map_choose.map_mini_grid_elemn[i].pos_x,self.map_choose.map_mini_grid_elemn[i].pos_y))
        self.controler_map_selection()

    def controler_map_selection(self):
            if (self.joysticks[0].get_hat( 0 )[0]==0):
                self.cursors[0].button_up = True
      
            if self.joysticks[0].get_hat( 0 )[0]==1 and self.cursors[0].button_up:
                self.nb_choix= self.nb_choix+1
                if self.nb_choix==5:
                    self.nb_choix=0
                self.map_choose=Map(self.packTexture[0],self.nb_choix)
                self.cursors[0].button_up = False
            elif self.joysticks[0].get_hat( 0 )[0]==-1 and self.cursors[0].button_up: 
                
                self.nb_choix= self.nb_choix-1
                if self.nb_choix==-1:
                    self.nb_choix=4
                self.map_choose=Map(self.packTexture[0],self.nb_choix)
                self.cursors[0].button_up = False
            if self.joysticks[0].get_button(0)==1:
                game = Game(self.screen,self.cursors,self.joysticks,self.map_choose)
                while 1:
                   
                    for event in pygame.event.get():
                        if event.type == QUIT:      #si l'utilisateur clique sur la croix
                            pygame.quit()
                            sys.exit()
                    game.refreshGame()
                    pygame.display.flip()
                    pygame.time.wait(5)
                
        

                
class Cursor_player_selection():
    def __init__(self,indice):
        self.indice=indice
        self.choix=0
        self.image=pygame.image.load("./image/main_menu/cursor/cursor_"+str(indice)+".png").convert_alpha()
        self.pos=(125+self.indice*52+self.choix*270,455)
        self.lock=False
        self.button_A_up = False
        self.button_B_up = False
        self.button_up = True
    def get_pos(self):
        return (125+self.indice*52+self.choix*270,455)
