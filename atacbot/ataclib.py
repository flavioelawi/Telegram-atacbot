from xmlrpc.client import Server
import json
import os
import logging

class ataclib:
    def __init__(self):
        configfile_path = os.path.join(os.path.expanduser("~"), ".atacbot", "config.json")
        c = open(configfile_path, "r")
        config = json.load(c)
        atac_key = config["atackey"]
        ####### INSERT DEV KEY IN config.ini HERE ################
        ####### [atackey]
        ####### atac_key=KEY
        ###########################################
        s1 = Server('http://muovi.roma.it/ws/xml/autenticazione/1')
        self.s2 = Server('http://muovi.roma.it/ws/xml/paline/7')
        self.token = s1.autenticazione.Accedi(atac_key, '')

    def getPercorso(self, linea):
        try:
            res = self.s2.paline.Percorsi(self.token, linea, 'it')
            # print(type(res))
            percorso = []
            i = 0
            while i < len(res.get('risposta').get('percorsi')):
                perc = res.get('risposta').get('percorsi')[i].get('id_percorso')
                capolinea = res.get('risposta').get('percorsi')[i].get('capolinea')
                percorso.append((perc, capolinea))
                # print("Percorso %s: " + percorso + " Capolinea: %s") % (i, capolinea)
                i = i + 1
            risposta = "Risposta da muovi.roma.it \n"

            for i in percorso:
                res = self.s2.paline.Percorso(self.token, i[0], '', '', '')
                risposta += "\n"
                risposta += "*Linea Bus " + linea + " capolinea " + i[1] + "* \n"
                p = 0
                while p < len(res.get('risposta').get('fermate')):
                    palina = res.get('risposta').get('fermate')[p].get('id_palina')
                    nome = res.get('risposta').get('fermate')[p].get('nome_ricapitalizzato')
                    nome = nome.replace('.','')
                    veicolo = res.get('risposta').get('fermate')[p].get('veicolo')
                    if veicolo:
                        risposta += palina + ": " + nome + " <-------  \n"
                    else:
                        risposta += palina + ": " + nome + "\n"
                    p = p + 1

            return risposta
        except Exception as e:
            logging.critical("%s %s" %(linea, str(e)))
            pass

    def getPalina(self, id_palina):
        try:
            res = self.s2.paline.Previsioni(self.token, id_palina, 'it')
            i=0
            arrivi=[]
            while i < len(res.get('risposta').get('arrivi')):
                linea = res.get('risposta').get('arrivi')[i].get('linea')
                annuncio = res.get('risposta').get('arrivi')[i].get('annuncio')
                arrivi.append((linea,annuncio))
                i=i+1

            risposta = "Risposta da muovi.roma.it \n"
            if arrivi:
                i = 0
                while i < len(arrivi):
                    risposta += str(arrivi[i][0]) + ": " + str(arrivi[i][1]) + "\n"
                    i = i + 1

            return risposta
        except Exception as e:
            logging.critical("%s %s" % (id_palina, str(e)))
            pass