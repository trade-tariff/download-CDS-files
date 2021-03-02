import csv
from classes.master import Master
import classes.globals as g


class GeographicalAreaMembership(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.membership_string = ""
        self.current_membership_string = ""
        self.get_data()

    def get_data(self):
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.hjid_of_member = int(Master.process_null(self.elem.find("geographicalAreaGroupSid")))
        self.get_member_description()
        self.tbl = [
               "Membership start date", Master.format_date(self.validity_start_date),
               "HJID", self.hjid_of_member,
               ]
        if self.validity_end_date == "":
            self.membership_string = Master.format_date(self.validity_start_date) + " : " + self.member_description + "\n"
            self.current_membership_string = Master.format_date(self.validity_start_date) + " : " + self.member_description + "\n"
        else:
            self.membership_string = Master.format_date(self.validity_start_date) + " to " + Master.format_date(self.validity_end_date) + " : " + self.member_description + "\n"

    def get_member_description(self):
        self.member_description = g.geography_hjid_dict[self.hjid_of_member]
