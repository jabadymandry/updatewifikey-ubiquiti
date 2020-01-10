import requests
import json
import string
import random

class p_UnifiController(object):
    """
    Acces controller AP Ubiquiti
    Bruno Enee <brunoenee@gmail.com>
    07/01/2020
    """

    def __init__(self, controller, username, password, port=8443, emailAddress=["brunoenee@gmail.com"], phoneNumber=[]):
        """
        Constructeur initialisation des variables.
        """
        self._emailAddress = emailAddress
        self._phoneNumber = phoneNumber
        self._controller = controller
        self._username = username
        self._password = password
        self._port = port
        self._session = None
        self._url = "https://{0}:{1}".format(self._controller, self._port)


    def connect(self):
        """ 
        Authentification sur le controller des Access Points
        """
        url = self._url+"/api/login"
        payload = json.dumps({'username':self._username,'password': self._password})
        headers = {
          'Content-Type': 'application/json'
        }
        self._session = requests.Session()
        response = self._session.request("POST", url, headers=headers, data = payload, verify=False)
        meta = response.json()['meta']['rc']
        print("Connexion sur controller: {0}".format(meta))
        return meta



    def getWifiConfig(self, allWifi=False):
        """
          Retourne les configurations wifi. Par defaut recupere seulement les wifi active
        """
        wifiConfig = []
        url = self._url+"/api/s/default/rest/wlanconf"
        response = self._session.request("GET", url, verify=False)
        data = response.json()['data']
        #print(data['data'])
        if allWifi == False:
          for wifi in data:
              #print (wifi)
              if wifi['enabled'] == True:
                  #print("SSID: {0} <->  Pass: {1} <-> id: {2}\n".format(wifi['name'], wifi['x_passphrase'],wifi['_id']))
                  wifiConfig.append(wifi)
        else:
          for wifi in data:
                #print("SSID: {0} <->  Pass: {1} <-> id: {2}\n".format(wifi['name'], wifi['x_passphrase'],wifi['_id']))
                wifiConfig.append(wifi)

        return wifiConfig

    def deconnect(self):
          """
          Deconnexion du controller des Access Point
          """
          url = self._url+"/api/logout"
          response = self._session.request("POST", url, verify=False)
          print("Deconnexion sur controller: {0}".format(response.json()['meta']['rc']))

    def generatePassword(self, passwd_length=9):
        """
        Generate random password of fixed lenght default 9
        """
        lettres = string.ascii_letters
        chiffres = string.digits
        special_chars = "@!#$"
        pass_chars = lettres+chiffres+special_chars
        password = ''.join(random.choice(pass_chars) for i in range(passwd_length))
        return password

    def updateWlanConfig(self, conf):
        """
        Mise a jour parametre WiFi
        """
        conf = json.loads(conf)
        url = self._url+"/api/s/{0}/rest/wlanconf/{1}".format(conf['site'],conf['id_wifi'])
        payload = json.dumps({'x_passphrase': conf['key']})
        headers = {
          'Content-Type': 'application/json'
        }
        response = self._session.request("PUT", url, headers=headers, data= payload, verify=False)
        print("Mise a jour cle wifi: {0} [{1}]".format(str(conf['wifi_name']),response.json()['meta']['rc']))
