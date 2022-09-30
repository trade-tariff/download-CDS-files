import xml.etree.ElementTree as ET
from classes.master import Master
import classes.globals as g


class FootnoteType(Master):
    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.get_data()
        self.write_data()

    def get_data(self):
        self.application_code = Master.process_null(self.elem.find("applicationCode"))
        self.footnote_type_id = Master.process_null(self.elem.find("footnoteTypeId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        footnote_type_description = self.elem.find('footnoteTypeDescription')
        if footnote_type_description:
            self.description = Master.process_null(footnote_type_description.find("description"))
        else:
            self.description = ""

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " footnote type", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.footnote_type_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.application_code, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.description, g.excel.format_wrap)
