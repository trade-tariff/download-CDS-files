from classes.master import Master
import csv


class GeographicalAreaMembership(Master):

    def __init__(self, md_file, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.md_file = md_file
        self.membership_string = ""
        self.current_membership_string = ""
        self.get_data()

    def get_data(self):
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.hjid_of_member = Master.process_null(self.elem.find("geographicalAreaGroupSid"))
        self.tbl = [
               "Membership start date", Master.format_date(self.validity_start_date),
               "HJID", self.hjid_of_member,
               ]
        if self.validity_end_date == "":
            self.membership_string = Master.format_date(self.validity_start_date) + " : " + self.hjid_of_member + "\n"
            self.current_membership_string = Master.format_date(self.validity_start_date) + " : " + self.hjid_of_member + "\n"
        else:
            self.membership_string = Master.format_date(self.validity_start_date) + " to " + Master.format_date(self.validity_end_date) + " : " + self.hjid_of_member + "\n"

