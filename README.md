# FFbD

---------------------------------------------------------

FFbD.py (Find Files by Dates) v0.1
Auteur: Yann MANET <yann.manet@unige.ch>

---------------------------------------------------------

Usage: FFbD.py -p <path> -s <startdate> -e <enddate> [-m]

Options:
        -p ou --path    <chemin du répertoire à analyser entre guillemets>
        -s ou --start   <date de début de recherche> (format jj-mm-aaaa), si manquant = date du jour
        -e ou --end     <date de fin de recherche> (format jj-mm-aaaa), si manquant = date du jour
        -m  par défaut, la recherche est faite par date de création, en ajoutant l'option -m, la recherche sera faite par date de modification
