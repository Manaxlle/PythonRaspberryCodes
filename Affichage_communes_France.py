# Importation des librairies
import requests
import csv
from bs4 import BeautifulSoup
import textwrap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import spidev

DC = 22
RST = 25
LED = 23

TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

# Initialisation de l'écran
TFT.initLCD(DC, RST, LED)

# Récupération du fichier officiel des codes postaux s'il n'existe pas
try :
    with open('codes_postaux.csv') :
        pass
except IOError :
    url = 'https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true'
    mon_fichier = requests.get(url)
    with open('codes_postaux.csv', 'wb') as donnees :
        donnees.write(mon_fichier.content)
      
# Demande à l'utilisateur le nom de la commune
commune = input("Commune à rechercher: ")
# Mise en majuscules
commune = commune.upper()
# Affichage du nom de la commune dans la console
print(commune)

# Extraction du code postal dans le fichier CSV
fichier_csv = open("codes_postaux.csv", "r")
try :
    lecteur_csv = csv.reader(fichier_csv, delimiter=";")
    for ligne in lecteur_csv :
        if ligne[1] == commune:
            code_postal = ligne[2]
#         Affichage du code postal dans la console
            print("Code postal de {}: {}".format(commune,code_postal))
finally :
    fichier_csv.close()
    
    
zone_ecran = TFT.draw()
TFT.clear((10,2,87))

police1 = ImageFont.truetype('polices/DK_Pimpernel.otf',36)
police2 = ImageFont.truetype('polices/DK_Pimpernel.otf',65)
zone_ecran.textrotated((150,75), "Code postal de", 270, font=police1, fill=(255,255,255))
zone_ecran.textrotated((120,100), "{} :".format(commune), 270, font=police1, fill=(255,255,255))
zone_ecran.textrotated((50,100), code_postal, 270, font=police2, fill=(255,255,255))
TFT.display()
    