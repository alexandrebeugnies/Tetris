# -*- coding: utf-8 -*-

import random
import time
import pygame
import sys
from pygame.locals import *

from constantes import *

PIECES = {
    'O':{
        '0000\n0110\n0110\n0000',
    },
    'S':{
        '0000\n0022\n0220\n0000',
        '0000\n0200\n0220\n0020',
    },
    'Z':{
        '0000\n3300\n0330\n0000',
        '0000\n0030\n0330\n0300',
    },
    'I':{
        '0400\n0400\n0400\n0400',
        '0000\n4444\n0000\n0000',
    },
    'J':{
        '0000\n5000\n5550\n0000',
        '0000\n0550\n0500\n0500',
        '0000\n0000\n5550\n0050',
        '0000\n0050\n0050\n0550',
    },
    'L':{
        '0000\n0060\n6660\n0000',
        '0000\n0060\n0060\n0660',
        '0000\n0000\n6660\n6000',
        '0000\n0660\n0060\n0060',
    },
    'T':{
        '0000\n0700\n7770\n0000',
        '0000\n0700\n0770\n0700',
        '0000\n0060\n7770\n0700',
        '0000\n0070\n0770\n0070',
    },
},

COULEURS = {
      0: (0, 0, 0),
      1: (255, 255 , 0),
      2: (0, 255, 0),
      3: (255, 0, 0),
      4: (0, 255, 255),
      5: (0, 0, 255),
      6: (255, 127, 0),
      7: (255, 0, 255),
      8: (127, 255, 0),
      9: (255, 255, 255)
      
}

for k,v in PIECES.items():
    print(k)
    for p in v:
            print (p, '\n')

for name, rotations in PIECES.items():
      PIECES[name] = [[[int(i) for i in p] for p in r.splitlines()] for r in rotations] 

TAILLE_FENETRE = 640, 480
DIM_PLATEAU = 10, 20
BORDURE_PLATEAU = 4
TAILLE_BLOC = 20, 20

TAILLE_PLATEAU = tuple([DIM_PLATEAU[i]*TAILLE_BLOC[i] for i in range(2)])
TAILLE_PLABORD = tuple([DIM_PLATEAU[i]*TAILLE_BLOC[i] + BORDURE_PLATEAU*2 for i in range(2)])

MARGE = tuple([TAILLE_FENETRE[i]-TAILLE_PLATEAU[i]-BORDURE_PLATEAU*2 for i in range(2)])
START_PLATEAU = int (MARGE[0]/2), MARGE[1]+2*BORDURE_PLATEAU
START_PLABORD = int (MARGE[0]/2)-BORDURE_PLATEAU,MARGE[1]+BORDURE_PLATEAU

CENTRE_FENETRE = tuple([TAILLE_FENETRE[i]/2 for i in range(2)])
POS = CENTRE_FENETRE[0], CENTRE_FENETRE[1]+100
POSITION_SCORE = TAILLE_FENETRE[0] - START_PLABORD[0]/2, 120
POSITION_PIECES = POSITION_SCORE[0], 150
POSITION_LIGNES = POSITION_SCORE[0], 180
POSITION_TETRIS = POSITION_SCORE[0], 210
POSITION_NIVEAU = POSITION_SCORE[0], 240

GRAVITE = 0.35

class Jeu(object):
      def __init__(self):
            pygame.init()
            self.clock = pygame.time.Clock()
            self.surface = pygame.display.set_mode(TAILLE_FENETRE)
            self.fonts = {
                  'defaut': pygame.font.Font('freesansbold.ttf', 18),
                  'titre': pygame.font.Font('freesansbold.ttf', 100),
            }
            pygame.display.set_caption('Tetris Game')
            
            def start(self):
                  self._afficherTexte('Tetris', CENTRE_FENETRE, font='titre')
                  self._afficherTexte('Appuyer sur une touche ...', POS)
                  self._attente()

            def stop(self):
                  self._afficherTexte('Perdu', CENTRE_FENETRE, font='titre')
                  self._attente()
                  self._quitter()
            
            def _afficherTexte(self, text, position, couleur=9, font='defaut'):
                  print("Afficher Texte")
                  font = self.fonts.get(font, self.fonts['defaut'])
                  couleur = COULEURS.get(couleur, COULEURS[9])
                  rendu = font.render(text, True, couleur)
                  rect = rendu.get_rect()
                  rect.center = position
                  self.surface.blit(rendu, rect)
            
            def _attente(self):
                  print("Attente")
                  while self._getEvent()== None:
                        self._rendre()
            def _rendre(self):
                  pygame.display.update()
                  self.clock.tick()
            
            def _getEvent(self):
                  for event in pygame.event.get():
                        if event.type == QUIT:
                              self._quitter()
                        if event.type == KEYUP:
                              if event.type == K_ESCAPE:
                                    self._quitter()
                        if event.type == KEYDOWN:
                              if event.key == K_ESCAPE:
                                    continue
                              return event.key
                        
            def _quitter(self):
                  print("Quitter")
                  pygame.quit()
                  sys.exit()
        
            def _getPiece(self):
                  return PIECES.get(random.choice(PIECES_KEYS))
            def _getCurrentPieceColor(self):
                  for l in self.current[0]:
                        for c in l:
                              if c != 0:
                                    return c
                              
            def _calculerDonneesPieceCourante(self):
                  m = self.current[self.position[2]]
                  coords = []
                  for i, l in enumerate(m):
                        for j, k in enumerate(l):
                              if k != 0:
                                    coords.append([i+self.position[0], j+self.position[1]])
                        self.coordonnees = coords 
            
            def _estValide(self, x=0, y=0, r=0 ):
                  max_x, max_y = DIM_PLATEAU
                  if r == 0:
                        coordonnees = self.coordonnees
                  else:
                        m = self.current[(self.position[2]+r) %len(self.current)]
                        coords =[]
                        for i, l in enumerate(m):
                              for j, k in enumerate(l):
                                    if k != 0:
                                        coords.append([i+self.position[0], j+self.position[1]])
                                        coordonnees = coords
                                        # print("Rotation testee : %s" % coordonnees) 
                                    for cx, cy in coordonnees:
                                          if not 0 <= x + cx < max_x:
                                                #print("Non valide en X: cx=%s, x=%s" % (cx, x))
                                                return False
                                          elif cy < 0:
                                                continue
                                          


                              


