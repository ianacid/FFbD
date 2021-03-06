---------------------------------------------------------

# FFbD.py (Find Files by Dates) v0.3

Author: Yann MANET <yann.manet@unige.ch>

University of Geneva - Switzerland

---------------------------------------------------------


## Usage:
- FFbD.py -p <path to search (between quotes)> -s <startdate (dd-mm-yyyy)> -e <enddate (dd-mm-yyyy)> -f <extensions (comma separated)> [-m]
- FFbD.py --path <path to search (between quotes)> --start <startdate (dd-mm-yyyy)> --end <enddate (dd-mm-yyyy)> --filter <extensions (comma separated)> [-m]


## Options:
	* [required] -p or --path	<path of the directory to be analysed between quotes>
	* [optional] -s or --start	<search start date> (dd-mm-yyyy), if missing = today's date
	* [optional] -e or --end	<search end date> (dd-mm-yyyy), if missing = today's date
	* [optional] -f or --filter	<File extensions> (comma-separated)
	* [optional] -m			NB: by default, the search is done by creation date, by adding the [-m] option, the search will be done by modification date
