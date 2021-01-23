import os
from .xml_file import XmlFile


class Parser(object):
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "resources")
        self.path = os.path.join(self.path, "xml")

    def parse_files(self):
        file_list = os.listdir(self.path)
        file_list.sort()
        for filename in file_list:
            if filename.endswith(".xml"):
                xml_file = XmlFile(filename)
                xml_file.parse_xml()
            else:
                continue
