import os, sys, getopt, time, re
import datetime as dt

# -------------------
# FONCTIONS
# -------------------

def usage():
	# Affichage de l'usage
	# return void
	
	print(
		"\nUsage:\n>> FFbD.py -p \"<path>\" -s <startdate (dd-mm-yyyy)> -e <enddate (dd-mm-yyyy)> -f <extensions (comma separated)> [-m]\n" + \
		">> FFbD.py --path \"<path>\" --start <startdate (dd-mm-yyyy)> --end <enddate (dd-mm-yyyy)> --filter <extensions (comma separated)> [-m]\n" + \
		"\nOptions:\n" + \
		"\t[required] -p or --path \t<path of the directory to be analysed between quotes>\n" + \
		"\t[optional] -s or --start \t<search start date> (dd-mm-yyyy), if missing = today's date\n" + \
		"\t[optional] -e or --end \t\t<search end date> (dd-mm-yyyy), if missing = today's date\n" + \
		"\t[optional] -f or --filter \t<File extensions> (comma-separated)\n" + \
		"\t[optional] -m \t\t\t NB: by default, the search is done by creation date, by adding the [-m] option, the search will be done by modification date\n\n"
	)
	
	return

def convertDate2Time(strDate, endDate):
	# Converti une date en timestamp
	# return timestamp
	
	if endDate == True:
		time = (dt.datetime.strptime(strDate, "%d-%m-%Y") - t0).total_seconds() + 86340
	
	else:
		time = (dt.datetime.strptime(strDate, "%d-%m-%Y") - t0).total_seconds()
	
	return time

def convertTime2strDate(t):
	# Converti un timestamp en date human-readable
	# return human-readable datetime
	
	return dt.datetime.utcfromtimestamp(t).strftime('%d-%m-%Y %H:%M')

# -------------------
# VARIABLES
# -------------------

# Informations variables

version = "0.2"
releaseDate = "28.08.2020"
author = "Yann MANET <yann.manet@unige.ch>\nUniversity of Geneva - Switzerland"

# Display variables

figlet = " ___  ___  _    ___\n| __>| __>| |_ | . \\\n| _> | _> | . \| | |\n|_|  |_|  |___/|___/"
screenDelimiter = "----------------------------------------------------------------------------------------------\n"
screenDelimiterBig = "==========================================================================================="
screenDelimiterErr = "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

title = screenDelimiterBig +"\n"+ figlet +".py (Find Files by Dates)\n\nVersion: "+ version +", Date: "+ releaseDate +"\nAuthor: "+ author +"\n\n"+ screenDelimiterBig

t0 = dt.datetime.utcfromtimestamp(0)
path = "."
startdate = int(convertDate2Time(dt.datetime.now().strftime("%d-%m-%Y"), False))
enddate = int(convertDate2Time(dt.datetime.now().strftime("%d-%m-%Y"), True))
index = -1
datePattern = "(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})"

filter = []

# Rafraichi le terminal
os.system('cls' if os.name == 'nt' else 'clear')

# -------------------
# PARAMETRES
# -------------------

try:
	opts, arg = getopt.getopt(sys.argv[1:], "h:p:s:e:f:m", ["--help", "path=", "start=", "end=", "filter="])

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
			usage()
			print(screenDelimiterErr + "\nError: Parameter ["+ opt +"]: Path is invalid\n" + screenDelimiterErr)
			exit(2)

	elif opt in ("-s", "--start"):
		
		p = re.compile(datePattern)
		
		if str(p.match(arg)) == "None":
			usage()
			print(screenDelimiterErr + "\nError: Parameter ["+ opt +"]: Invalid date format\n" + screenDelimiterErr )
			exit(2)
		
		startdate = int(convertDate2Time(arg, False))

	elif opt in ("-e", "--end"):

		p = re.compile(datePattern)
		
		if str(p.match(arg)) == "None":
			usage()
			print(screenDelimiterErr + "\nError: Parameter ["+ opt +"]: Invalid date format\n" + screenDelimiterErr )
			exit(2)
		
		
		enddate = int(convertDate2Time(arg, True))
	
	elif opt in ("-f", "--filter"):
		
		filter = arg.split(",")
		
	elif opt == "-m":
		index = -2

# -------------------
# INFOS
# -------------------

# Affichage du titre
print (title)

# Affichage des informations de recherche
print(	
	">> List by file modification date" if index == -2 else ">> List by file creation date\n" + \
	">>>> In: "+ path +"\n" + \
	">>>> Between "+ convertTime2strDate(startdate) +" and "+ convertTime2strDate(enddate)
)

# Affichage si filtre activé
if len(filter) > 0:
	print (">>>> Filter on extension(s): "+ str(filter))
	
print (
	">>>> List generated on " + dt.datetime.now().strftime("%d-%m-%Y %H:%M") +"\n" + \
	screenDelimiter + \
	screenDelimiter + \
	"DATETIME [UTC]\t | \tFILENAME\t | \tPATH\n" + \
	screenDelimiter
)

# -------------------
# RECHERCHES ET AFFICHAGE RESULTATS
# -------------------

# Parcours du répertoire 
# et de ses sous-répertoires

for (dirpath, dirnames, filenames) in os.walk(path):
	
	for filename in filenames:
		
		# Contrôle de l'OS
		# le but est de recréer le path 
		# dans le cas de Windows le séparateur est \
		# dans le cas d'Unix le séparateur est /
		
		if os.name == 'nt':
			f = '\\'.join([dirpath,filename]) # Windows
		else:
			f = '/'.join([dirpath,filename]) # Unix
			
		ctime = os.stat(f)[index] # Récupération du timestamp du fichier
		
		extension = f.split(os.extsep)[-1] # Récupération de l'extension du fichier
		
		# Si la longueur de la liste filtre est inférieur à 1
		# OU (donc si supérieur à 0), l'extension du fichier en cours
		# se trouve dans la liste de filtre
		
		if len(filter) < 1 or extension in filter:
			
			if ctime>=startdate and ctime <=enddate:
				
				print (
					convertTime2strDate(ctime) + "\t" + \
					filename + "\t" + \
					f
				)
				
			

print (screenDelimiter)

exit(0)
