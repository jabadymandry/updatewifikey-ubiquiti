#!/usr/bin/python
# Script pour changer mettre a jour googlesheet
# Bruno Enee <brunoenee@gmail.com>
# Update 08/01/2020
# ----------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from unificontroller import p_UnifiController
import configparser
import json

def clearGoogleSheet(google_credentials, google_sheet_id):
    """
    Vider le googlesheet et retourner l'instance du sheet pour mise a jour
    Ajout en tete du tableau
     _______________________
    | WIFI SSID | WIFI KEY  |
    ------------------------
    | ETE-CONF  | $#Nma$#dz |
    -------------------------
    """
    # Definition de credentials pour acces API Google
    credentials = google_credentials
    # Definition scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
    client = gspread.authorize(creds)
    # Googlesheet a editer
    GoogleSheet_Id = google_sheet_id
    # Ouvrir googlesheet avec ID
    sheet = client.open_by_key(GoogleSheet_Id).sheet1
    sheet.clear()
    sheet.insert_row(["WIFI - SSID", "WIFI - KEY"],1)
    return sheet


def updateGoogleSheet(sheet, data):
    """
    Mise a jour Tableur google sheet en respectant le modele ci-dessous
    """
    #print("Mise a jour googlesheet")
    data = json.loads(data)
    data_in_file = sheet.get_all_values()
    #print("Nombre de lignes dans le fichier: {0}".format(len(data_in_file)))
    #for d in data_in_file:
    #    print(d)
    sheet.insert_row([str(data['ssid']), str(data['key'])], len(data_in_file)+1)

try:
    configFile = "wifi.conf"
    config = configparser.ConfigParser()
    config.read(configFile)
    controller = config['GOOGLE']['controller']
    username = config['GOOGLE']['username']
    password = config['GOOGLE']['password']
    gsheet = clearGoogleSheet(config['GOOGLE']['google_credentials'], config['GOOGLE']['google_sheet_id'])

    etechcontroller = p_UnifiController(controller, username, password)
    if config['WIFI']['cle_unique'] == "yes":
        if etechcontroller.connect() == "ok":
            wifi_config = etechcontroller.getWifiConfig()
            for wifi_name in config['WIFI']['ssid'].split(','):
                wifi_key = etechcontroller.generatePassword()
                #print(wifi_key)
                for wifi in wifi_config:
                    if wifi_name == wifi['name']:
                        id_wifi = wifi['_id']
                        for  s in config['WIFI']['site'].split(','):
                            update_params = json.dumps({'site': s, 'id_wifi': id_wifi, 'key': wifi_key, 'wifi_name': wifi_name})
                            etechcontroller.updateWlanConfig(update_params)
                            sheet_data = json.dumps({'ssid': wifi_name, 'key': wifi_key})
                            updateGoogleSheet(gsheet, sheet_data)
    else:
        if etechcontroller.connect() == "ok":
            wifi_config = etechcontroller.getWifiConfig()
            for wifi_name in config['WIFI']['ssid'].split(','):
                for wifi in wifi_config:
                    if wifi_name == wifi['name']:
                        id_wifi = wifi['_id']
                        for  s in config['WIFI']['site'].split(','):
                            #print(config['WIFI']['ussid'].split(','))
                            wifi_key = etechcontroller.generatePassword()
                            #print(wifi_key)
                            update_params = json.dumps({'site': s, 'id_wifi': id_wifi, 'key': wifi_key, 'wifi_name': wifi_name})
                            etechcontroller.updateWlanConfig(update_params)
                            sheet_data = json.dumps({'ssid': wifi_name, 'key': wifi_key})
                            updateGoogleSheet(gsheet, sheet_data)
    etechcontroller.deconnect()
except Exception as error:
    print("Une erreur s\'est produite: {0}".format(error))