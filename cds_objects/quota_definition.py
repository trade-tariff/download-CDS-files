import sys
import xml.etree.ElementTree as ET

from classes.master import Master
from classes.database import Database
import classes.globals as g
from cds_objects.quota_balance_event import QuotaBalanceEvent
from cds_objects.change import QuotaDefinitionChange


class QuotaDefinition(Master):

    def __init__(self, elem, worksheet, row_count):
        Master.__init__(self, elem)
        self.elem = elem
        self.worksheet = worksheet
        self.row_count = row_count
        self.quota_balance_events = []
        self.quota_balance_event_string = ""
        self.comm_code_string = ""
        self.get_data()
        # self.write_data()

    def get_data(self):
        self.sid = Master.process_null(self.elem.find("sid"))
        self.critical_state = Master.process_null(self.elem.find("criticalState"))
        self.critical_threshold = Master.process_null(self.elem.find("criticalThreshold"))
        self.initial_volume = Master.process_null(self.elem.find("initialVolume"))
        self.volume = Master.process_null(self.elem.find("volume"))
        self.maximum_precision = Master.process_null(self.elem.find("maximumPrecision"))
        self.quota_order_number_id = Master.process_null(self.elem.find("quotaOrderNumber/quotaOrderNumberId"))
        self.quota_order_number_sid = Master.process_null(self.elem.find("quotaOrderNumber/sid"))
        self.validity_start_date = Master.process_null(self.elem.find("validityStartDate"))
        self.validity_end_date = Master.process_null(self.elem.find("validityEndDate"))
        self.get_balance_events()
        self.get_sample_comm_codes()

        change = QuotaDefinitionChange(self.sid, "Quota definition", self.operation)
        g.change_list.append(change)

    def get_sample_comm_codes(self):
        sql = "select distinct(goods_nomenclature_item_id) from measures where ordernumber = '" + self.quota_order_number_id + "' order by 1 limit 5"
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            self.comm_code_string += row[0] + ", "

        self.comm_code_string = self.comm_code_string.strip()
        self.comm_code_string = self.comm_code_string.strip(",")

    def write_data(self):
        # Write the Excel
        self.worksheet.write(self.row_count, 0, self.operation_text + " definition", g.excel.format_wrap)
        self.worksheet.write(self.row_count, 1, self.quota_order_number_id, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 2, self.quota_balance_event_string, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 3, self.comm_code_string, g.excel.format_force_text)
        self.worksheet.write(self.row_count, 4, self.sid, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 5, self.critical_state, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 6, self.critical_threshold, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 7, self.initial_volume, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 8, self.volume, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 9, self.maximum_precision, g.excel.format_wrap)
        self.worksheet.write(self.row_count, 10, Master.format_date(self.validity_start_date), g.excel.format_wrap)
        self.worksheet.write(self.row_count, 11, Master.format_date(self.validity_end_date), g.excel.format_wrap)

    def get_balance_events(self):
        self.quota_balance_event_string = ""
        quota_balance_events = self.elem.findall('quotaBalanceEvent')
        quota_balance_events_list = []
        for quota_balance_event in quota_balance_events:
            obj = QuotaBalanceEvent(quota_balance_event)
            quota_balance_events_list.append(obj)

        quota_balance_events_list = sorted(quota_balance_events_list, key=lambda x: x.occurrence_timestamp)
        # if self.quota_order_number_id == "052105":
        #     for quota_balance_event in quota_balance_events_list:
        #         print(quota_balance_event.occurrence_timestamp)

        if quota_balance_events_list:
            quota_balance_event_count = len(quota_balance_events_list)
            quota_balance_event = quota_balance_events_list[quota_balance_event_count - 1]
            self.quota_balance_event_string = quota_balance_event.quota_balance_event_string + "\n"
            self.quota_balance_event_string = self.quota_balance_event_string.strip("\n")
