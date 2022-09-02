import os
import xml.etree.ElementTree as ET
from pathlib import Path


class XpathMarkdown(object):
    def __init__(self, records, query_class, query_id):
        self.records = records
        self.query_class = query_class
        self.query_id = query_id
        self.markdown = ""
        self.make_folders()
        self.get_filename()

    def make_folders(self):
        resources_folder = os.path.join(os.getcwd(), "resources")
        queries_folder = os.path.join(resources_folder, "queries")
        self.commodities_folder = os.path.join(queries_folder, "commodities")
        self.measures_folder = os.path.join(queries_folder, "measures")
        self.make_folder(queries_folder)
        self.make_folder(self.commodities_folder)
        self.make_folder(self.measures_folder)

    def make_folder(self, folder):
        try:
            os.mkdir(folder)
        except Exception as e:
            pass

    def get_filename(self):
        self.filename = "{qc}_{qid}.md".format(qc=self.query_class, qid=self.query_id)
        if self.query_class == "commodity":
            self.filepath = os.path.join(self.commodities_folder, self.filename)
        elif self.query_class == "measure":
            self.filepath = os.path.join(self.measures_folder, self.filename)

    def write_markdown(self):
        if self.query_class == "commodity":
            self.write_markdown_commodity()
        elif self.query_class == "measure":
            self.write_markdown_measure()

    def write_markdown_commodity(self):
        self.markdown += "# Instances of commodity code {item}\n\n".format(item=self.query_id)
        for record in self.records:
            self.markdown += "## {filename}\n\n".format(filename=record[0])
            self.markdown += "- Transaction ID = {item}\n".format(item=record[2])
            self.markdown += "- Commodity code = {item}\n".format(item=record[1])
            self.markdown += "- PLS = {item}\n".format(item=record[3])
            self.markdown += "- SID = {item}\n".format(item=record[4])
            self.markdown += "- Start date = {item}\n".format(item=record[5])
            self.markdown += "- End date = {item}\n\n".format(item=record[6])

        f = open(self.filepath, "w")
        f.write(self.markdown)
        f.close()

    def write_markdown_measure(self):
        # obj = (filename, self.query_id, transaction_id, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
        self.markdown += "# Instances of measure {item}\n\n".format(item=self.query_id)
        for record in self.records:
            self.markdown += "## {item}\n\n".format(item=record[0])
            self.markdown += "- Transaction ID = {item}\n".format(item=record[2])
            self.markdown += "- Commodity code = {item}\n".format(item=record[3])
            self.markdown += "- Start date = {item}\n".format(item=record[4])
            self.markdown += "- End date = {item}\n".format(item=record[5])
            self.markdown += "- Measure type ID = {item}\n".format(item=record[6])
            self.markdown += "- Geographical area ID = {item}\n".format(item=record[7])
            self.markdown += "- Goods nomenclature SID = {item}\n\n".format(item=record[8])

        f = open(self.filepath, "w")
        f.write(self.markdown)
        f.close()