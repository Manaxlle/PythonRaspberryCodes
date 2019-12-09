# Serveur web - Gestion on-off de la matrice

# Importation des modules nécessaires
from flask import Flask
from flask import render_template #bibiliothèque pour le rendu de page web
from flask import request, url_for
from sense_hat import SenseHat
import socket

sense = SenseHat()
bleu = (5,41,99)
orange = (252,177,37)
sense.set_rotation(180)

# Instanciation du serveur
serveur_web = Flask(__name__)

#Définit ce que le serveur renvoie selon le chemin de l'URL
@serveur_web.route('/') # page racine
def racine():
    return render_template('Ex04.html')

@serveur_web.route('/change/',methods=['POST'])
def change():
    if request.method == 'POST':
        valr = request.form['rouge']
        valv = request.form['vert']
        valb = request.form['bleu']
        
        x = (valr,valv,valb)

        couleur = [x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x,
                   x,x,x,x,x,x,x,x]
        
        sense.set_pixels(couleur)



    return render_template('Ex04.html')

#Programme principal
serveur_web.debug = False
serveur_web.run(host="0.0.0.0")
