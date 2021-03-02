import sys
from classes.master import Master
from classes.database import Database
import classes.globals as g
from cds_objects.geographical_area_description import GeographicalAreaDescription
from cds_objects.geographical_area_membership import GeographicalAreaMembership


class GeographicalArea(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.descriptions = []
        self.description_string = ""
        self.memberships = []
        self.membership_string = ""
        self.current_membership_string = ""
        self.get_data()

    def get_data(self):
        self.sid = Master.process_null(self.elem.find("sid"))
        self.geographical_area_id = Master.process_null(self.elem.find("geographicalAreaId"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.parent_geographical_area_group_sid = Master.process_null(self.elem.find("parentGeographicalAreaGroupSid"))

        self.get_descriptions()
        self.get_members()

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " geographical area", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.geographical_area_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.sid, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 4, Master.format_date(self.validity_end_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.description_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, self.current_membership_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 7, self.membership_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 8, self.parent_geographical_area_group_sid, g.excel.format_wrap)

    def get_descriptions(self):
        geographical_area_descriptions = self.elem.findall('geographicalAreaDescriptionPeriod')
        if geographical_area_descriptions:
            for geographical_area_description in geographical_area_descriptions:
                obj = GeographicalAreaDescription(geographical_area_description)
                self.descriptions += obj.tbl
                self.description_string += obj.description_string
                
    def get_members(self):
        geographical_area_memberships = self.elem.findall('geographicalAreaMembership')
        if geographical_area_memberships:
            for geographical_area_membership in geographical_area_memberships:
                obj = GeographicalAreaMembership(geographical_area_membership)
                self.memberships += obj.tbl
                self.membership_string += obj.membership_string
                self.current_membership_string += obj.current_membership_string
                
