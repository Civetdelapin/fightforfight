# -*- coding:Utf-8 -*-
from classes import *
#importation de pygame
import pygame
from pygame.locals import *
#importation de la bibliothèque system
import sys
#importation du mixer pour gérer la musique
import pygame.mixer
import random
pygame.init()

#Creation de la fenetre de jeu
fenetre  = pygame.display.set_mode((1280,768))


clock = pygame.time.Clock()
#can_shoot = True

joysticks = []

#Pour tous les joysticks connectés
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print "Detected joystick '",joysticks[-1].get_name(),"'"

texture = TexturesListCheck()
nbErreur = texture.checkExistBlock()
if nbErreur == 0:
    print "Chargement des textures ok"
else:
    print nbErreur
    #print "Erreur(s) de texture:"
    #print texture.get_TexturesFolder()
    #Afficher un message d'erreur

packTexture = texture.get_TexturesFolderBlock()
game = Game(fenetre,pygame.joystick.get_count(),joysticks,packTexture[random.randint(0,len(packTexture)-1)])  #mettre un random pour faire de la diversité pour les textures
#????????????????????????
pygame.key.set_repeat(20,20)

#boucle infinie pour affichage permanent de la fenêtre
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:      #si l'utilisateur clique sur la croix
            pygame.quit()
            sys.exit()
    game.refreshGame()
    pygame.display.flip()  #????????????????????????
    pygame.time.wait(5)    #????????????????????????
