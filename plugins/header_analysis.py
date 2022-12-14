import os
from tinyhtml import h, raw
from FFbD import FFbd


class Plugin:
    plugin = "Header Analysis"
    version = "1.0.0"
    analyse = ["_HEADER.txt", "_HEADER.TXT"]
    analyseResult = "<tr><th colspan='3' class='text-right'>" \
                    "<a href='#' id='header_analysis_export_btn'>Export</a></th></tr>"

    """ 
        @desc: Launch the script
        @params: void
        @return: void
    """

    def run(self, parent):
        self.analyseResult += "<tr><th colspan='3'>Plugin: " + self.plugin + " in " \
                              + parent.path + "</th>" \
                              "</tr>"

        for (dir_path, dir_names, filenames) in os.walk(parent.path):
            for filename in filenames:
                if filename in self.analyse:
                    self.analyseResult += self.fileanalysis(filename)

        parent.additionalElements.append(
            h("table", klass=["table", "table-striped"], id="header_analysis")(raw(self.analyseResult))
        )
        FFbd.factory_html()

        return

    """ 
        @desc: Executes the file analysis
        @params:
            filename [String] File to analyse
        @return: String
    """

    @staticmethod
    def fileanalysis(filename):
        output = ""
        file = open(filename, "r")
        substrings = ["Method:"]

        for line in file:
            for substring in substrings:
                if line.find(substring) != -1:
                    split_1 = line.split("$ ")
                    split_2 = split_1[1].split(": ")

                    method_name = split_2[0]
                    method_path = "[empty]" if split_2[1] == "\n" else split_2[1].rstrip('\n')
                    output += "<tr><td>" + filename + "</td><td>" + method_name + "</td><td>" + method_path + "</td" \
                                                                                                              "></tr> "

        file.close()

        return output
