import os
import xml.etree.ElementTree as ET
from pathlib import Path


class XpathQuery(object):
    def __init__(self, filename, query_class, query_id):
        self.filename = filename
        self.query_class = query_class
        self.query_id = query_id
        self.register_namespaces()

    def register_namespaces(self):
        self.namespaces = {
            'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0',
            'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0'
        }
        for ns in self.namespaces:
            ET.register_namespace(ns, self.namespaces[ns])

    def run_query(self):
        self.root = ET.parse(self.filename)
        if self.query_class == "commodity":
            ret = self.run_query_commodity()
        elif self.query_class == "measure":
            ret = self.run_query_measure()
        return ret

    def run_query_commodity(self):
        ret = []
        self.query = ".//oub:goods.nomenclature[oub:goods.nomenclature.item.id = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = self.get_value(elem, "oub:transaction.id")
            sid = self.get_value(elem, "oub:goods.nomenclature/oub:goods.nomenclature.sid")
            productline_suffix = self.get_value(elem, "oub:goods.nomenclature/oub:producline.suffix")
            validity_start_date = self.get_value(elem, "oub:goods.nomenclature/oub:validity.start.date")
            validity_end_date = self.get_value(elem, "oub:goods.nomenclature/oub:validity.end.date")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, sid, productline_suffix, transaction_id, validity_start_date, validity_end_date)
            ret.append(obj)
        return ret

    def run_query_measure(self):
        ret = []
        self.query = ".//oub:measure[oub:measure.sid = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = self.get_value(elem, "oub:transaction.id")
            goods_nomenclature_sid = self.get_value(elem, "oub:measure/oub:goods.nomenclature.sid")
            goods_nomenclature_item_id = self.get_value(elem, "oub:measure/oub:goods.nomenclature.item.id")
            validity_start_date = self.get_value(elem, "oub:measure/oub:validity.start.date")
            validity_end_date = self.get_value(elem, "oub:measure/oub:validity.end.date")
            measure_type_id = self.get_value(elem, "oub:measure/oub:measure.type")
            geographical_area_id = self.get_value(elem, "oub:measure/oub:geographical.area")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def get_value(self, elem, query):
        obj = elem.find(query, self.namespaces)
        if obj is None:
            return ""
        else:
            return obj.text
