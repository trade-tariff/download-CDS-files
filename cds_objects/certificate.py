import sys
from classes.master import Master
from cds_objects.certificate_description import CertificateDescription
import classes.globals as g


class Certificate(Master):

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
        self.certificate_code = Master.process_null(self.elem.find("certificateCode"))
        self.certificate_type_code = Master.process_null(self.elem.find("certificateType/certificateTypeCode"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.get_descriptions()

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " certificate", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.certificate_type_code, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.certificate_code, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.description_string, g.excel.format_wrap)

    def get_descriptions(self):
        certificate_descriptions = self.elem.findall('certificateDescriptionPeriod')
        if certificate_descriptions:
            for certificate_description in certificate_descriptions:
                obj = CertificateDescription(certificate_description)
                self.descriptions += obj.tbl
                self.description_string += obj.description_string