# -*- coding: utf-8 -*-

import os, sys

from defineOptions import options

# NOTICE: Automatic text wrapping is disabled due to position issues, please use multiline strings if text is too long for the monitor used
# --------------------------
# Introduction screen
# --------------------------

# -------
# General
# -------
introContinue = "Appuyez sur l'espace/pouce pour continuer."

# ----------
# Intro text
# ----------	
	
'''
Nested tuples, each tuple is a new page during the introduction text phase
'''
training_fam = (("Cher/chère participant,\n\nmerci de participer à notre étude. Nous voulons savoir\ncomment les gens apprennent à trouver leur chemin dans un environnement inconnu.\n\n" +"Pour cela, vous vous déplacerez dans un environnement virtuel, qui représente\nune ville allemande typique. Les environs se composent de différentes rues et\nintersections, ainsi que de la mairie et de l'église de la ville." + " Votre travail consistera à pointer\nà partir de certains endroits dans les directions  où se trouvent ces bâtiments. Vous\naurez aussi l'ocassion de vous familiariser avec l'environnement."+ "\n\nL'expérience prendra environ une heure.\n"),

("La première chose est d'apprendre à connaître l'environnement\n\nVous pouvez utiliser les quatre touches fléchées (haut, bas, gauche et droite) pour vous déplacer dans la ville:" +"\n\nVotre tâche est de collecter\n\n les boules rouges au bout des rues\net mémoriser les emplacements de l'église et de la mairie." +"\nS'il vous plaît, faites attention aux intersections que vous traversez." +"\n\nNous vous demanderons également de dessiner une carte de l'environnement à la fin de l'expérience."))

'''
Nested tuples, each tuple is a new page during the introduction text phase. The second page is generated seperately in the run.py
'''
training_prac = (("Maintenant vous devez vous familiariser avec la tâche\nque vous effectuerez au scanner.\n\nVous serez d'abord déplacé dans l'environnement virtuel\nà partir d'une rue jusqu'au milieu d'une intersection.\n\n" + "Une fois que vous vous arrêtez et qu'une croix aérienne apparaît, pointez\nvers la mairie, l'église ou le bâtiment de l'intersection qui est bleu ou assombri\nselon le bâtiment qui est affiché en bas de l'écran."),
("Veuillez toujours essayer de pointer vers le centre du bâtiment (quel que soit le parcours\nsur les routes). Pour ce faire, déplacez le réticule dans la direction\nappropriée et confirmez avec le bouton espace/pouce\n" + "\nCette partie de la tâche n'est pas une question de précision.\nIl s'agit d'apprendre à connaître la tâche"))
	fmri_prac = ("Comme vous l'avez fait en dehors du scanner,\nvous allez répéter la tâche brièvement.\n\nVeuillez pointer à nouveau le bâtiment (église, mairie, bâtiment bleu)\ndès que le réticule apparaît, et gardez vos doigts sur les boutons pendant la mesure.")
	
'''
Nested tuples, each tuple is the text corresponding to the set feedback mode in defineOptions.py
'''	fmri_test = ("Maintenant nous commençons l'expérience principale\n\n Comme avant, le but est de pointer dans la direction du bâtiment représenté.\n\n" + "Il est important que vous essayiez de répondre le plus rapidement et le plus précisément possible.\n\n" + "La nouveauté, c'est qu'après un certain nombre d'essais,\nvous aurez visité toutes les rues du quartier.\nCela vous donnera une meilleure impression de l'environnement."+ "\n\nA la fin de l'expérience, nous vous demanderons de dessiner une carte de l'environnement."'\n\nBon courage!')
	
# ----------------------
# Procedual text German
# ----------------------
partEnded = 'Super!'
expEnd = "Fini!\n\nMerci beaucoup d'avoir participé."
targetText = [["S'il vous plaît, pointez\ndu doigt la mairie."],["S'il vous plaît, pointez\ndu doigt l'église."],["S'il vous plaît, pointez\nvers le bâtiment de l'intersection."]]
missedPointing = "Trop lent ! Répondez plus vite."
pauseText = '+'
tutorialOver = "Et maintenant, sans aide."tutorialMoveForward = "Vous êtes sur le point d'arriver au milieu de l'intersection."tutorialRotate = "Veuillez déplacer le réticule vers la gauche ou la droite pour pointer vers le bâtiment affiché ci-dessous."tutorialDecide = "Appuyez sur l'espace pour confirmer."
# ---------------------------
# Form strings & dictionaries
# ---------------------------

introText = (training_fam, training_prac, fmri_prac, fmri_test)

procedualText = {'introContinue':introContinue,'expEnd':expEnd, 'partEnded':partEnded, 'targetText':targetText, 'missedPointing':missedPointing, 'pauseText':pauseText, 'tutorialOver':tutorialOver, 'tutorialMoveForward': tutorialMoveForward,'tutorialRotate':tutorialRotate, 'tutorialDecide':tutorialDecide}