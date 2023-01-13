from classes.master import Master


class BaseRegulation(Master):
    def __init__(self, xml_file, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.xml_file = xml_file
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.get_data()
        self.write_data()

    def get_data(self):
        self.base_regulation_id = Master.process_null(
            self.elem.find("baseRegulationId")
        )
        self.information_text = Master.process_null(self.elem.find("informationText"))
        self.validity_start_date = Master.process_null(
            self.elem.find("validityStartDate")
        )
        self.regulation_group_id = Master.process_null(
            self.elem.find("regulationGroup/regulationGroupId")
        )
        self.regulation_role_type_id = Master.process_null(
            self.elem.find("regulationRoleType/regulationRoleTypeId")
        )

    def write_data(self):
        # Write the Excel
        self.worksheet.write(
            self.row_count,
            0,
            self.operation_text + " base regulation",
            self.xml_file.excel.format_wrap,
        )
        self.worksheet.write(
            self.row_count, 1, self.base_regulation_id, self.xml_file.excel.format_wrap
        )
        self.worksheet.write(
            self.row_count, 2, self.information_text, self.xml_file.excel.format_wrap
        )
        self.worksheet.write(
            self.row_count,
            3,
            Master.format_date(self.validity_start_date),
            self.xml_file.excel.format_wrap,
        )
        self.worksheet.write(
            self.row_count, 4, self.regulation_group_id, self.xml_file.excel.format_wrap
        )
        self.worksheet.write(
            self.row_count,
            5,
            self.regulation_role_type_id,
            self.xml_file.excel.format_wrap,
        )
