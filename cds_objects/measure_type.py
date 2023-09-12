from classes.master import Master
import classes.globals as g


class MeasureType(Master):
    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.get_data()
        self.write_data()

    def get_data(self):
        self.measure_type_id = Master.process_null(self.elem.find("measureTypeId"))
        self.validity_start_date = Master.process_null(
            self.elem.find("validityStartDate")
        )
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))

        self.measure_component_applicable_code = Master.process_null(
            self.elem.find("measureComponentApplicableCode")
        )
        self.measure_explosion_level = Master.process_null(
            self.elem.find("measureExplosionLevel")
        )
        self.order_number_capture_code = Master.process_null(
            self.elem.find("orderNumberCaptureCode")
        )
        self.origin_dest_code = Master.process_null(self.elem.find("originDestCode"))
        self.priority_code = Master.process_null(self.elem.find("priorityCode"))
        self.trade_movement_code = Master.process_null(
            self.elem.find("tradeMovementCode")
        )

        measure_type_description = self.elem.find("measureTypeDescription")
        if measure_type_description:
            self.description = Master.process_null(
                measure_type_description.find("description")
            )
        else:
            self.description = ""

    def write_data(self):
        wrap = g.excel.format_wrap if g.excel else None

        # Write the Excel
        self.worksheet.write(
            self.row_count,
            0,
            self.operation_text + " measure type",
            wrap,
        )
        self.worksheet.write(self.row_count, 1, self.measure_type_id, wrap)
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
        self.worksheet.write(self.row_count, 5, self.trade_movement_code, wrap)
        self.worksheet.write(self.row_count, 6, self.origin_dest_code, wrap)
        self.worksheet.write(
            self.row_count,
            7,
            self.measure_component_applicable_code,
            wrap,
        )
        self.worksheet.write(self.row_count, 8, self.order_number_capture_code, wrap)
        self.worksheet.write(self.row_count, 9, self.measure_explosion_level, wrap)
        self.worksheet.write(self.row_count, 10, self.priority_code, wrap)
