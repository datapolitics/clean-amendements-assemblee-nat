#%%
# creates a list with all file names

AMENDEMENTS_FOLDER = "amendements" # dosssier dans lequel ont été extraits les amandements téléchargés au format JSON depuis https://data.assemblee-nationale.fr/travaux-parlementaires/amendements/tous-les-amendements
import os
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if(name != '.DS_Store'):
                r.append(os.path.join(root, name))
    return r

files = list_files("amandements")

# %%
# for each file, import to json and add selected fields to df
import json
import csv
csv_columns = ['id',
            'chronotag',
            'examenRef',
            'texteLegislatifRef',
            'typeAuteur',
            'acteurRef',
            'groupePolitiqueRef',
            'dateDepot',
            'datePublication',
            'dateSort',
            'sort',
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

csv_file = "df_amandements.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for f in files:
            with open(f) as amandement_json:
                data = json.load(amandement_json)

                new_row = {
                    'id' : data["amendement"]["uid"],
                    'chronotag' : parse(data["amendement"]["chronotag"]),
                    'examenRef' : parse(data["amendement"]["examenRef"]),
                    'texteLegislatifRef' : parse(data["amendement"]["texteLegislatifRef"]),
                    'typeAuteur' : parse(data["amendement"]["signataires"]["auteur"]["typeAuteur"]),
                    'acteurRef' : parse(data["amendement"]["signataires"]["auteur"]["acteurRef"]),
                    'groupePolitiqueRef': parse(data["amendement"]["signataires"]["auteur"]["groupePolitiqueRef"]),
                    'dateDepot' : parse(data["amendement"]["cycleDeVie"]["dateDepot"]),
                    'datePublication' : parse(data["amendement"]["cycleDeVie"]["datePublication"]),
                    'dateSort': parse(data["amendement"]["cycleDeVie"]["dateSort"]),
                    'sort': parse(data["amendement"]["cycleDeVie"]["sort"]),
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
# END