import os
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
import BMP280
import time
import json
import pprint

import spidev
DC = 22
RST = 25
LED = 23
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

TFT.initLCD(DC, RST, LED)

# Détermination des éléments de la date du jour
date_complete = datetime.date.today()
jour = date_complete.day
mois = date_complete.month
annee = date_complete.year
jour_semaine = date_complete.weekday()
liste_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Mise en forme de la date du jour. Exemple : "Lundi 14/10/2019"
Txt_date = str(liste_jours[jour_semaine])+" "+str(jour)+"/"+str(mois)+"/"+str(annee)

longueur_chaine = len(Txt_date)
varY_date = int((320-(longueur_chaine*13))/2) #Position Y de la date à afficher

try :
    # création d'un objet basé sur la classe BMP280
    capteur_bmp280 = BMP280.BMP280()
    # initialisation du capteur
    capteur_bmp280.init()
    # Lecture de la température + arrondi à un chiffre après la virgule
    temp_bmp280 = "T. int : "+str(round(capteur_bmp280.temperature(),1))+" °C"
    # lecture de la pression + arrondi à un chiffre après la virgule
    pression_bmp280 = "P : "+str(round(capteur_bmp280.pressure(),1))+" hPa"

    # pause
    time.sleep(1)
except KeyboardInterrupt :
    GPIO.cleanup()
    print ("Au revoir...")

#Ouverture du fichier json avec le bon encodage pour lire les accents
json_data=open('Current_weather.json', encoding = "ISO-8859-1")
#Lecture des données du fichier json
response = json.load(json_data)
#Fermeture du fichier json
json_data.close()

#Ouverture du fichier json avec le bon encodage pour lire les accents
json_data=open('7_days_forecast.json', encoding = "ISO-8859-1")
#Lecture des données du fichier json
response_forecast = json.load(json_data)
#Fermeture du fichier json
json_data.close()

#Affichage brut mais structuré des données
pprint.pprint(response)
pprint.pprint(response_forecast)

#Extraction de l'information de description
tendance = response['weather'][0]['description']
longueur_chaine = len(tendance)
varY_tendance = int((320-(longueur_chaine*13))/2)

# Acquisition des températures min et max de la journée
temperatures = response['main']
temp_min = "T ext min : "+str(round(response['main']['temp_min'],1))+" °C"
temp_max = "T ext max : "+str(round(response['main']['temp_max'],1))+" °C"

# Acquisition du n° d'image associé à la tendance
id_tendance = response['weather'][0]['id']

# Nombre de jours du fichier JSON prévisions
nbjours = response_forecast['cnt']

# Acquisition des prévisions pour les nbjours à venir
previsions = response_forecast['list']

zone_ecran = TFT.draw()
TFT.clear((150,7,232))

police_date = ImageFont.truetype('Polices/Letters_for_Learners.ttf',36)
police_TempPres = ImageFont.truetype('Polices/Letters_for_Learners.ttf',24)

zone_ecran.textrotated((30,190), temp_bmp280, 270, font=police_TempPres, fill=(255,255,255))
zone_ecran.textrotated((5,190), pression_bmp280, 270, font=police_TempPres, fill=(255,255,255))
zone_ecran.rectangle(((5,172),(48,172)), fill=(0,0,0))

#En boucle: on affiche les informations du jour-même puis celles des nbjours à venir
while True:
    TFT.clear((150,7,232))
    date_complete = datetime.date.today()
    jour = date_complete.day
    mois = date_complete.month
    annee = date_complete.year
    jour_semaine = date_complete.weekday()
    
    Txt_date = str(liste_jours[jour_semaine])+" "+str(jour)+"/"+str(mois)+"/"+str(annee)
    tendance = response['weather'][0]['description']
    longueur_chaine = len(tendance)
    varY_tendance = int((320-(longueur_chaine*13))/2)

    temperatures = response['main']
    temp_min = "T ext min : "+str(round(response['main']['temp_min'],1))+" °C"
    temp_max = "T ext max : "+str(round(response['main']['temp_max'],1))+" °C"

    id_tendance = response['weather'][0]['id']
    zone_ecran.pasteimage('icons/'+str(id_tendance)+".jpg",(80,100))
    zone_ecran.textrotated((210,varY_date), Txt_date, 270, font=police_date, fill=(0,0,0))

    zone_ecran.textrotated((60,varY_tendance), tendance, 270, font=police_date, fill=(0,0,0))

    zone_ecran.textrotated((30,10), temp_max, 270, font=police_TempPres, fill=(255,255,255))
    zone_ecran.textrotated((5,10), temp_min, 270, font=police_TempPres, fill=(255,255,255))
    
    zone_ecran.textrotated((30,190), temp_bmp280, 270, font=police_TempPres, fill=(255,255,255))
    zone_ecran.textrotated((5,190), pression_bmp280, 270, font=police_TempPres, fill=(255,255,255))
    zone_ecran.rectangle(((5,172),(48,172)), fill=(0,0,0))

    zone_ecran.pasteimage('icons/'+str(id_tendance)+".jpg",(80,100))

    TFT.display()
    time.sleep(3)
    
    for i in range(nbjours):
        TFT.clear((150,7,232))
        jour = jour+1
        #Si on doit repasser du dimanche au lundi (pour éviter de dépasser la longueur de la liste)
        if jour_semaine+1+i > 6:
            jour_semaine = jour_semaine-3-i
        
        Txt_date = str(liste_jours[jour_semaine+1+i])+" "+str(jour)+"/"+str(mois)+"/"+str(annee)
        
        tendance = previsions[i]['weather'][0]['description']
        id_tendance = previsions[i]['weather'][0]['id']
        temp_min = "T ext min : "+str(round(previsions[i]['temp']['min'],1))+" °C"
        temp_max = "T ext max : "+str(round(previsions[i]['temp']['max'],1))+" °C"

        longueur_chaine = len(tendance)
        varY_tendance = int((320-(longueur_chaine*13))/2)
        
        longueur_chaine = len(Txt_date)
        varY_date = int((320-(longueur_chaine*13))/2)

    
        zone_ecran.textrotated((210,varY_date), Txt_date, 270, font=police_date, fill=(0,0,0))

        zone_ecran.textrotated((50,varY_tendance), tendance, 270, font=police_date, fill=(0,0,0))

        zone_ecran.textrotated((30,10), temp_max, 270, font=police_TempPres, fill=(255,255,255))
        zone_ecran.textrotated((5,10), temp_min, 270, font=police_TempPres, fill=(255,255,255))

        zone_ecran.pasteimage('icons/'+str(id_tendance)+".jpg",(80,100))

        TFT.display()
        time.sleep(3)