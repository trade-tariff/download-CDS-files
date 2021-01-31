import os
from dotenv import load_dotenv
from .xml_file import XmlFile


class Parser(object):
    def __init__(self):
        load_dotenv('.env')
        self.OVERWRITE_XLSX = int(os.getenv('OVERWRITE_XLSX'))
        self.path = os.path.join(os.getcwd(), "resources")
        self.xml_path = os.path.join(self.path, "xml")
        self.xlsx_path = os.path.join(self.path, "xlsx")

    def parse_files(self):
        file_list = os.listdir(self.xml_path)
        file_list.sort()
        for filename in file_list:
            if filename.endswith(".xml"):
                if self.OVERWRITE_XLSX == 1:
                    proceed = True
                else:
                    proceed = not self.check_exists(filename)
                if proceed:
                    xml_file = XmlFile(filename)
                    xml_file.parse_xml()
            else:
                continue

    def check_exists(self, filename):
        filename = filename.replace("xml", "xlsx")
        xlsx_filename = os.path.join(self.xlsx_path, filename)
        exists = os.path.exists(xlsx_filename)
        return exists
