from classes.master import Master
import csv


class FootnoteAssociationMeasure(Master):

    def __init__(self, elem):
        Master.__init__(self, elem)
        self.elem = elem
        self.get_data()

    def get_data(self):
        if self.operation != "D":
            self.footnote_id = Master.process_null(self.elem.find("footnote/footnoteId"))
            self.footnote_type_id = Master.process_null(self.elem.find("footnote/footnoteType/footnoteTypeId"))
        else:
            self.footnote_id = ""
            self.footnote_type_id = ""

        self.footnote = self.footnote_type_id + self.footnote_id
