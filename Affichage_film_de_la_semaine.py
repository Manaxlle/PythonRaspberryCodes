# Importation des librairies
# sudo pip3 install feedparser
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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev

DC = 22
RST = 25
LED = 23

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

# Initialisation de l'écran
TFT.initLCD(DC, RST, LED)

# Récupération du flux allocine des sorties de la semaine
url = 'http://rss.allocine.fr/ac/cine/cettesemaine'
flux = feedparser.parse(url)
#print(flux)

# Extraction des informations
entrees_flux = flux.entries
titres_films = []
affiches_films = []
index = 0

zone_ecran = TFT.draw()
TFT.clear((255,255,255))

logo = Image.open('images/Allocine.jpg')
logo = logo.rotate(-90, expand=True)
logo = logo.resize((240,320))
logo.save('images/logo.jpg')

zone_ecran.pasteimage('images/logo.jpg',(0,0))
police = ImageFont.truetype('polices/DK_Pimpernel.otf',36)
zone_ecran.textrotated((60,60), "Films de la semaine", 270, font=police, fill=(0,0,0))

TFT.display()

for entree in entrees_flux :
    print (entree.title)
    titres_films.append(entree.title)
    #print(entree.links[1]['href'])
    try:
        affiches_films.append(entree.links[1]['href'])
        affiche_fichier = requests.get(affiches_films[index], stream=True)
        fichier = open("affiches/"+str(index)+".jpg",'wb')
        affiche_fichier.raw.decode_content = True
        shutil.copyfileobj(affiche_fichier.raw,fichier)
        fichier.close()
        affiche = Image.open('affiches/'+str(index)+'.jpg')
        affiche = affiche.rotate(-90, expand = True)
        affiche.thumbnail((190,190))
        affiche.save('affiches/'+str(index)+'.jpg')
    except:
        print("erreur")
    
    index = index+1
    
    
try:
    TFT.clear((0,0,0))
    i=0
    while 1:
        for i in range(len(titres_films)):
            TFT.clear((0,0,0))
            zone_ecran.textrotated((10,10), titres_films[i], 270, font=police, fill=(255,255,255))
            zone_ecran.pasteimage('affiches/'+str(i)+'.jpg',(60,100))
            TFT.display()
            sleep(2)
except KeyboardInterrupt:
    print("orvoir")