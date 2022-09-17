import sys
from classes.master import Master
import classes.globals as g

from cds_objects.change import MeasureChange
from cds_objects.measure_component import MeasureComponent
from cds_objects.measure_condition import MeasureCondition
from cds_objects.measure_excluded_geographical_area import MeasureExcludedGeographicalArea
from cds_objects.footnote_association_measure import FootnoteAssociationMeasure


class Measure(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.combined_duty = ""
        self.footnote_string = ""
        self.descriptions = []
        self.duty_expression_array = []
        self.measure_condition_array = []
        self.get_data()

    def get_data(self):
        self.measure_sid = Master.process_null_int(self.elem.find("sid"))
        self.measure_generating_regulation_id = Master.process_null(
            self.elem.find("measureGeneratingRegulationId"))
        self.geographical_area_id = Master.process_null(
            self.elem.find("geographicalArea/geographicalAreaId"))
        self.goods_nomenclature_item_id = Master.process_null(
            self.elem.find("goodsNomenclature/goodsNomenclatureItemId"))
        self.measure_type_id = Master.process_null(
            self.elem.find("measureType/measureTypeId"))
        self.validity_start_date = Master.process_null(
            self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(
            self.elem.find("validityEndDate"))
        self.ordernumber = Master.process_null(
            self.elem.find("ordernumber"))
        self.additional_code_code = Master.process_null(
            self.elem.find("additionalCode/additionalCodeCode"))
        self.additional_code_type_id = Master.process_null(
            self.elem.find("additionalCode/additionalCodeType/additionalCodeTypeId"))
        self.additional_code = self.additional_code_type_id + self.additional_code_code

        self.get_geographical_area_description()
        self.get_measure_type_description()
        self.get_measure_components()
        self.get_measure_conditions()
        self.get_measure_excluded_geographical_areas()
        self.get_footnotes()

        change = MeasureChange(self.measure_sid, self.goods_nomenclature_item_id, "Measure", self.operation)
        g.change_list.append(change)

    def get_geographical_area_description(self):
        try:
            self.geographical_area_description = g.geography_dict[self.geographical_area_id]
        except Exception as e:
            print("Failure on geo area", self.geographical_area_id)
            sys.exit()

    def get_measure_type_description(self):
        self.measure_type_description = g.measure_type_dict[self.measure_type_id]

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " measure", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.goods_nomenclature_item_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.additional_code, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, self.measure_type_id + " (" + self.measure_type_description + ")", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, self.geographical_area_id + " (" + self.geographical_area_description + ")", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.ordernumber, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 7, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 8, self.combined_duty, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 9, self.exclusion_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 10, self.footnote_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 11, self.measure_condition_string_excel, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 12, self.measure_sid, g.excel.format_wrap)

    def get_measure_components(self):
        measure_components = self.elem.findall('measureComponent')
        self.measure_components = []
        self.combined_duty = ""

        if measure_components:
            for measure_component in measure_components:
                duty_string = MeasureComponent(measure_component).duty_string
                if duty_string is not None:
                    self.measure_components.append(duty_string)

        for item in self.measure_components:
            self.combined_duty += " " + item
        self.combined_duty = self.combined_duty.strip()
        self.duty_expression_array = [
            "Duty expression",
            self.combined_duty
        ]

    def get_measure_conditions(self):
        measure_conditions = self.elem.findall('measureCondition')
        self.measure_condition_string = ""

        if measure_conditions:
            for measure_condition in measure_conditions:
                measure_condition_string = MeasureCondition(measure_condition).output
                if measure_condition_string != "":
                    self.measure_condition_string += measure_condition_string
        self.measure_condition_string_excel = self.measure_condition_string.replace("<br />", "\n")

        self.measure_condition_array = [
            "Measure conditions",
            self.measure_condition_string
        ]

    def get_measure_excluded_geographical_areas(self):
        measure_excluded_geographical_areas = self.elem.findall(
            'measureExcludedGeographicalArea')
        self.measure_excluded_geographical_areas = []
        self.exclusion_string = ""

        if measure_excluded_geographical_areas:
            for measure_excluded_geographical_area in measure_excluded_geographical_areas:
                geographical_area_id = MeasureExcludedGeographicalArea(
                    measure_excluded_geographical_area).geographical_area_id
                if geographical_area_id is not None:
                    self.exclusion_string += geographical_area_id + ", "

        self.exclusion_string = self.exclusion_string.strip()
        self.exclusion_string = self.exclusion_string.strip(",")

        self.exclusion_string_array = [
            "Excluded countries",
            self.exclusion_string
        ]

    def get_footnotes(self):
        footnotes = self.elem.findall('footnoteAssociationMeasure')
        self.footnotes = []
        self.footnote_string = ""

        if footnotes:
            for footnote in footnotes:
                footnote_id = FootnoteAssociationMeasure(footnote).footnote
                if footnote_id != "":
                    self.footnote_string += footnote_id + ", "

        self.footnote_string = self.footnote_string.strip()
        self.footnote_string = self.footnote_string.strip(",")

        self.footnote_array = [
            "Associated footnotes",
            self.footnote_string
        ]
