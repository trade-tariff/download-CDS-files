import sys
from classes.master import Master
from cds_objects.additional_code_description import AdditionalCodeDescription
import classes.globals as g


class QuotaBalanceEvent(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.quota_balance_event_string = ""
        self.get_data()

    def get_data(self):
        self.new_balance = Master.process_null(self.elem.find("newBalance"))
        self.old_balance = Master.process_null(self.elem.find("oldBalance"))
        self.occurrence_timestamp = Master.format_date_ymd(self.elem.find("occurrenceTimestamp").text)
        self.quota_balance_event_string = str(self.occurrence_timestamp) + " - New: " + str(self.new_balance) + " : " + "Old: " + str(self.old_balance)
