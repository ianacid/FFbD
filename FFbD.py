import datetime as dt
import getopt
import os
import re
import sys
from tinyhtml import html, h, frag, raw
import webbrowser
import importlib


class FFbd:
    # -------------------
    # VARIABLES
    # -------------------
    version = "1.0.1"
    releaseDate = "07.12.2022"

    author = "Yann MANET [<a class='text-decoration-none' " \
             "href='mailto:yann.manet@unige.ch'>yann.manet@unige.ch</a>]<br/>University of Geneva - Switzerland "
    logo = "<img src='img/logo.png' class='logo' alt='logo'/>"
    titleHTML = logo + "<br/><strong>Version:</strong> " + version + " - " + releaseDate + "<br/><strong>Author" \
                                                                                           ":</strong> " + author
    t0 = dt.datetime.utcfromtimestamp(0)
    path = "."
    datePattern = "(\d\d)-(\d\d)-(\d\d\d\d)"
    ffbd_filter = []
    opts = []
    plugins = []

    analyseResult = ""
    startdate = 0
    enddate = 0
    index = -1

    infoHTML = ""
    ffbdHTML = ""
    html_content = 0
    fragedElements = 0
    additionalElements = []

    def __init__(self):
        self.startdate = int(self.convert_date_to_time(dt.datetime.now().strftime("%d-%m-%Y"), False))
        self.enddate = int(self.convert_date_to_time(dt.datetime.now().strftime("%d-%m-%Y"), True))
        self.index = -1

    """ 
        @desc: Displays the help
        @params: void
        @return: void
    """

    @staticmethod
    def usage():
        print(
            "\nUsage:\n>> FFbD.py -p \"<path>\" -s <startdate (dd-mm-yyyy)> -e=<enddate (dd-mm-yyyy)> -f=<extensions "
            "(comma separated)> [-m] [--plugins <plugins to load (comma separated)>]\n" 
            ">> FFbD.py --path \"<path>\" --start <startdate (dd-mm-yyyy)> --end <enddate (dd-mm-yyyy)> --filter "
            "<extensions (comma separated)> [-m] [--plugins <plugins to load (comma separated)>]\n" 
            "\nOptions:\n" 
            "\t[optional] -p or --path \t<path of the directory to be analysed between quotes>\n" 
            "\t[optional] -s or --start \t<search start date> (dd-mm-yyyy), if missing = today's date\n"
            "\t[optional] -e or --end \t\t<search end date> (dd-mm-yyyy), if missing = today's date\n"
            "\t[optional] -f or --filter \t<File extensions> (comma-separated)\n"
            "\t[optional] -m \t\t\t NB: by default, the search is done by creation date, by adding the [-m] option, "
            "the search will be done by modification date\n"
            "\t[optional] --plugins <plugins to load (comma separated)>\t\t\t \n\n"
        )
        return

    """ 
        @desc: Convert a string date to date format 
        @params: 
            str_date [string] string date
            end_date [boolean] True if it is the end date
        @return: Date
    """

    def convert_date_to_time(self, str_date, end_date):
        if end_date:
            time = (dt.datetime.strptime(str_date, "%d-%m-%Y") - self.t0).total_seconds() + 86340
        else:
            time = (dt.datetime.strptime(str_date, "%d-%m-%Y") - self.t0).total_seconds()

        return time

    """ 
        @desc: Convert a date to a string date
        @params:
            date [Date] 
        @return: String
    """

    @staticmethod
    def convert_time_to_strdate(date):
        return dt.datetime.utcfromtimestamp(date).strftime('%d-%m-%Y %H:%M')

    """ 
        @desc: Analyzes the options and performs the requested functions
        @params: void
        @return: void
    """

    def options(self):
        try:
            self.opts, arg = getopt.getopt(sys.argv[1:], "h:p:s:e:f:m",
                                           ["--help", "path=", "start=", "end=", "filter=", "plugins="])

        except getopt.GetoptError:
            self.usage()
            exit(2)

        for opt, arg in self.opts:
            if opt in ("-h", "--help"):
                self.usage()
                exit()

            elif opt in ("-p", "--path"):
                self.path = arg

                if not os.path.isdir(self.path):
                    self.usage()
                    print("\nError: Parameter [" + opt + "]: Path is invalid\n")
                    exit(2)

            elif opt in ("-s", "--start"):

                p = re.compile(self.datePattern)

                if str(p.match(arg)) == "None":
                    self.usage()
                    print("\nError: Parameter [" + opt + "]: " + arg + "  " + str(
                        p.match(arg)) + " is an invalid date format\n")
                    exit(2)

                self.startdate = int(self.convert_date_to_time(arg, False))

            elif opt in ("-e", "--end"):

                p = re.compile(self.datePattern)

                if str(p.match(arg)) == "None":
                    self.usage()
                    print("\nError: Parameter [" + opt + "]: Invalid date format\n")
                    exit(2)

                self.enddate = int(self.convert_date_to_time(arg, True))

            elif opt in ("-f", "--filter"):

                self.ffbd_filter = arg.split(",")

            elif opt in "--plugins":

                plugins = arg.split(",")

                if plugins:
                    self.plugins = [
                        importlib.import_module("plugins." + plugin).Plugin() for plugin in plugins
                    ]

            elif opt == "-m":
                self.index = -2
        return

    """ 
        @desc: Builds the basic template of the HTML page
        @params: void
        @return: void
    """

    @staticmethod
    def factory_html():
        FFbd.html_content = html(lang="en")(
            h("head")(
                (h("title")("FFbD Report")),
                (h("link", rel="stylesheet", href="css/bootstrap.min.css")),
                (h("link", rel="stylesheet", href="css/css.css")),
            ),
            h("body")(
                FFbd.fragedElements,
                (addelmts for addelmts in FFbd.additionalElements),
                h("script", src="js/export.js")(),
            ),
        )
        return

    """ 
        @desc: Creation of the HTML file and deployment on the web browser
        @params: void
        @return: void
    """

    def factory_webpage(self):
        f = open('report/report.html', 'w')

        render_html = self.html_content.render()

        f.write(render_html)
        f.close()

        webbrowser.open('file:///' + os.getcwd() + '/' + 'report/report.html', 0, True)
        return

    """ 
        @desc: Builds information for the user based on the entered parameters
        @params: void
        @return: void
    """

    def factory_info_html(self):
        self.infoHTML = "<strong>List by file modification date</strong>" if self.index == -2 else "<strong>List by " \
                                                                                                   "file creation " \
                                                                                                   "date</strong> "
        self.infoHTML += "<br/>In: <strong>" + self.path + "</strong><br/> Between <strong>" \
                         + self.convert_time_to_strdate(self.startdate) + "</strong> and <strong>" \
                         + self.convert_time_to_strdate(self.enddate) + "</strong>"

        if len(self.ffbd_filter) > 0:
            self.infoHTML += "<br/>Filter on extension(s): <strong>" + str(self.ffbd_filter) + "</strong>"

        self.infoHTML += "<br/>List generated on <strong>" + dt.datetime.now().strftime("%d-%m-%Y %H:%M") + "</strong>"
        return

    """ 
        @desc: Launch the script
        @params: void
        @return: void
    """

    def run(self):
        self.options()
        self.factory_info_html()

        self.ffbdHTML = "<tr><th colspan='4' class='text-right'><a href='#' id='ffbd_export_btn'>Export</a></th></tr>" \
            "<tr><th>CREATION [UTC]</th><th>MODIFICATION [UTC]</th><th>FILENAME</th><th>PATH</th></tr>"

        for (dirpath, dirnames, filenames) in os.walk(self.path):

            for filename in filenames:

                file_path = '\\'.join([dirpath, filename]) if os.name == 'nt' else '/'.join([dirpath, filename])  # Unix

                ctime = os.stat(file_path)[self.index]
                extension = file_path.split(os.extsep)[-1]

                if len(self.ffbd_filter) < 1 or extension in self.ffbd_filter:
                    if self.startdate <= ctime <= self.enddate:
                        self.ffbdHTML += "<tr><td>" + self.convert_time_to_strdate(
                            os.stat(file_path)[-1]) + "</td><td>" + self.convert_time_to_strdate(
                            os.stat(file_path)[-2]) + "</td><td>" + filename + "</td><td>" + file_path + "</td></tr>"

        FFbd.fragedElements = frag(
            h("div", klass=["card", "text-bg-dark"])(h("div", klass="card-body")(raw(self.titleHTML))),
            h("div", klass=["card", "bg-light"])(h("div", klass="card-body")(raw(self.infoHTML))),
            h("hr"),
            h("table", klass=["table", "table-striped"], id="ffbd")(raw(self.ffbdHTML)),
            h("hr"),
        )
        return
