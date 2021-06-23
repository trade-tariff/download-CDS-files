import os
import sys
from datetime import datetime
from classes.database import Database
from classes.classification import Classification


class CodeList(object):
    def create_commodity_extract(self):
        print("Creating commodity code extract")
        d = datetime.now()
        d2 = datetime.strftime(d, '%Y-%m-%d')
        for i in range(0, 10):
            self.classifications = []
            chapter = str(i) + "%"
            sql = """
            select goods_nomenclature_sid, goods_nomenclature_item_id, producline_suffix, number_indents, leaf
            from utils.goods_nomenclature_export_new('""" + chapter + """', '""" + d2 + """')
            where validity_end_date is null
            order by goods_nomenclature_item_id, producline_suffix;
            """

            print("Getting complete commodity code list for codes beginning with " + str(i))
            d = Database()
            rows = d.run_query(sql)
            for row in rows:
                self.validity_start_date = str(row[0])
                classification = Classification(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
                self.classifications.append(classification)

            self.folder = os.getcwd()
            self.folder = os.path.join(self.folder, "resources")
            self.folder = os.path.join(self.folder, "csv")
            filename = os.path.join(self.folder, "commodities_" + str(i) + ".csv")

            f = open(filename, "w+")
            field_names = '"SID","Commodity code","Product line suffix","Indentation","End line"\n'
            f.write(field_names)
            for item in self.classifications:
                f.write(item.extract_row())
            f.close()
            
        self.concatenate()

    def concatenate(self):
        return