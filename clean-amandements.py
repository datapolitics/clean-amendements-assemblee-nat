#%%
# creates a list with all file names

AMENDEMENTS_FOLDER = "amendements" # dosssier dans lequel ont été extraits les amandements téléchargés au format JSON depuis https://data.assemblee-nationale.fr/travaux-parlementaires/amendements/tous-les-amendements
import os

from pandas.core import groupby
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if(name != '.DS_Store'):
                r.append(os.path.join(root, name))
    return r

files = list_files(AMENDEMENTS_FOLDER)

# %%
# for each file, import to json and add selected fields to df
import json
import csv
csv_columns = ['id',
            'numeroOrdreDepot',
            'chronotag',
            'prefixeOrganeExamen',
            'examenRef',
            'texteLegislatifRef',
            'typeAuteur',
            'acteurRef',
            'groupePolitiqueRef',
            'dateDepot',
            'datePublication',
            'dateSort',
            'sort',
            'etat_code',
            'etat_libelle',
            'cartoucheInformatif',
            'documentURI',
            'seanceDiscussionRef',
            'article99',
            'discussionCommune',
            'discussionIdentique',
            'loiReference_codeLoi',
            'loiReference_divisionCodeLoi',
            'seanceDiscussionRef'
]

def parse(field):
    if(isinstance(field,dict)):
        return field if not '@xsi:nil' in field else "none"
    else:
        return field

csv_file = "amendements.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for f in files:
            with open(f) as amandement_json:
                data = json.load(amandement_json)

                new_row = {
                    'id' : data["amendement"]["uid"],
                    'numeroOrdreDepot' : data["amendement"]["identification"]["numeroOrdreDepot"],
                    'chronotag' : parse(data["amendement"]["chronotag"]),
                    'prefixeOrganeExamen' :  parse(data["amendement"]["identification"]["prefixeOrganeExamen"]),
                    'examenRef' : parse(data["amendement"]["examenRef"]),
                    'texteLegislatifRef' : parse(data["amendement"]["texteLegislatifRef"]),
                    'typeAuteur' : parse(data["amendement"]["signataires"]["auteur"]["typeAuteur"]),
                    'acteurRef' : parse(data["amendement"]["signataires"]["auteur"]["acteurRef"]),
                    'groupePolitiqueRef': parse(data["amendement"]["signataires"]["auteur"]["groupePolitiqueRef"]),
                    'dateDepot' : parse(data["amendement"]["cycleDeVie"]["dateDepot"]),
                    'datePublication' : parse(data["amendement"]["cycleDeVie"]["datePublication"]),
                    'dateSort': parse(data["amendement"]["cycleDeVie"]["dateSort"]),
                    'sort': parse(data["amendement"]["cycleDeVie"]["sort"]),
                    'etat_code': parse(data["amendement"]["cycleDeVie"]["etatDesTraitements"]["etat"]["code"]) if '@xsi:nil' not in data["amendement"]["cycleDeVie"]["etatDesTraitements"]["etat"] else "none",
                    'etat_libelle': parse(data["amendement"]["cycleDeVie"]["etatDesTraitements"]["etat"]["libelle"]) if '@xsi:nil' not in data["amendement"]["cycleDeVie"]["etatDesTraitements"]["etat"] else "none",
                    'cartoucheInformatif': parse(data["amendement"]["corps"]["cartoucheInformatif"]),
                    'documentURI': parse(data["amendement"]["representations"]["representation"]["contenu"]["documentURI"]),
                    'seanceDiscussionRef' : parse(data["amendement"]["seanceDiscussionRef"]),
                    'article99' : parse(data["amendement"]["article99"]),
                    'discussionCommune': parse(data["amendement"]["discussionCommune"]["idDiscussion"]) if '@xsi:nil' not in data["amendement"]["discussionCommune"] else "none",
                    'discussionIdentique': parse(data["amendement"]["discussionIdentique"]["idDiscussion"]) if '@xsi:nil' not in data["amendement"]["discussionIdentique"] else "none",
                    'loiReference_codeLoi': parse(data["amendement"]["loiReference"]["codeLoi"]) if '@xsi:nil' not in data["amendement"]["loiReference"] else "none",
                    'loiReference_divisionCodeLoi': parse(data["amendement"]["loiReference"]["divisionCodeLoi"]) if '@xsi:nil' not in data["amendement"]["loiReference"] else "none",
                    'seanceDiscussionRef': parse(data["amendement"]["seanceDiscussionRef"])
                }

                writer.writerow(new_row)

except IOError:
    print("I/O error")

# %%
# ajouter infos sur les députés et les partis
import pandas as pd
df_deputes = pd.read_csv("deputes.csv",sep=";",dtype={"identifiant":str})
df_deputes["identifiant"] = "PA" + df_deputes["identifiant"]

couleurs_politiques = {
    'Les Républicains': "Droite",
    'La République en Marche': "Centre",
    'Libertés et Territoires': "Centre",
    'Agir ensemble': "Centre",
    'La France insoumise' : "Gauche radicale",
    'Mouvement Démocrate (MoDem) et Démocrates apparentés' : "Centre",
    'Socialistes et apparentés': "Gauche",
    'UDI et Indépendants': "Droite",
    'Non inscrit': "None",
    'Gauche démocrate et républicaine' : "Gauche" 
}

from datetime import datetime
def parse_date(date):
    try: 
        print(date)
        return datetime.strptime(date, '%Y-%m-%d')
    except:
        return "none"

dateparse = lambda x:parse_date(x)

df_amendements = pd.read_csv("amendements.csv",parse_dates=["dateDepot"]) #,date_parser=dateparse)
df_amendements = df_amendements.merge(df_deputes, left_on="acteurRef", right_on="identifiant", how="left")

df_amendements["Groupe politique (complet)"].fillna("Groupe Inconnu", inplace=True)


#%%
# on rajoute la data sur les groupes pour les députés n'appartenant plus à l'assemblée

import csv

with open('ex-deputes.csv', mode='r') as inp:
    reader = csv.reader(inp)
    map_deputes_mandat_ecourté = {rows[0]:rows[1] for rows in reader}


deputes_not_found = []

def map_groupe(row):

    if(row["typeAuteur"] == "Député" and row["acteurRef"] in map_deputes_mandat_ecourté):
            return map_deputes_mandat_ecourté[row["acteurRef"]]
    else:
            if(row["acteurRef"] != "none"):
                deputes_not_found.append(row["acteurRef"])
            return "Groupe Inconnu"
            
if(len(deputes_not_found)) > 0:
    print("Les députés : " , deputes_not_found , " ont émis un amendement mais ne sont pas connus du sytème. Rafraichissez le csv de députés ou compléter la map de députés au mandat écourté")


df_amendements["Groupe politique (complet)"] = df_amendements.apply(
    lambda row: map_groupe(row) if row["Groupe politique (complet)"] == "Groupe Inconnu" else row["Groupe politique (complet)"],
    axis=1
)

df_amendements["couleur"] = df_amendements.apply(
    lambda row: couleurs_politiques[row["Groupe politique (complet)"]] if row["typeAuteur"] == "Député" else "none",
    axis=1)


#%%
df_amendements.to_csv("amendements.csv")


