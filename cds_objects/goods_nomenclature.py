import sys
from classes.master import Master
from cds_objects.goods_nomenclature_description import GoodsNomenclatureDescription
import classes.globals as g
from cds_objects.change import CommodityChange


class GoodsNomenclature(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.descriptions = []
        self.description_string = ""
        self.get_data()
        # self.write_data()

    def get_data(self):
        self.goods_nomenclature_sid = Master.process_null(self.elem.find("sid"))
        self.goods_nomenclature_item_id = Master.process_null(self.elem.find("goodsNomenclatureItemId"))
        self.product_line_suffix = Master.process_null(self.elem.find("produclineSuffix"))
        self.statistical_indicator = Master.process_null(self.elem.find("statisticalIndicator"))
        self.validity_start_date = Master.process_null(
            self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(
            self.elem.find("validityEndDate"))
        self.get_descriptions()
        
        change = CommodityChange(self.goods_nomenclature_sid, self.goods_nomenclature_item_id, self.product_line_suffix, "Commodity", self.operation)
        g.change_list.append(change)

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " commodity", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.goods_nomenclature_item_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.product_line_suffix, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, self.description_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, self.statistical_indicator, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 7, self.goods_nomenclature_sid, g.excel.format_wrap)

    def get_descriptions(self):
        descriptions = self.elem.findall('goodsNomenclatureDescriptionPeriod')
        if descriptions:
            for description in descriptions:
                obj = GoodsNomenclatureDescription(description)
                if obj.tbl is not None:
                    self.descriptions += obj.tbl
                self.description_string = obj.description_string
