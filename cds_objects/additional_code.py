import sys
from classes.master import Master
from cds_objects.additional_code_description import AdditionalCodeDescription
import classes.globals as g


class AdditionalCode(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.descriptions = []
        self.description_string = ""
        self.get_data()
        self.write_data()

    def get_data(self):
        self.additional_code_sid = Master.process_null(self.elem.find("sid"))
        self.additional_code_id = Master.process_null(self.elem.find("additionalCodeCode"))
        self.additional_code_type_id = Master.process_null(self.elem.find("additionalCodeType/additionalCodeTypeId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.get_descriptions()

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " additional code", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.additional_code_type_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.additional_code_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.description_string, g.excel.format_wrap)

    def get_descriptions(self):
        additional_code_descriptions = self.elem.findall('additionalCodeDescriptionPeriod')
        if additional_code_descriptions:
            for additional_code_description in additional_code_descriptions:
                obj = AdditionalCodeDescription(additional_code_description)
                self.descriptions += obj.tbl
                self.description_string += obj.description_string