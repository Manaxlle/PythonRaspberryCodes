# CORRESPONDANCE ENTRE LA COULEUR SOUS LE CURSEUR ET CELLE D'UNE LED
# on affiche une image multicolore à l'écran et en déplaçant le curseur
# de la souris sur l'image, la LED prend la couleur correspondante

# Importation des modules nécessaires
from guizero import App, Picture
from PIL import Image
from time import sleep
from sense_hat import SenseHat

# Instanciation de l'objet SenseHat
sense = SenseHat()

# chemin du fichier de l'image utilisée
chemin_fichier = "images/parapluies.jpg"

# Fonction de récupération de la couleur à la position du clic dans l'image
def Affichage_couleur(infos) :
    # Affichage des coordonnées dans l'image
    print("Clic !!")
    print("x = {} / y = {}".format(infos.x, infos.y))
    # Récupération de la couleur du pixel cliqué
    img = Image.open(chemin_fichier)
    img = img.convert('RGB')
    (r,v,b) = img.getpixel((infos.x, infos.y))
    print (r,v,b)
    # Affichage de la couleur
    couleur = (r,v,b)
    table = [couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur,
             couleur, couleur, couleur, couleur, couleur, couleur, couleur, couleur]
    sense.set_pixels(table)
# Mise en place de la fenêtre
fenetre = App(width=1024, height=768)
fenetre.focus()
# Chargement d'une image dans la zone de dessin
fond = Picture(fenetre, image=chemin_fichier)

# Définition de la fonction à appeler lors d'un clic
fond.when_clicked = Affichage_couleur

# Boucle principale infinie de la fenêtre
fenetre.display()
