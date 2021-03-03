import os
import xlsxwriter


class Excel(object):
    def __init__(self):
        pass

    def create_excel(self, path, filename):
        # export-20210228T000000_20210228T235959-20210301T200034
        self.path = path
        self.filename = filename
        parts = self.filename.split("T")
        part0 = parts[0]
        parts = part0.split("-")
        part1 = parts[1]
        self.excel_filename = "CDS updates " + part1[0:4] + "-" + part1[4:6] + "-" + part1[6:] + ".xlsx"

        self.excel_path = self.path.replace("xml", "xlsx")
        self.excel_filename = os.path.join(self.excel_path, self.excel_filename)
        
        # Open rhe workbook
        self.workbook = xlsxwriter.Workbook(self.excel_filename)
        
        # Create the formats that will be used in all sheets
        self.format_bold = self.workbook.add_format({'bold': True})
        self.format_bold.set_align('top')
        self.format_bold.set_align('left')
        self.format_bold.set_bg_color("#f0f0f0")

        self.format_wrap = self.workbook.add_format({'text_wrap': True})
        self.format_wrap.set_align('top')
        self.format_wrap.set_align('left')

        self.format_force_text = self.workbook.add_format({'text_wrap': True})
        self.format_force_text.set_align('top')
        self.format_force_text.set_align('left')
        self.format_force_text.set_num_format('@')
        

    def close_excel(self):
        self.workbook.close()
