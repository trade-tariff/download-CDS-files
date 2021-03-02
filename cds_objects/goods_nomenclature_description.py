from classes.master import Master
import csv


class GoodsNomenclatureDescription(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.tbl = self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
            self.description = Master.process_null(self.elem.find("goodsNomenclatureDescription/description"))
            self.tbl = [
                "Description start date", Master.format_date(self.validity_start_date),
                "Description", self.description,
                ]
            self.description_string = self.description
        else:
            self.tbl = None
            self.description_string = ""
