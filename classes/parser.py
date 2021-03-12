import os
import sys
import csv
from dotenv import load_dotenv

import classes.globals as g
import classes.functions as f
from classes.database import Database
from classes.classification import Classification
from .xml_file import XmlFile


class Parser(object):
    def __init__(self):
        load_dotenv('.env')
        self.OVERWRITE_XLSX = int(os.getenv('OVERWRITE_XLSX'))
        self.path = os.path.join(os.getcwd(), "resources")
        self.xml_path = os.path.join(self.path, "xml")
        self.xlsx_path = os.path.join(self.path, "xlsx")

    def parse_files(self):
        self.get_quota_definitions()
        self.get_codes()
        file_list = os.listdir(self.xml_path)
        file_list.sort()
        for filename in file_list:
            if filename.endswith(".xml"):
                if self.OVERWRITE_XLSX == 1:
                    proceed = True
                else:
                    excel_filename = f.xml_to_xlsx_filename(filename)
                    proceed = not self.check_exists(excel_filename)
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
    
    def get_codes(self):
        g.code_lists = {}
        for i in range(0, 10):
            code_key = "codes_" + str(i)
            codes = []
            path = os.getcwd()
            resources_path = os.path.join(path, "resources")
            csv_path = os.path.join(resources_path, "csv")
            csv_path = os.path.join(csv_path, "commodities_" + str(i) + ".csv")

            with open(csv_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0

                for row in csv_reader:
                    if line_count != 0:
                        code = Classification(row[0], row[1], row[2], row[3], row[4])
                        codes.append(code)
                    
                    line_count += 1
                    
            g.code_lists[code_key] = codes

    def get_quota_definitions(self):
        g.definition_list = {}
        d = Database()
        sql = """select quota_definition_sid, quota_order_number_id, m.goods_nomenclature_item_id 
        from quota_definitions qd, measures m
        where m.ordernumber = qd.quota_order_number_id 
        and qd.validity_start_date >= '2021-01-01'
        and m.validity_start_date >= '2021-01-01'
        order by 1, 2, 3;"""

        rows = d.run_query(sql)
        for row in rows:
            quota_definition_sid = row[0]
            goods_nomenclature_item_id = row[2]

            if quota_definition_sid not in g.definition_list:
                g.definition_list["sid_" + str(quota_definition_sid)] = []
                g.definition_list["sid_" + str(quota_definition_sid)].append(goods_nomenclature_item_id)
            else:
                g.definition_list["sid_" + str(quota_definition_sid)].append(goods_nomenclature_item_id)


        a = 1
