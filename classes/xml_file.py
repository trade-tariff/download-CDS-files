import os
import xml.etree.ElementTree as ET
from classes.ses_mailer import SesMailer

from cds_objects.measure_type import MeasureType
from cds_objects.measurement_unit import MeasurementUnit
from cds_objects.footnote_type import FootnoteType
from cds_objects.footnote import Footnote
from cds_objects.additional_code import AdditionalCode
from cds_objects.certificate import Certificate
from cds_objects.measure import Measure
from cds_objects.goods_nomenclature import GoodsNomenclature
from cds_objects.quota_order_number import QuotaOrderNumber
from cds_objects.quota_definition import QuotaDefinition
from cds_objects.geographical_area import GeographicalArea
from cds_objects.base_regulation import BaseRegulation
from classes.excel import Excel


class XmlFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.join(os.getcwd(), "resources")
        self.path = os.path.join(self.path, "xml")
        self.file_path = os.path.join(self.path, self.filename)
        self.excel = Excel(self.path, self.filename)
        self.excel.create_excel()

    def parse_xml(self):
        print("Creating file", os.path.basename(self.excel.excel_filename))

        tree = ET.parse(self.file_path)
        self.root = tree.getroot()

        self.get_results_info()
        self.get_measure_types()
        self.get_measurement_units()
        self.get_footnote_types()
        self.get_footnotes()
        self.get_additional_codes()
        self.get_certificates()
        self.get_measures()
        self.get_commodities()
        self.get_quota_order_numbers()
        self.get_quota_definitions()
        self.get_geographical_areas()
        self.get_base_regulations()

        self.excel.close_excel()

        self.mail_extract()

    def mail_extract(self):
        if self.should_send_mail():
            SesMailer.build_for_cds_upload(self.excel).send()

    def get_measure_types(self):
        row_count = 0
        measure_types = self.root.find(".//findMeasureTypeByDatesResponse")
        if measure_types:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Measure types")
            data = (
                "Action",
                "Measure type ID",
                "Start date",
                "End date",
                "Description",
                "Trade movement code",
                "Origin dest code",
                "Measure component applicable code",
                "Order number capture code",
                "Measure explosion level",
                "Priority code",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 10, 20)
            worksheet.set_column(4, 4, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            measure_types = measure_types.findall("MeasureType")
            for measure_type in measure_types:
                row_count += 1
                MeasureType(measure_type, worksheet, row_count)

    def get_measurement_units(self):
        row_count = 0
        measurement_units = self.root.find(".//findMeasurementUnitByDatesResponse")
        if measurement_units:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Measurement units")
            data = (
                "Action",
                "Measurement unit code",
                "Start date",
                "End date",
                "Description",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 3, 30)
            worksheet.set_column(4, 4, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            measurement_units = measurement_units.findall("MeasurementUnit")
            for measurement_unit in measurement_units:
                row_count += 1
                MeasurementUnit(measurement_unit, worksheet, row_count)

    def get_footnote_types(self):
        row_count = 0
        footnote_types = self.root.find(".//findFootnoteTypeByDatesResponse")
        if footnote_types:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Footnote types")
            data = (
                "Action",
                "Footnote type ID",
                "Application code",
                "Start date",
                "End date",
                "Description",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 20)
            worksheet.set_column(5, 5, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            footnote_types = footnote_types.findall("FootnoteType")
            for footnote_type in footnote_types:
                row_count += 1
                FootnoteType(self, footnote_type, worksheet, row_count)

        return row_count

    def get_footnotes(self):
        row_count = 0
        footnotes = self.root.find(".//findFootnoteByDatesResponse")
        if footnotes:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Footnotes")
            data = (
                "Action",
                "Combined",
                "Footnote type ID",
                "Footnote ID",
                "Start date",
                "End date",
                "Description",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 5, 20)
            worksheet.set_column(6, 6, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            footnotes = footnotes.findall("Footnote")
            for footnote in footnotes:
                row_count += 1
                Footnote(self, footnote, worksheet, row_count)

        return row_count

    def get_additional_codes(self):
        row_count = 0
        additional_codes = self.root.find(".//findAdditionalCodeByDatesResponse")
        if additional_codes:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Additional codes")
            data = (
                "Action",
                "Additional code type",
                "Additional code ID",
                "Start date",
                "End date",
                "Description",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 20)
            worksheet.set_column(5, 5, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            additional_codes = additional_codes.findall("AdditionalCode")
            for additional_code in additional_codes:
                row_count += 1
                AdditionalCode(self, additional_code, worksheet, row_count)

        return row_count

    def get_certificates(self):
        row_count = 0
        certificates = self.root.find(".//findCertificateByDatesResponse")
        if certificates:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Certificates")
            data = (
                "Action",
                "Certificate code type",
                "Certificate code",
                "Start date",
                "End date",
                "Description",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 4, 20)
            worksheet.set_column(5, 5, 50)
            worksheet.freeze_panes(1, 0)

            # Get data
            certificates = certificates.findall("Certificate")
            for certificate in certificates:
                row_count += 1
                Certificate(self, certificate, worksheet, row_count)

        return row_count

    def get_base_regulations(self):
        row_count = 0
        base_regulations = self.root.find(".//findBaseRegulationByDatesResponseHistory")
        if base_regulations:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Base regulations")
            data = (
                "Action",
                "Regulation ID",
                "Information text",
                "Start date",
                "Regulation group",
                "Regulation role type",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(0, 1, 20)
            worksheet.set_column(2, 2, 40)
            worksheet.set_column(3, 5, 20)
            worksheet.freeze_panes(1, 0)

            # Get data
            base_regulations = base_regulations.findall("BaseRegulation")
            for base_regulation in base_regulations:
                row_count += 1
                BaseRegulation(self, base_regulation, worksheet, row_count)

        return row_count

    def get_measures(self):
        row_count = 0
        measures = self.root.find(".//findMeasureByDatesResponseHistory")
        if measures:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Measures")
            data = (
                "Action",
                "Commodity code",
                "Additional code",
                "Measure type",
                "Geographical area",
                "Quota order number",
                "Start date",
                "End date",
                "Duty",
                "Excluded areas",
                "Footnotes",
                "Conditions",
                "SID",
            )
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 7, 20)
            worksheet.set_column(3, 4, 40)
            worksheet.set_column(8, 8, 40)
            worksheet.set_column(9, 10, 30)
            worksheet.set_column(11, 11, 100)
            worksheet.set_column(12, 12, 30)
            worksheet.freeze_panes(1, 0)

            # Get data
            measures = measures.findall("Measure")
            measure_objects = []
            for measure in measures:
                row_count += 1
                measure_objects.append(Measure(self, measure, worksheet, row_count))

            measure_objects = sorted(
                measure_objects, key=lambda x: x.measure_type_id, reverse=False
            )
            measure_objects = sorted(
                measure_objects,
                key=lambda x: x.goods_nomenclature_item_id,
                reverse=False,
            )
            measure_objects = sorted(
                measure_objects, key=lambda x: x.operation_text, reverse=False
            )

            row_count = 0
            for measure in measure_objects:
                row_count += 1
                measure.row_count = row_count
                measure.write_data()

            range = "A1:M" + str(row_count)
            worksheet.autofilter(range)

        return row_count

    def get_commodities(self):
        row_count = 0
        commodities = self.root.find(".//findGoodsNomenclatureByDatesResponse")
        if commodities:
            commodities = commodities.findall("GoodsNomenclature")
            if commodities:
                # Write Excel column headers
                worksheet = self.excel.workbook.add_worksheet("Commodities")
                data = (
                    "Action",
                    "Commodity code",
                    "Product line suffix",
                    "Description",
                    "Start date",
                    "End date",
                    "Statistical indicator",
                    "SID",
                )
                worksheet.write_row("A1", data, self.excel.format_bold)
                worksheet.set_column(0, 0, 30)
                worksheet.set_column(1, 7, 20)
                worksheet.set_column(3, 3, 50)
                worksheet.freeze_panes(1, 0)

                commodity_objects = []
                for commodity in commodities:
                    row_count += 1
                    commodity_objects.append(
                        GoodsNomenclature(self, commodity, worksheet, row_count)
                    )

                commodity_objects = sorted(
                    commodity_objects,
                    key=lambda x: x.product_line_suffix,
                    reverse=False,
                )
                commodity_objects = sorted(
                    commodity_objects,
                    key=lambda x: x.goods_nomenclature_item_id,
                    reverse=False,
                )
                commodity_objects = sorted(
                    commodity_objects, key=lambda x: x.operation_text, reverse=False
                )

                row_count = 0
                for commodity in commodity_objects:
                    if commodity.description_string != "":
                        row_count += 1
                        commodity.row_count = row_count
                        commodity.write_data()

                range = "A1:H" + str(row_count)
                worksheet.autofilter(range)

        return row_count

    def get_quota_order_numbers(self):
        row_count = 0
        quotas = self.root.find(".//findQuotaOrderNumberByDatesResponseHistory")
        if quotas:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Quota order numbers")
            data = ("Action", "SID", "Order number", "Start date", "End date")
            worksheet.write_row("A1", data, self.excel.format_bold)
            worksheet.set_column(0, 0, 40)
            worksheet.set_column(1, 4, 20)
            worksheet.freeze_panes(1, 0)

            # Get data
            quotas = quotas.findall("QuotaOrderNumber")
            for quota in quotas:
                row_count += 1
                QuotaOrderNumber(self, quota, worksheet, row_count)

        return row_count

    def get_geographical_areas(self):
        row_count = 0
        geographical_areas = self.root.find(".//findGeographicalAreaByDatesResponse")
        if geographical_areas:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Geographical areas")
            data = (
                "Action",
                "Geographical area ID",
                "SID",
                "Start date",
                "End date",
                "Description(s)",
                "Current memberships",
                "All memberships",
                "Parent group SID",
            )
            widths = [30, 20, 15, 15, 20, 50, 70, 70, 15]
            worksheet.write_row("A1", data, self.excel.format_bold)
            for i in range(0, len(widths)):
                worksheet.set_column(i, i, widths[i])
            worksheet.freeze_panes(1, 0)

            # Get data
            geographical_areas = geographical_areas.findall("GeographicalArea")
            geographical_area_objects = []
            for geographical_area in geographical_areas:
                row_count += 1
                geographical_area_object = GeographicalArea(
                    self, geographical_area, worksheet, row_count
                )
                geographical_area_objects.append(geographical_area_object)

            geographical_area_objects = sorted(
                geographical_area_objects,
                key=lambda x: x.geographical_area_id,
                reverse=False,
            )

            row_count = 1
            for geographical_area_object in geographical_area_objects:
                geographical_area_object.row_count = row_count
                geographical_area_object.write_data()
                row_count += 1

        return row_count

    def get_quota_definitions(self):
        row_count = 0
        quota_definitions = self.root.find(
            ".//findQuotaDefinitionByDatesResponseHistory"
        )
        if quota_definitions:
            # Write Excel column headers
            worksheet = self.excel.workbook.add_worksheet("Quota definitions")
            worksheet.write(
                "A1",
                "Please be careful when checking quota balances - each file may contains multiple updates on the same quota definition",  # noqa: E501
                self.excel.format_bold,
            )

            data = (
                "Action",
                "Quota order number",
                "Balance updates",
                "Sample commodities",
                "SID",
                "Critical state",
                "Critical threshold",
                "Initial volume",
                "Volume",
                "Maximum precision",
                "Start date",
                "End date",
            )
            widths = [30, 20, 50, 70, 20, 20, 20, 20, 20, 20, 20, 20]
            worksheet.write_row("A3", data, self.excel.format_bold)
            for i in range(0, len(widths)):
                worksheet.set_column(i, i, widths[i])
            worksheet.freeze_panes(1, 0)

            # Get data
            quota_definitions = quota_definitions.findall("QuotaDefinition")
            quota_definition_objects = []
            for quota_definition in quota_definitions:
                row_count += 1
                quota_definition_object = QuotaDefinition(
                    self, quota_definition, worksheet, row_count
                )
                quota_definition_objects.append(quota_definition_object)

            quota_definition_objects = sorted(
                quota_definition_objects,
                key=lambda x: x.quota_order_number_id,
                reverse=False,
            )

            row_count = 3
            for quota_definition_object in quota_definition_objects:
                quota_definition_object.row_count = row_count
                quota_definition_object.write_data()
                row_count += 1

        return row_count

    def get_results_info(self):
        results_info = self.root.find("ResultsInfo")
        self.total_records = int(results_info.find("totalRecords").text)
        self.execution_date = results_info.find("executionDate").text

    def should_send_mail(self):
        return int(os.getenv("SEND_MAIL", "0")) == 1
