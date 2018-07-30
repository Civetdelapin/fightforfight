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



pygame.init()

fenetre  = pygame.display.set_mode((1280,768))

clock = pygame.time.Clock()
can_shoot = True
pygame.mixer.music.load('./music.mp3')
pygame.mixer.music.play(-1)


joysticks = []
# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    #print "Detected joystick "+joysticks[-1].get_name()+""


if pygame.joystick.get_count()==0:
    image_no_controler=pygame.image.load("./image/main_menu/no_controler.png").convert_alpha()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:      #si l'utilisateur clique sur la croix
                pygame.quit()
                sys.exit()
        fenetre.blit(image_no_controler,(0,0))
        pygame.display.flip()
        pygame.time.wait(5)
else:
    menu = Menu(fenetre,joysticks)

    ##import random 
    #texture = TexturesListCheck()
    #nbErreur = texture.checkExistBlock()


    #game = Game(fenetre,pygame.joystick.get_count(),joysticks,packTexture[random.randint(0,len(packTexture)-1)])  #mettre un random pour faire de la diversité pour les textures

    pygame.key.set_repeat(20,20)


    #boucle infinie pour affichage permanent de la fenï¿½tre
    menu_controler=-1
    while 1:
        
        for event in pygame.event.get():
            if event.type == QUIT:      #si l'utilisateur clique sur la croix
                pygame.quit()
                sys.exit()
        menu_controler=menu.button_pressed(menu_controler)
        if menu_controler==0:
            menu_controler=menu.caracter_selection()
        elif menu_controler==1:
            menu.rules()
        elif menu_controler==2:
            menu.credit()
        elif menu_controler==-1:
            menu.refresh_menu()
        #game.movementGame()
        pygame.display.flip()
        pygame.time.wait(5)



