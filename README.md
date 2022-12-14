---------------------------------------------------------
# FFbD.py (Find Files by Dates) v1.0.1

Author: Yann MANET <yann.manet@unige.ch>
University of Geneva - Switzerland
---------------------------------------------------------

[![Quality Gate Status](https://ispso-dev.unige.ch/sonarqube/api/project_badges/measure?project=Yann.Manet_ffbd_AYUKVkHyjuNyJIE-IoLr&metric=alert_status&token=75307ff1b186627caf1b03badbe274828666eec6)](https://ispso-dev.unige.ch/sonarqube/dashboard?id=Yann.Manet_ffbd_AYUKVkHyjuNyJIE-IoLr)
[![Vulnerabilities](https://ispso-dev.unige.ch/sonarqube/api/project_badges/measure?project=Yann.Manet_ffbd_AYUKVkHyjuNyJIE-IoLr&metric=vulnerabilities&token=75307ff1b186627caf1b03badbe274828666eec6)](https://ispso-dev.unige.ch/sonarqube/dashboard?id=Yann.Manet_ffbd_AYUKVkHyjuNyJIE-IoLr)

## Requisite:

FFbD needs the tinyhtml library to be installed

    pip install tinyhtml


## Usage:
    python3 run.py -p "<path>" -s <startdate (dd-mm-yyyy)> -e=<enddate (dd-mm-yyyy)> -f=<extensions (comma separated)> [-m] [--plugins <plugins to load (comma separated)>]
    python3 run.py --path "<path>" --start <startdate (dd-mm-yyyy)> --end <enddate (dd-mm-yyyy)> --filter <extensions (comma separated)> [-m] [--plugins <plugins to load (comma separated)>]

## Options:
	* [optional] -p or --path	<path of the directory to be analysed>, default = current directory
	* [optional] -s or --start	<start date> (dd-mm-yyyy), if missing = today's date
	* [optional] -e or --end	<end date> (dd-mm-yyyy), if missing = today's date
	* [optional] -f or --filter	<File extensions> (comma-separated)
	* [optional] -m			NB: by default, the search is done by creation date, by adding the [-m] option, the search will be done by modification date
    * [optional] --plugins <plugins to load (comma separated)>

## Example:
    python3 run.py -p /path/to/directory -s 12-12-2022 -e 13-12-2022 -f txt --plugins header_analysis
    