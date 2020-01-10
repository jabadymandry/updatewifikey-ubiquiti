- Requirements:
    - Python 2.7.x ou supérieur. Testé sur version Python 2.7.13
    - module python : gspread oauth2client
    - Accès en mode ecriture de l'utilisateur utilisé par le script representé dans le fichier json

- Installation:
    - Deploiement les codes sur un serveur
    - Créer un cron pour le déclanchement


- Configuration:
Le fichier de configuration de l'application se trouve dans /etc/updatewifikey/wifi.conf dont le contenu est le suivant:

# section concernant le googlesheet
[GOOGLE]
google_credentials = 3531b0eefab4.json                          # Crédentials que j'ai créer pour pouvoir editer le fichier
google_sheet_id = 0XnZkjvgkq4M9H6Pmwru6JO3i-ULvq1w              # id du fichier sheet recuperer sur l'url du fichier
controller = 192.168.1.250                                      # Adresse du controlleur Unifi
username = appli                                                # Utilisateur sur le controlleur avec droit d'edition (admin)
password = sesfsffds2020                                        # mot de passe

# Section Wifi
[WIFI]
ssid = ETE-CONF                                                 # Liste de wifi à modifier la clé: exemple: ssid = ETE-CONF,SU-Staff
site = default                                                  # Site auxquels sont rattaché les AP, par defaut c'est "default"
cle_unique = yes                                                # Les même sssid auront -il le même mot de passe ou non?