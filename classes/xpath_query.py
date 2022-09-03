import os
import xml.etree.ElementTree as ET
from pathlib import Path


class XpathQuery(object):
    def __init__(self, filename, query_class, query_id, scope):
        self.filename = filename
        self.query_class = query_class
        self.query_id = query_id
        self.scope = scope
        self.register_namespaces()

    def register_namespaces(self):
        if self.scope != "cds":
            self.namespaces = {
                'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0',
                'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0'
            }
        else:
            self.namespaces = {
                'ns2': 'http://www.eurodyn.com/Tariff/services/DispatchDataExportXMLData/v03'
            }
            self.namespaces = {}
        for ns in self.namespaces:
            ET.register_namespace(ns, self.namespaces[ns])

    def run_query(self):
        self.root = ET.parse(self.filename)
        if self.scope != "cds":
            if self.query_class == "commodity":
                ret = self.run_query_commodity_taric()
            elif self.query_class == "measure":
                ret = self.run_query_measure_taric()
            elif self.query_class == "measure_type":
                ret = self.run_query_measure_type_taric()
            elif self.query_class == "geographical_area":
                ret = self.run_query_geographical_area_taric()
            elif self.query_class == "commodity_measure":
                ret = self.run_query_commodity_measure_taric()
        else:
            if self.query_class == "commodity":
                ret = self.run_query_commodity_cds()
            elif self.query_class == "measure":
                ret = self.run_query_measure_cds()
            elif self.query_class == "measure_type":
                ret = self.run_query_measure_type_cds()
            elif self.query_class == "geographical_area":
                ret = self.run_query_geographical_area_cds()
            elif self.query_class == "commodity_measure":
                ret = self.run_query_commodity_measure_cds()
        return ret

    def run_query_commodity_taric(self):
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

    def run_query_commodity_cds(self):
        ret = []
        self.query = ".//GoodsNomenclature[goodsNomenclatureItemId = '{item}']".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            sid = self.get_value(elem, "sid")
            productline_suffix = self.get_value(elem, "produclineSuffix")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, sid, productline_suffix, transaction_id, validity_start_date, validity_end_date)
            ret.append(obj)
        return ret

    def run_query_measure_taric(self):
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

    def run_query_measure_cds(self):
        ret = []
        self.query = ".//Measure[sid = '{item}']".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_measure_type_taric(self):
        ret = []
        self.query = ".//oub:measure[oub:measure.type = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = self.get_value(elem, "oub:transaction.id")
            measure_sid = self.get_value(elem, "oub:measure.sid")
            goods_nomenclature_sid = self.get_value(elem, "oub:measure/oub:goods.nomenclature.sid")
            goods_nomenclature_item_id = self.get_value(elem, "oub:measure/oub:goods.nomenclature.item.id")
            validity_start_date = self.get_value(elem, "oub:measure/oub:validity.start.date")
            validity_end_date = self.get_value(elem, "oub:measure/oub:validity.end.date")
            measure_type_id = self.get_value(elem, "oub:measure/oub:measure.type")
            geographical_area_id = self.get_value(elem, "oub:measure/oub:geographical.area")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_measure_type_cds(self):
        ret = []
        self.query = ".//Measure/measureType/[measureTypeId = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(elem, "geographicalArea/geographicalAreaId")

            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_geographical_area_taric(self):
        ret = []
        self.query = ".//oub:measure[oub:geographical.area = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = self.get_value(elem, "oub:transaction.id")
            measure_sid = self.get_value(elem, "oub:measure.sid")
            goods_nomenclature_sid = self.get_value(elem, "oub:measure/oub:goods.nomenclature.sid")
            goods_nomenclature_item_id = self.get_value(elem, "oub:measure/oub:goods.nomenclature.item.id")
            validity_start_date = self.get_value(elem, "oub:measure/oub:validity.start.date")
            validity_end_date = self.get_value(elem, "oub:measure/oub:validity.end.date")
            measure_type_id = self.get_value(elem, "oub:measure/oub:measure.type")
            geographical_area_id = self.get_value(elem, "oub:measure/oub:geographical.area")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_geographical_area_cds(self):
        ret = []
        self.query = ".//Measure/geographicalArea[geographicalAreaId = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def run_query_commodity_measure_cds(self):
        ret = []
        self.query = ".//Measure/goodsNomenclature[goodsNomenclatureItemId = '{item}']/..".format(item=self.query_id)
        for elem in self.root.findall(self.query, self.namespaces):
            transaction_id = "n/a"
            measure_sid = self.get_value(elem, "sid")
            goods_nomenclature_sid = self.get_value(elem, "goodsNomenclature/sid")
            goods_nomenclature_item_id = self.get_value(elem, "goodsNomenclature/goodsNomenclatureItemId")
            validity_start_date = self.get_value(elem, "validityStartDate")
            validity_end_date = self.get_value(elem, "validityEndDate")
            measure_type_id = self.get_value(elem, "measureType/measureTypeId")
            geographical_area_id = self.get_value(elem, "geographicalArea/geographicalAreaId")
            filename = Path(self.filename).stem
            obj = (filename, self.query_id, transaction_id, measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date, measure_type_id, geographical_area_id, goods_nomenclature_sid)
            ret.append(obj)
        return ret

    def get_value(self, elem, query):
        obj = elem.find(query, self.namespaces)
        if obj is None:
            return ""
        else:
            return obj.text
