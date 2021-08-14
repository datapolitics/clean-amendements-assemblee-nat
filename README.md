<div align="center" id="top"> 


  <!-- <a href="https://{{app_url}}.netlify.app">Demo</a> -->
</div>

<h1 align="center">Clean-Amendements</h1>

<br>

## :dart: A propos ##

Ce projet contient un script permettant de créer un CSV unique regroupant les méta-données de chaque amandement de la 15ème législature de l'assemblée nationale, à partir de [open data assemblée nationale](https://data.assemblee-nationale.fr/travaux-parlementaires/amendements/tous-les-amendements).


Afin d'optimiser la taille de l'output , seule certaines données sont exportées dans le résultat.

Mais vous pouvez adapter en fonction des données dont vous avez besoin, ou simplement utiliser le dataset de ce repository. 


## :white_check_mark: Requirements ##

Python 3.7+
Aucune dépendance.


## ▶️ Utilisation ##

1. Télécharger la base amandements en format JSON [ici](https://data.assemblee-nationale.fr/travaux-parlementaires/amendements/tous-les-amendements

2. Créer un dossier "amendements" à la racine du projet et y décompresser les amendements téléhargés

3. Exécuter le script clean-amendements.py

Un fichier amendements.csv est créé.

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


