## -*- coding: utf-8 -*-

import pygame
from random import randint,choice
from time import time

pygame.init() # initialisation du module "pygame"

fenetre = pygame.display.set_mode( (600,600) ) # Création d'une fenêtre graphique de taille 600x600 pixels
pygame.display.set_caption("Harti Kenza") # Définit le titre de la fenêtre


## Chargement des images:
#    On définit et affecte les variables qui contiendront les images du vaisseau ou de l'alien
imageAlien = pygame.image.load("alien.png")
imageVaisseau = pygame.image.load("vaisseau.png")
imageVaisseau = pygame.transform.scale(imageVaisseau, (64, 64)) # On redimensionne l'image du vaisseau à une taille de 64x64 pixels
imageBombe = pygame.image.load("bombe.png")
imageBombe = pygame.transform.scale(imageBombe, (32, 32))
sonProjectile = pygame.mixer.Sound("sons/projectile.wav")
sonAlien = pygame.mixer.Sound("sons/alien.wav")
sonBombe = pygame.mixer.Sound("sons/son_bombe.wav")
sonEtoile = pygame.mixer.Sound("sons/etoile.wav")
sonFin = pygame.mixer.Sound("sons/gameover.wav")
musique = pygame.mixer.Sound("sons/Harder_Better_Faster_Stronger.wav")
imageEtoile=pygame.image.load("etoile.png")
imageCoeur=pygame.image.load("coeur.png")
imageCoeur = pygame.transform.scale(imageCoeur, (32, 32))
score=0
nb_projectile=100
# On définit les variables qui contiendront les positions des différents éléments (vaisseau, alien, projectile)
# Chaque position est un couple de valeur '(x,y)'
positionVaisseau = (300,525)
nbAlien = 5
positionAlien = [(randint(0,567),randint(-10,100)) for i in range(nbAlien)]
positionBombe=False
projectile = []
dsdigit = pygame.font.Font("ds_digital/DS-DIGII.TTF",30)
tps = time()-0.15
rand = [(False,True) for i in range(nbAlien)]
etoiles = [(randint(2,598),randint(2,598)) for i in range(50)]
pvs = 60
dsdigitb = pygame.font.Font("ds_digital/DS-DIGIT.TTF",70)
police_bests = pygame.font.Font("ds_digital/DS-DIGIB.TTF",25)
msgArret=dsdigitb.render("GAME OVER", True, pygame.Color(255, 255, 255))
positionEtoile = False
positionCoeur = False
T=0
F=0
nom = input("Nom (8 caractères max) : ")
bests = []
pygame.mixer.Sound.play(musique)

def dossTxt():
    global texte
    oldScores = open("scores.txt", "r")
    texte = oldScores.readlines()
    rang = 0
    while rang<len(texte) and score < int(texte[rang].split(" : ")[1][:-1]):
        rang += 1
    texte.insert(rang,nom+" : "+ str(score).rjust(4,"0")+"\n")
    oldScores = open("scores.txt", "w")
    for l in texte:
        oldScores.write(l)
    top10()

def top10():
    global bests
    for i in range(9):
        bests.append(str(i+1)+" "*5+texte[i].split(" : ")[0].rjust(8," ")+" : "+texte[i].split(" : ")[1][:-1])
    bests.append(str(10) + " " * 4 + texte[9].split(" : ")[0].rjust(8, " ") + " : " + texte[9].split(" : ")[1][:-1])
# Fonction en charge de dessiner tous les éléments sur notre fenêtre graphique.
# Cette fonction sera appelée depuis notre boucle infinie
def dessiner():
    global imageAlien, imageVaisseau, fenetre, projectile,po
    # On remplit complètement notre fenêtre avec la couleur noire: (0,0,0)
    # Ceci permet de 'nettoyer' notre fenêtre avant de la dessiner
    fenetre.fill( (0,0,0) )
    if drap:
        fenetre.blit(msgArret,(150,100))
        texteScore = dsdigit.render("score : " + str(score), True, pygame.Color(255, 255, 255))
        fenetre.blit(texteScore, (250, 175))
        for top in range(10):
            s = police_bests.render(bests[top], True, pygame.Color(255, 255, 255))
            fenetre.blit(s, (200, 250+25*top))
    else:
        fenetre.blit(imageVaisseau, positionVaisseau) # On dessine l'image du vaisseau à sa position
        for alien in positionAlien:
            fenetre.blit(imageAlien, (alien[0],int(alien[1]))) # On dessine l'image du vaisseau à sa position
        texteScore = dsdigit.render("score : "+str(score),True,pygame.Color(255,255,255))
        texteProjectile=dsdigit.render("Projectiles : "+str(nb_projectile),True,pygame.Color(255,255,255))
        texteVie = dsdigit.render("PV : " + str(pvs), True, pygame.Color(255, 255, 255))
        fenetre.blit(texteScore,(10,10))
        fenetre.blit(texteProjectile,(10,50))
        fenetre.blit(texteVie, (10, 90))
        if positionBombe:
            fenetre.blit(imageBombe,positionBombe)
        if positionEtoile:
            fenetre.blit(imageEtoile, positionEtoile)
        if positionCoeur:
            fenetre.blit(imageCoeur,positionCoeur)
        for point in projectile:
            pygame.draw.circle(fenetre, (255,255,255), point, 5) # On dessine le projectile (un simple petit cercle)
    for etoile in etoiles:
        pygame.draw.circle(fenetre, (255, 255, 255), etoile, 2)
    pygame.display.flip() # Rafraichissement complet de la fenêtre avec les dernières opérations de dessin


# Fonction en charge de gérer les évènements clavier (ou souris)
# Cette fonction sera appelée depuis notre boucle infinie
def gererClavierEtSouris():
    global positionVaisseau, projectile,nb_projectile,tps,drap
    # Gestion du clavier: Quelles touches sont pressées ?

    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_SPACE] == True and nb_projectile>0 and time()-tps >0.15:
        projectile.append((positionVaisseau[0]+32,positionVaisseau[1]))
        pygame.mixer.Sound.play(sonProjectile)
        nb_projectile-=1
        tps = time()
    if touchesPressees[pygame.K_RIGHT] == True and positionVaisseau[0]<600-64:
        positionVaisseau = ( positionVaisseau[0] + 5 , positionVaisseau[1] )
    if touchesPressees[pygame.K_LEFT] == True and positionVaisseau[0]>0:
        positionVaisseau = ( positionVaisseau[0] - 5 , positionVaisseau[1] )

def placeAlien():
    global positionAlien,rand,drap
    for loop in range(len(positionAlien)):
        if not rand[loop][0]:
            if rand[loop][1]:
                rand[loop] = (randint(0,positionAlien[loop][0]),not rand[loop][1])
            else:
                rand[loop] = (randint(positionAlien[loop][0],567), not rand[loop][1])
        if abs(rand[loop][0] - positionAlien[loop][0]) >= 2:
            if rand[loop][1] :
                positionAlien[loop] = (positionAlien[loop][0]+1,positionAlien[loop][1]+0.7)
            else:
                positionAlien[loop] = (positionAlien[loop][0]-1,positionAlien[loop][1]+0.7)
            if positionAlien[loop][1] > 600 or (positionVaisseau[0]-33<=positionAlien[loop][0]<=positionVaisseau[0]+60 and positionVaisseau[1]-27<=positionAlien[loop][1]<=positionVaisseau[1]+60):
                drap = True
                dossTxt()
        else :
            rand[loop] = (False,rand[loop][1])

def videListe():
    global projectile, positionAlien, rand
    while None in projectile:
        projectile.pop(projectile.index(None))
    while None in positionAlien:
        rand.pop(positionAlien.index(None))
        positionAlien.pop(positionAlien.index(None))

def quitter():
    global continuer
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Permet de gérer un clic sur le bouton de fermeture de la fenêtre
            continuer = False

def bonMalus(position):
    global pvs,nb_projectile
    position0 = position
    if position:
        position = (position[0], position[1] + 7)
        if position[1] > 600:
            position = False
        elif positionVaisseau[0] - 32 <= position[0] <= positionVaisseau[0] + 60 and positionVaisseau [1] - 32 <= position[1]:
            position = False
            if position0 == positionBombe:
                pvs -= 20
                pygame.mixer.Sound.play(sonBombe)
            else:
                pygame.mixer.Sound.play(sonEtoile)
                if position0 == positionEtoile:
                    nb_projectile = 100
                else:
                    pvs += 20
    return position
# On crée une nouvelle horloge qui nous permettra de fixer la vitesse de rafraichissement de notre fenêtre
clock = pygame.time.Clock()

# La boucle infinie de pygame:
# On va continuellement dessiner sur la fenêtre, gérer les évènements et calculer certains déplacements
continuer = True
drap = False
while continuer:
    # pygame permet de fixer la vitesse de notre boucle:
    # ici on déclare 50 tours par secondes soit une animation à 50 images par secondes
    clock.tick(50)
    quitter()
    if drap:
        dessiner()
    else :
        dessiner()
        gererClavierEtSouris()
        placeAlien()
        positionBombe = bonMalus(positionBombe)
        positionEtoile = bonMalus(positionEtoile)
        positionCoeur = bonMalus(positionCoeur)
        # On fait avancer le projectile (si il existe)
        for point in range(len(projectile)):
            projectile[point] = (projectile[point][0], projectile[point][1] - 5) # le projectile "monte" vers le haut de la fenêtre
            for alien in range(len(positionAlien)):
                if projectile[point] != None and positionAlien[alien]:
                    if positionAlien[alien][0]<=projectile[point][0]<=positionAlien[alien][0]+33 and positionAlien[alien][1]<=projectile[point][1]<=positionAlien[alien][1]+27:
                        projectile[point]=None
                        positionAlien[alien]=None
                        pygame.mixer.Sound.play(sonAlien)
                        score+=1
                    elif projectile[point][1]<0:
                        projectile[point]=None
        videListe()
        tpsAlien = time()
        if int(tpsAlien*100)%10 == 0 or int(tpsAlien*100)%10 == 1:
            if int(tpsAlien * 10) % 10 == 0:
                if positionAlien != [] and int(tpsAlien) % 2 == 0:
                    positionBombe = positionAlien[randint(0,len(positionAlien)-1)]
                if int(tpsAlien) % 8 == 0:
                    if (choice([True,False])and T<2) or F == 2:
                        F=0
                        T += 1
                        positionEtoile = (randint(0,568),0)
                    else:
                        T=0
                        F += 1
                        positionCoeur = (randint(0,568),0)

                positionAlien.append((randint(0, 567), -10))
                rand.append((False, True))
            elif int(tpsAlien * 10) % 10 == 5:
                positionAlien.append((randint(0, 567), -10))
                rand.append((False, True))
        if pvs <= 0:
            drap = True
            dossTxt()
            pygame.mixer.pause()
            pygame.mixer.Sound.play(sonFin)
    for place in range(len(etoiles)):
        etoiles[place] = (etoiles[place][0], etoiles[place][1] + 1)
        if etoiles[place][1] > 600:
            etoiles[place] = (randint(2, 600), 1)

    ## A la fin, lorsque l'on sortira de la boucle, on demandera à Pygame de quitter proprement
pygame.quit()