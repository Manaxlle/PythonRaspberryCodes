# Importation des librairies
import os
import feedparser
import requests
import shutil
import csv
from bs4 import BeautifulSoup
import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
from time import sleep
import apds9960 as GestureSensor
from apds9960_constants import *
from gpiozero import DigitalInputDevice 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from ColorCube import ColorCube
from PIL import Image
cc = ColorCube(avoid_color=[255, 255, 255])
# sudo pip3 install google_images_download
# http:www.github.com/hardikvasa/google-images-download  pour un lien vers la doc de l'API
from google_images_download import google_images_download

import spidev

DC = 22
RST = 25
LED = 23

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

# Initialisation de l'écran
TFT.initLCD(DC, RST, LED)

zone_ecran = TFT.draw()
TFT.clear((255,255,255))

# Nombre d'images à télécharger
NB_IMG = 15

# Creation du dossier 'google_search' s'il n'existe pas
if not os.path.exists("google_search") :
    os.makedirs("google_search")

# Effacement de tous les fichiers du dossier 'google_search'
try :
    fichiers_presents = [ f for f in os.listdir("google_search")]
    for f in fichiers_presents:
        os.remove(os.path.join("google_search", f))
except FileNotFoundError :
    print("...")

# Instantiation de l'objet 'google'
reponse = google_images_download.googleimagesdownload()

# Demande des mots clefs à l'utilisateur
mots_clefs = input("Quels mots clefs souhaitez-vous pour votre recherche ? ")

# Récupération des images du résultat de la recherche
absolute_image_paths = reponse.download({"keywords":mots_clefs,"limit":NB_IMG,"format":"jpg","output_directory":"google_search","no_directory":'1'})

# renommer les images en changeant le nom web en index uniquement (ex: '8.jpg')
global i
i=0
for f in os.listdir("google_search") :
    os.rename("google_search/"+f,"google_search/"+str(i)+".jpg")
    i+=1
    
for i in range(NB_IMG):
    resultat = Image.open('google_search/'+str(i)+'.jpg')
    resultat = resultat.rotate(-90, expand = True)
    if resultat.size[0] >= resultat.size[1]:
        resultat.thumbnail((220,220))
    else:
        resultat.thumbnail((300,300))
    resultat.save('google_search/'+str(i)+'.jpg')

SENSOR_INTERRUPT = 4

i= 0
TFT.clear((255,255,255))
zone_ecran.pasteimage('google_search/'+str(i)+'.jpg',(0,0))
TFT.display()
# Fonction d'interruption permettant de lire le geste qui s'est produit
def Lecture_geste():
    global i
    while capteur_APDS9960.isGestureAvailable():
        geste=capteur_APDS9960.readGesture()
        if geste == Directions.DIR_LEFT:
            print ("Gauche")
            i = i-1
            if i == -1:
                i = NB_IMG-1
            TFT.clear((255,255,255))
            zone_ecran.pasteimage('google_search/'+str(i)+'.jpg',(0,0))
            TFT.display()
            colors = cc.get_colors('google_search/'+str(i)+'.jpg')
            print ("couleur dominante R : {}".format(colors[0][0]))
            print ("couleur dominante G : {}".format(colors[0][1]))
            print ("couleur dominante B : {}".format(colors[0][2]))
            
        if geste == Directions.DIR_RIGHT:
            print ("Droit")
            i = i+1
            if i == NB_IMG:
                i = 0
            TFT.clear((255,255,255))
            zone_ecran.pasteimage('google_search/'+str(i)+'.jpg',(0,0))
            TFT.display()
            colors = cc.get_colors('google_search/'+str(i)+'.jpg')
            print ("couleur dominante R : {}".format(colors[0][0]))
            print ("couleur dominante G : {}".format(colors[0][1]))
            print ("couleur dominante B : {}".format(colors[0][2]))
            
        capteur_APDS9960.enableGestureSensor(True)

# Déclaration de la broche d'interruption du capteur APDS-9960
APDS9960_INT = DigitalInputDevice(SENSOR_INTERRUPT, pull_up = True)
# Précise que lorsqu'un nouveau geste sera détecté (broche d'interruption changera d'état)
# alors on exécutera la fonction 'Lecture_geste()'
APDS9960_INT.when_activated = Lecture_geste

# Déclaration de l'objet associé au capteur APDS-9960
capteur_APDS9960 = GestureSensor.APDS9960(bus=1)
# Initialisation du capteur APDS-9960
capteur_APDS9960.initDevice()
capteur_APDS9960.resetGestureParameters()
# Modification légère des paramètres pour s'adapter au module présent sur la carte (meilleurs résultats de détection)
capteur_APDS9960.setGestureGain(GGAIN_2X)
capteur_APDS9960.setGestureLEDDrive(LED_DRIVE_25MA)
# Rend le capteur APDS-9960 actif  
capteur_APDS9960.enableGestureSensor(True)

# Boucle infinie d'attente d'interruption
try:
    while True:
        pass
except KeyboardInterrupt:
    capteur_APDS9960.resetGestureParameters()
    print ("STOP")
