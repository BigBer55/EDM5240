# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

url = "http://wwwapps.tc.gc.ca/Corp-Serv-Gen/2/PDC-DPC/contrat/liste_de_contrat.aspx?trimestre=1&annee=2016"
# Site offline le 4 novembre!! À suivre...
fichier = "transportcanada-JHR.csv"

entetes = {
    "User-Agent":"Maxime Bernier - Pour s'informer des transports",
    "From":"max_bernier@hotmail.com"
}

contenu = requests.get(url,headers=entetes)
page = BeautifulSoup(contenu.text,"html.parser")

# print(page)

i = 0

for ligne in page.find_all("tr"):
    if i > 0:
        # print(ligne)
        lien = ligne.a.get("href")
        # print(lien)
        hyperlien = "http://wwwapps.tc.gc.ca/Corp-Serv-Gen/2/PDC-DPC/contrat/" + lien
        # print("="*50)
        # print(hyperlien)

        contenu2 = requests.get(hyperlien,headers=entetes)
        page2 = BeautifulSoup(contenu2.text,"html.parser")

        contrat = []
        
        contrat.append(hyperlien)

        for item in page2.find_all("tr"):
            # print(item)

        # Certain éléments n'ont pas été reconnus, car une partie du tableau est vide. Cette condition permet d'enlever ces espaces vides. 
            if item.td is not None:
                contrat.append(item.td.text)
            else:
                contrat.append(None)

        print(contrat)

        travail = open(fichier,"a")
        marcgarneau = csv.writer(travail)
        marcgarneau.writerow(contrat)

    i += 1

# C'est parfait, tout marche très bien!
# Tu es prêt à essayer de moissonner des sites plus difficiles! :-)
