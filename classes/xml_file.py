import os
import sys
import json
import markdown
import xml.etree.ElementTree as ET
import classes.globals as g
from mdutils.mdutils import MdUtils
from mdutils import Html

import classes.functions as func
from cds_objects.footnote_type import FootnoteType
from cds_objects.footnote import Footnote
from cds_objects.additional_code import AdditionalCode
from cds_objects.measure import Measure
from cds_objects.goods_nomenclature import GoodsNomenclature
from cds_objects.quota_order_number import QuotaOrderNumber
from cds_objects.quota_definition import QuotaDefinition
from cds_objects.geographical_area import GeographicalArea
from classes.excel import Excel


class XmlFile(object):
    def __init__(self, filename):
        self.markdown = ""
        self.filename = filename
        self.path = os.path.join(os.getcwd(), "resources")
        self.path = os.path.join(self.path, "xml")
        self.file_path = os.path.join(self.path, self.filename)

    def parse_xml(self):
        # Create the Excel
        g.excel = Excel()
        g.excel.create_excel(self.path, self.filename)
        print("Creating file", self.filename.replace("xml", "xlsx"))

        self.create_markdown_file()  # Create the markdown file
        tree = ET.parse(self.file_path)
        self.root = tree.getroot()
        self.get_results_info()
        self.parse_filename()

        self.get_footnote_types()
        self.get_footnotes()
        self.get_additional_codes()
        self.get_measures()
        self.get_commodities()
        self.get_quota_order_numbers()
        self.get_quota_definitions()
        self.get_geographical_areas()

        self.table_of_contents()
        self.save_markdown_file()  # Save the markdown file
        self.convert_to_html()  # Convert file to html
        # g.excel.close_excel()

        self.write_changes()

    def write_changes(self):
        self.json_path = self.path.replace("xml", "json")
        temp = self.filename.split("T")[0] + ".json"
        self.json_filename = temp # self.filename.replace("xml", "json")
        self.json_filename = os.path.join(self.json_path, self.json_filename)

        my_dict = {}
        changes = []
        consolidated_commodities = []
        measures = []
        commodities = []
        quota_definitions = []
        summary = {}
        summary["execution_date"] = self.execution_date
        summary["change_count"] = str(len(g.change_list))
        for change in g.change_list:
            if change.object_type == "Measure":
                measures.append(change.__dict__)
                consolidated_commodities += change.impacted_end_lines

            elif change.object_type == "Commodity":
                commodities.append(change.__dict__)
                consolidated_commodities += change.impacted_end_lines

            elif change.object_type == "Quota definition":
                quota_definitions.append(change.__dict__)
                consolidated_commodities += change.impacted_end_lines
                
        consolidated_commodities = list(set(consolidated_commodities))
        consolidated_commodities.sort()

        my_dict["summary"] = summary
        my_dict["updated_commodity_codes"] = consolidated_commodities
        my_dict["commodity_changes"] = commodities
        my_dict["measure_changes"] = measures
        my_dict["quota_definition_changes"] = quota_definitions
        
        f = open(self.json_filename, "w+")
        my_string = json.dumps(my_dict, indent=2, sort_keys=False)
        f.write(my_string)
        f.close()

        sys.exit()

    def table_of_contents(self):
        self.md_file.new_table_of_contents(table_title='Contents', depth=1)

    def get_footnote_types(self):
        row_count = 0
        footnote_types = self.root.find('.//findFootnoteTypeByDatesResponse')
        if footnote_types:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Footnote types")
            data = ('Action', 'Footnote type ID', 'Application code',
                    'Start date', 'End date', 'Description')
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 20)
            worksheet.set_column(5, 5, 50)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(level=1, title="Changes to footnote types")

            # Get data
            footnote_types = footnote_types.findall("FootnoteType")
            for footnote_type in footnote_types:
                row_count += 1
                FootnoteType(self.md_file, footnote_type, worksheet, row_count)

    def get_footnotes(self):
        row_count = 0
        footnotes = self.root.find('.//findFootnoteByDatesResponse')
        if footnotes:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Footnotes")
            data = ('Action', 'Combined', 'Footnote type ID',
                    'Footnote ID', 'Start date', 'End date', 'Description')
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 5, 20)
            worksheet.set_column(6, 6, 50)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(level=1, title="Changes to footnotes")

            # Get data
            footnotes = footnotes.findall("Footnote")
            for footnote in footnotes:
                row_count += 1
                Footnote(self.md_file, footnote, worksheet, row_count)

    def get_additional_codes(self):
        row_count = 0
        additional_codes = self.root.find(
            './/findAdditionalCodeByDatesResponse')
        if additional_codes:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Additional codes")
            data = ('Action', 'Additional code type', 'Additional code ID',
                    'Start date', 'End date', 'Description')
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 20)
            worksheet.set_column(5, 5, 50)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(
                level=1, title="Changes to additional codes")

            # Get data
            additional_codes = additional_codes.findall("AdditionalCode")
            for additional_code in additional_codes:
                row_count += 1
                AdditionalCode(self.md_file, additional_code,
                               worksheet, row_count)

    def get_measures(self):
        row_count = 0
        measures = self.root.find('.//findMeasureByDatesResponseHistory')
        if measures:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Measures")
            data = (
                'Action', 'SID', 'Commodity code', 'Additional code', 'Measure type',
                'Geographical area', 'Quota order number', 'Start date',
                'End date', 'Duty', 'Excluded areas', 'Footnotes', 'Conditions'
            )
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 8, 20)
            worksheet.set_column(4, 5, 40)
            worksheet.set_column(9, 9, 40)
            worksheet.set_column(10, 11, 30)
            worksheet.set_column(12, 12, 50)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(level=1, title="Changes to measures")

            # Get data
            measures = measures.findall("Measure")
            for measure in measures:
                row_count += 1
                Measure(self.md_file, measure, worksheet, row_count)

    def get_commodities(self):
        row_count = 0
        commodities = self.root.find('.//findGoodsNomenclatureByDatesResponse')
        if commodities:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Commodities")
            data = ('Action', 'SID', 'Commodity code', 'Product line suffix',
                    'Statistical indicator', 'Start date', 'End date', 'Description')
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 6, 20)
            worksheet.set_column(7, 7, 50)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(
                level=1, title="Changes to commodity codes")
            commodities = commodities.findall("GoodsNomenclature")
            for commodity in commodities:
                row_count += 1
                GoodsNomenclature(self.md_file, commodity,
                                  worksheet, row_count)

    def get_quota_order_numbers(self):
        row_count = 0
        quotas = self.root.find(
            './/findQuotaOrderNumberByDatesResponseHistory')
        if quotas:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Quota order numbers")
            data = ('Action', 'SID', 'Order number', 'Start date', 'End date')
            worksheet.write_row('A1', data, g.excel.format_bold)
            worksheet.set_column(0, 0, 40)
            worksheet.set_column(1, 4, 20)
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(
                level=1, title="Changes to quota order numbers")

            # Get data
            quotas = quotas.findall("QuotaOrderNumber")
            for quota in quotas:
                row_count += 1
                QuotaOrderNumber(self.md_file, quota, worksheet, row_count)

    def get_geographical_areas(self):
        row_count = 0
        geographical_areas = self.root.find(
            './/findGeographicalAreaByDatesResponse')
        if geographical_areas:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Geographical areas")
            data = (
                'Action', 'Geographical area ID', 'SID',
                "Start date", 'End date',
                'Description(s)', 'Current memberships', 'All memberships', 'Parent group SID')
            widths = [30, 20, 15, 15, 20, 50, 70, 70, 15]
            worksheet.write_row('A1', data, g.excel.format_bold)
            for i in range(0, len(widths)):
                worksheet.set_column(i, i, widths[i])
            worksheet.freeze_panes(1, 0)

            # Get data
            geographical_areas = geographical_areas.findall("GeographicalArea")
            geographical_area_objects = []
            for geographical_area in geographical_areas:
                row_count += 1
                geographical_area_object = GeographicalArea(
                    self.md_file, geographical_area, worksheet, row_count)
                geographical_area_objects.append(geographical_area_object)

            geographical_area_objects = sorted(
                geographical_area_objects, key=lambda x: x.geographical_area_id, reverse=False)

            row_count = 1
            for geographical_area_object in geographical_area_objects:
                geographical_area_object.row_count = row_count
                geographical_area_object.write_data()
                row_count += 1

    def get_quota_definitions(self):
        row_count = 0
        quota_definitions = self.root.find(
            './/findQuotaDefinitionByDatesResponseHistory')
        if quota_definitions:
            # Write Excel column headers
            worksheet = g.excel.workbook.add_worksheet("Quota definitions")
            worksheet.write(
                'A1', "Please be careful when checking quota balances - each file may contains multiple updates on the same quota definition", g.excel.format_bold)

            data = ('Action', 'Quota order number', 'Balance updates', "Sample commodities", 'SID',
                    'Critical state', 'Critical threshold', 'Initial volume', 'Volume',
                    'Maximum precision', 'Start date', 'End date')
            widths = [30, 20, 50, 70, 20, 20, 20, 20, 20, 20, 20, 20]
            worksheet.write_row('A3', data, g.excel.format_bold)
            for i in range(0, len(widths)):
                worksheet.set_column(i, i, widths[i])
            worksheet.freeze_panes(1, 0)

            # Write markdown header
            self.md_file.new_header(
                level=1, title="Changes to quota definitions")

            # Get data
            quota_definitions = quota_definitions.findall("QuotaDefinition")
            quota_definition_objects = []
            for quota_definition in quota_definitions:
                row_count += 1
                quota_definition_object = QuotaDefinition(
                    self.md_file, quota_definition, worksheet, row_count)
                quota_definition_objects.append(quota_definition_object)

            quota_definition_objects = sorted(
                quota_definition_objects, key=lambda x: x.quota_order_number_id, reverse=False)

            row_count = 3
            for quota_definition_object in quota_definition_objects:
                quota_definition_object.row_count = row_count
                quota_definition_object.write_data()
                row_count += 1

    def create_markdown_file(self):
        self.md_path = self.path.replace("xml", "md")
        self.md_filename = self.filename.replace("xml", "md")
        self.md_filename = os.path.join(self.md_path, self.md_filename)
        self.md_file = MdUtils(file_name=self.md_filename,
                               title='CDS data extract')

    def save_markdown_file(self):
        self.md_file.create_md_file()

    def get_results_info(self):
        results_info = self.root.find('ResultsInfo')
        self.total_records = results_info.find("totalRecords").text
        self.execution_date = results_info.find("executionDate").text

    def parse_filename(self):
        self.export_date = func.parse_date(self.filename[7:15])
        self.range_start = func.parse_date(self.filename[23:31])
        self.range_end = func.parse_date(self.filename[39:47])

        self.md_file.new_header(level=1, title="Core info")
        tbl = ["Field", "Value", "Record count", self.total_records, "Export date",
               self.export_date, "Range start", self.range_start, "Range end", self.range_end]
        self.md_file.new_table(columns=2, rows=5, text=tbl, text_align='left')

    def convert_to_html(self):
        return
        self.html_path = self.path.replace("xml", "html")
        self.html_filename = self.filename.replace("xml", "html")
        self.html_filename = os.path.join(self.html_path, self.html_filename)

        self.docx_path = self.path.replace("xml", "docx")
        self.docx_filename = self.filename.replace("xml", "docx")
        self.docx_filename = os.path.join(self.docx_path, self.docx_filename)

        self.md_file = MdUtils(file_name=self.html_filename,
                               title='CDS data extract')

        # Convert to HTML
        css_file = os.path.join(os.getcwd(), "css")
        css_file = os.path.join(css_file, "custom.css")

        # os.system("pandoc --quiet '" + self.md_filename + "' -f markdown -t html -s -o  '" + self.html_filename + "'")
        # os.system("pandoc --quiet '" + self.md_filename + "' -f markdown -t docx -s -o  '" + self.docx_filename + "'")
