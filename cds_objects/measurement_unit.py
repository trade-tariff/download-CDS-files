from classes.master import Master
import classes.globals as g


class MeasurementUnit(Master):
    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.get_data()
        self.write_data()

    def get_data(self):
        self.measurement_unit_code = Master.process_null(
            self.elem.find("measurementUnitCode")
        )
        self.validity_start_date = Master.process_null(
            self.elem.find("validityStartDate")
        )
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        measurement_unit_description = self.elem.find("measurementUnitDescription")
        if measurement_unit_description:
            self.description = Master.process_null(
                measurement_unit_description.find("description")
            )
        else:
            self.description = ""

    def write_data(self):
        wrap = g.excel.format_wrap if g.excel else None

        self.worksheet.write(
            self.row_count,
            0,
            self.operation_text + " measurement unit code",
            wrap,
        )
        self.worksheet.write(self.row_count, 1, self.measurement_unit_code, wrap)
        self.worksheet.write(
            self.row_count,
            2,
            Master.format_date(self.validity_start_date),
            wrap,
        )
        self.worksheet.write(
            self.row_count,
            3,
            Master.format_date(self.validity_end_date),
            wrap,
        )
        self.worksheet.write(self.row_count, 4, self.description, wrap)
