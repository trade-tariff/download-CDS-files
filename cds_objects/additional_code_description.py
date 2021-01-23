from classes.master import Master
import csv


class AdditionalCodeDescription(Master):

    def __init__(self, md_file, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.md_file = md_file
        self.get_data()

    def get_data(self):
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.description = Master.process_null(self.elem.find("additionalCodeDescription/description"))
        self.tbl = [
               "Description start date", Master.format_date(self.validity_start_date),
               "Description", self.description,
               ]
        self.description_string = Master.format_date(self.validity_start_date) + "\n" + self.description + "\n"
