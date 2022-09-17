import csv
from classes.master import Master
import classes.globals as g


class MeasureCondition(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.sid = Master.process_null_float(self.elem.find("sid"))
            self.condition_sequence_number = Master.process_null(
                self.elem.find("conditionSequenceNumber"))
            self.certificate_code = Master.process_null(
                self.elem.find("certificate/certificateCode"))
            self.certificate_type_code = Master.process_null(
                self.elem.find("certificate/certificateType/certificateTypeCode"))
            self.certificate = self.certificate_type_code + self.certificate_code
            self.action_code = Master.process_null(
                self.elem.find("measureAction/actionCode"))
            self.condition_code = Master.process_null(
                self.elem.find("measureConditionCode/conditionCode"))

            self.get_condition_code_description()
            self.get_action_code_description()

            self.output = ""
            if self.certificate == "":
                self.certificate = "n/a"
            self.output += "Certificate: " + self.certificate + ", "
            self.output += "Condition code: " + self.condition_code + " (" + self.condition_code_description + "), "
            self.output += "Action code: " + self.action_code + " (" + self.action_code_description + ")<br /><br />"
            
        else:
            self.output = ""

    def get_condition_code_description(self):
        self.condition_code_description = g.condition_code_dict[self.condition_code]

    def get_action_code_description(self):
        self.action_code_description = g.action_code_dict[self.action_code]

