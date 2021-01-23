import sys
from classes.master import Master
from cds_objects.footnote_description import FootnoteDescription
import classes.globals as g


class Footnote(Master):

    def __init__(self, md_file, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.md_file = md_file
        self.descriptions = []
        self.description_string = ""
        self.get_data()
        self.write_data()

    def get_data(self):
        self.footnote_id = Master.process_null(self.elem.find("footnoteId"))
        self.footnote_type_id = Master.process_null(self.elem.find("footnoteType/footnoteTypeId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.get_descriptions()

    def write_data(self):
        # Write the markdown
        self.md_file.new_header(level=2, title=self.operation_text + " footnote")
        tbl = ["Field", "Value",
               "Footnote ID", self.footnote_id + " (" + self.footnote_type_id + self.footnote_id + ")",
               "Footnote type ID", self.footnote_type_id,
               "Validity start date", Master.format_date(self.validity_start_date),
               "Validity end date", Master.format_date(self.validity_end_date)
               ]
        tbl += self.descriptions
        self.md_file.new_table(columns=2, rows=int(len(tbl)/2), text=tbl, text_align='left')

        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " footnote", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.footnote_type_id + self.footnote_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.footnote_type_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, self.footnote_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, self.description_string, g.excel.format_wrap)

    def get_descriptions(self):
        footnote_descriptions = self.elem.findall('footnoteDescriptionPeriod')
        if footnote_descriptions:
            for footnote_description in footnote_descriptions:
                obj = FootnoteDescription(self.md_file, footnote_description)
                self.descriptions += obj.tbl
                self.description_string += obj.description_string