from datetime import datetime
import os
import classes.globals as g


class Classification(object):
    def __init__(self, goods_nomenclature_sid, goods_nomenclature_item_id, productline_suffix, number_indents, leaf):
        self.goods_nomenclature_sid = goods_nomenclature_sid
        self.goods_nomenclature_item_id = goods_nomenclature_item_id
        self.productline_suffix = productline_suffix
        self.number_indents = int(number_indents)
        self.leaf = int(leaf)

    def extract_row(self):
        C = ','
        Q = '"'
        QC = '",'
        NL = "\n"
        s = str(self.goods_nomenclature_sid) + C
        s += Q + self.goods_nomenclature_item_id + QC
        s += Q + self.productline_suffix + QC
        s += str(self.number_indents) + C
        s += str(self.leaf) + NL
        return s
