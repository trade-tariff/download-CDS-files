import sys
from classes.master import Master
from cds_objects.additional_code_description import AdditionalCodeDescription
import classes.globals as g


class QuotaOrderNumber(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.descriptions = []
        self.get_data()
        self.write_data()

    def get_data(self):
        self.quota_order_number_sid = Master.process_null(self.elem.find("sid"))
        self.quota_order_number_id = Master.process_null(self.elem.find("quotaOrderNumberId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " quota order number", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.quota_order_number_sid, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.quota_order_number_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_end_date), g.excel.format_wrap)
