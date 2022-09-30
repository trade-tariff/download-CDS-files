from classes.master import Master
import csv


class MeasureComponent(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.duty_amount = Master.process_null_float(self.elem.find("dutyAmount"))
            self.duty_expression_id = Master.process_null(self.elem.find("dutyExpression/dutyExpressionId"))
            self.measurement_unit_code = Master.process_null(self.elem.find("measurementUnit/measurementUnitCode"))
            self.measurement_unit_qualifier_code = Master.process_null(self.elem.find("measurementUnitQualifier/measurementUnitQualifierCode"))
            self.monetary_unit_code = Master.process_null(self.elem.find("monetaryUnit/monetaryUnitCode"))
            self.get_duty_string()
        else:
            self.duty_string = None

    def get_duty_string(self):
        self.duty_string = ""

        if self.duty_expression_id == "01":
            if self.monetary_unit_code == "":
                self.duty_string += "{0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "{0:1.4f}".format(
                    self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + \
                        self.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + self.get_qualifier()

        elif self.duty_expression_id in ("04", "19", "20"):
            if self.monetary_unit_code == "":
                self.duty_string += "+ {0:1.4f}".format(self.duty_amount) + "%"
            else:
                self.duty_string += "+ {0:1.4f}".format(
                    self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + \
                        self.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + self.get_qualifier()

        elif self.duty_expression_id == "15":
            if self.monetary_unit_code == "":
                self.duty_string += "MIN {0:1.4f}".format(
                    self.duty_amount) + "%"
            else:
                self.duty_string += "MIN {0:1.4f}".format(
                    self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + \
                        self.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + self.get_qualifier()

        elif self.duty_expression_id in ("17", "35"):  # MAX
            if self.monetary_unit_code == "":
                self.duty_string += "MAX {0:1.4f}".format(
                    self.duty_amount) + "%"
            else:
                self.duty_string += "MAX {0:1.4f}".format(
                    self.duty_amount) + " " + self.monetary_unit_code
                if self.measurement_unit_code != "":
                    self.duty_string += " / " + \
                        self.get_measurement_unit(self.measurement_unit_code)
                    if self.measurement_unit_qualifier_code != "":
                        self.duty_string += " / " + self.get_qualifier()

        elif self.duty_expression_id in ("12"):
            self.duty_string += " + AC"

        elif self.duty_expression_id in ("14"):
            self.duty_string += " + ACR"

        elif self.duty_expression_id in ("21"):
            self.duty_string += " + SD"

        elif self.duty_expression_id in ("25"):
            self.duty_string += " + SDR"

        elif self.duty_expression_id in ("27"):
            self.duty_string += " + FD"

        elif self.duty_expression_id in ("29"):
            self.duty_string += " + FDR"

        elif self.duty_expression_id in ("99"):
            self.duty_string += self.measurement_unit_code

        else:
            print("Unexpected duty expression found", self.duty_expression_id)

        self.duty_string = self.duty_string.replace("  ", " ")

    def get_measurement_unit(self, s):
        if s == "ASV":
            return "% vol"
        if s == "NAR":
            return "item"
        elif s == "CCT":
            return "ct/l"
        elif s == "CEN":
            return "100 p/st"
        elif s == "CTM":
            return "c/k"
        elif s == "DTN":
            return "100 kg"
        elif s == "GFI":
            return "gi F/S"
        elif s == "GRM":
            return "g"
        elif s == "HLT":
            return "hl"  # 2209009100
        elif s == "HMT":
            return "100 m"  # 3706909900
        elif s == "KGM":
            return "kg"
        elif s == "KLT":
            return "1,000 l"
        elif s == "KMA":
            return "kg met.am."
        elif s == "KNI":
            return "kg N"
        elif s == "KNS":
            return "kg H2O2"
        elif s == "KPH":
            return "kg KOH"
        elif s == "KPO":
            return "kg K2O"
        elif s == "KPP":
            return "kg P2O5"
        elif s == "KSD":
            return "kg 90 % sdt"
        elif s == "KSH":
            return "kg NaOH"
        elif s == "KUR":
            return "kg U"
        elif s == "LPA":
            return "l alc. 100%"
        elif s == "LTR":
            return "l"
        elif s == "MIL":
            return "1,000 items"
        elif s == "MTK":
            return "m2"
        elif s == "MTQ":
            return "m3"
        elif s == "MTR":
            return "m"
        elif s == "MWH":
            return "1,000 kWh"
        elif s == "NCL":
            return "ce/el"
        elif s == "NPR":
            return "pa"
        elif s == "TJO":
            return "TJ"
        elif s == "TNE":
            return "tonne"  # 1005900020
            # return "1000 kg" # 1005900020
        else:
            return s

    def get_qualifier(self):
        sQualDesc = ""
        s = self.measurement_unit_qualifier_code
        if s == "A":
            sQualDesc = "tot alc"  # Total alcohol
        elif s == "C":
            sQualDesc = "1 000"  # Total alcohol
        elif s == "E":
            sQualDesc = "net drained wt"  # net of drained weight
        elif s == "G":
            sQualDesc = "gross"  # Gross
        elif s == "I":
            sQualDesc = "biodiesel"  # Gross
        elif s == "M":
            sQualDesc = "net dry"  # net of dry matter
        elif s == "P":
            sQualDesc = "lactic matter"  # of lactic matter
        elif s == "R":
            sQualDesc = "std qual"  # of the standard quality
        elif s == "S":
            sQualDesc = " raw sugar"
        elif s == "T":
            sQualDesc = "dry lactic matter"  # of dry lactic matter
        elif s == "X":
            sQualDesc = " hl"  # Hectolitre
        elif s == "Z":
            sQualDesc = "% sacchar."  # per 1% by weight of sucrose
        return sQualDesc
