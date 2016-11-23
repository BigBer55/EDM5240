#OK! C'est lui le bon!
# coding: utf-8

#  Je me suis créé un environnement virtuel. 
#  J'ai installé BeautifulSoup pour pouvoir travailler

import csv
import requests
from bs4 import BeautifulSoup


# Voici mon url utilisé : la divulgation de contrats du Ministère des Transport du Canada
url = "http://wwwapps.tc.gc.ca/Corp-Serv-Gen/2/PDC-DPC/contrat/liste_de_contrat.aspx?trimestre=1&annee=2016"

# Nom de mon fichier csv qui va regrouper les données à la fin.

fichier = "transportcanada.csv"

# Je donne mes coordonnées personnelles afin d'aviser le moissonnage de données.
entetes = {
    "User-Agent":"Maxime Bernier - Pour s'informer des transports",
    "From":"max_bernier@hotmail.com"
}

# On demande à requests d'établir une connexion avec mon url. Je veux le contenu dans ma variable appelée contenu. 
contenu = requests.get(url,headers=entetes)

#  Je demande à BeautifulSoup de prendre tout le texte HTML de mon contenu et de l'analyser. Le résultat sera compris dans la variable page.
page = BeautifulSoup(contenu.text,"html.parser")

# print(page)

# On crée un compteur. 0 signifie la première ligne de chaque tableau des contrats, qui n'a aucune information. Elle ne me sert donc à rien. C'est pourquoi j'indique i>0. 
# Ensuite, étant donné que je veux chaque ligne comprise dans tous les tableaux dans un élément html, j'utilise find.all pour les réunir sur une même liste. 
# Tout le contenu défile
i = 0
# print(i)

#  Par la suite, je recheche la partie du url qui revient dans chaque contrat. Pour ma part, elle débute avec le mot contrat. 
# Je prends tout ce qui précède pour me créer un hyperlien. 
# Ceci permettra de retrouver toutes les informations de tous les contrats

for ligne in page.find_all("tr"):
    if i > 0:
        # print(ligne)
        lien = ligne.a.get("href")
        # print(lien)
        hyperlien = "http://wwwapps.tc.gc.ca/Corp-Serv-Gen/2/PDC-DPC/contrat/" + lien
        # print("="*50)
        # print(hyperlien)
    
        # Il est maintenant possible de rechercher des infos propres à chaque contrat avec cet hyperlien
        contenu2 = requests.get(hyperlien,headers=entetes)
        page2 = BeautifulSoup(contenu2.text,"html.parser")
        
        # La variable contrat sera utilisée pour la recherche d'information, Chaque contrat est un tableau avec des données. 
        
        contrat = []
        
        contrat.append(hyperlien)
        # Chaque page de contrat est un petit tableau. On veut aller chercher tous les éléments tr de chaque tableau.
        # On va aussi regrouper tous les items de chaque tableau
        for item in page2.find_all("tr"):
            # print(item)
         
        # Certain éléments n'ont pas été reconnus, car une partie du tableau est vide. Cette condition permet d'enlever ces espaces vides. 
            if item.td is not None:
                contrat.append(item.td.text)
            else:
                contrat.append(None)
            
          
        
        # print(contrat)
        
        # Je crée un fichier csv pour regrouper mes données. 
        travail = open(fichier,"a")
        marcgarneau = csv.writer(travail)
        marcgarneau.writerow(contrat)
            
           
    # Afin d'avoir toutes les données de mes tableauux. (Plus grand que ma première ligne 0)
    i += 1
            
   
