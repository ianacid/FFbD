import os, sys, getopt, time
import datetime as dt

# ############
# FONCTIONS
# ############

def usage():
	print (title)
	print("\nUsage: FFbD.py -p <path> -s <startdate> -e <enddate> [-m]")
	print("\nOptions:")
	print("\t-p ou --path \t<chemin du répertoire à analyser entre guillemets>")
	print("\t-s ou --start \t<date de début de recherche> (format jj-mm-aaaa), si manquant = date du jour")
	print("\t-e ou --end \t<date de fin de recherche> (format jj-mm-aaaa), si manquant = date du jour")
	print("\n\t-m  >> par défaut, la recherche est faite par date de création, en ajoutant l'option -m, la recherche sera faite par date de modification")
	return

def convertDate2Time(strDate, endDate):
	if endDate == True:
		time = (dt.datetime.strptime(strDate, "%d-%m-%Y") - t0).total_seconds() + 86340
	else:
		time = (dt.datetime.strptime(strDate, "%d-%m-%Y") - t0).total_seconds()
	return time

def convertTime2strDate(t):
	return dt.datetime.utcfromtimestamp(t).strftime('%d-%m-%Y %H:%M')

# ############
# VARIABLES
# ############
screenDelimiter = "---------------------------------------------------------"
version = "0.1"
title = screenDelimiter + "\n\nFFbD.py (Find Files by Dates) v" + version + "\nAuteur: Yann MANET <yann.manet@unige.ch>\n\n" + screenDelimiter
t0 = dt.datetime.utcfromtimestamp(0)
path = ""
startdate = int(convertDate2Time(dt.datetime.now().strftime("%d-%m-%Y"), False))
enddate = int(convertDate2Time(dt.datetime.now().strftime("%d-%m-%Y"), True))
index = -1
screenDelimiter = "---------------------------------------------------------"

# ############
# PARAMETRES
# ############

try:
	opts, arg = getopt.getopt(sys.argv[1:], "h:p:s:e:m", ["--help","path=","start=","end="])

except getopt.GetoptError as err:
	usage()
	exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		usage()
		exit()

	elif opt in ("-p", "--path"):
		path = arg

		if not os.path.isdir(path):
			print("Erreur: directive -p ou --path: le chemin n'est pas valide")
			usage()
			exit(2)

	elif opt in ("-s", "--start"):
		# Conversion de la date start en timestamp
		startdate = int(convertDate2Time(arg, False))

	elif opt in ("-e", "--end"):
		# Conversion de la date end en timestamp
		enddate = int(convertDate2Time(arg, True))

	elif opt == "-m":
		index = -2

# ############
# INFOS
# ############

print (screenDelimiter)

print (title)

if index == -2:
	print ("Liste par date de modification de fichier")
else:
	print ("Liste par date de création de fichier")

print ("Dans: " + path)
print ("Entre le " + convertTime2strDate(startdate) + " et le " + convertTime2strDate(enddate))
print ("Liste générée le " + dt.datetime.now().strftime("%d-%m-%Y %H:%M"))
print (screenDelimiter)
print (screenDelimiter)
print ("CRÉATION\t | \tFILENAME\t | \tPATH")
print (screenDelimiter)

# ############
# RECHERCHES ET AFFICHAGE RESULTATS
# ############

for (dirpath, dirnames, filenames) in os.walk(path):
	for filename in filenames:
		f = '\\'.join([dirpath,filename])

		ctime = os.stat(f)[index]

		if ctime>=startdate and ctime <=enddate:
			print (convertTime2strDate(ctime) + "\t", end = '')
			print (filename + "\t", end = '')
			print (f)
			print (ctime)
			print (os.stat(f))

print (screenDelimiter)

exit(0)