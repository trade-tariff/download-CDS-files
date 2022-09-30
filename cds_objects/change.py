import classes.globals as g
import os
import sys


class Change(object):
    def __init__(self, sid, id, object_type, operation):
        self.sid = sid
        self.id = id
        self.object_type = object_type
        self.operation = operation


class MeasureChange(object):
    def __init__(self, sid, id, object_type, operation):
        self.sid = sid
        self.goods_nomenclature_item_id = id
        self.object_type = object_type
        self.operation = operation
        self.impacted_end_lines = []

        # print(self.sid)
        self.get_end_lines()
        
    def get_end_lines(self):
        try:
            code_key = "codes_" + self.goods_nomenclature_item_id[0]
            code_list = g.code_lists[code_key]
            found = False
            is_leaf = False
            index = -1
            number_indents = None

            for code in code_list:
                index += 1
                if (code.goods_nomenclature_item_id == self.goods_nomenclature_item_id) and (str(code.productline_suffix) == "80"):
                    found = True
                    if self.goods_nomenclature_item_id[-8:] == "00000000":
                        number_indents = -1
                    else:
                        number_indents = code.number_indents
        
                    if int(code.leaf) == 1:
                        is_leaf = True
                    break
            if is_leaf == False and found == True:
                for loop in range(index + 1, len(code_list) - 1):
                    next_code = code_list[loop]
                    if next_code.leaf == 1:
                        self.impacted_end_lines.append(next_code.goods_nomenclature_item_id)
                    
                    if (next_code.number_indents <= number_indents) or (next_code.goods_nomenclature_item_id[-8:]) == "00000000":
                        break
            
            if is_leaf == True or found == False:
                self.impacted_end_lines.append(self.goods_nomenclature_item_id)

        except:
            pass


class CommodityChange(object):
    def __init__(self, sid, id, productline_suffix, object_type, operation):
        self.sid = sid
        self.goods_nomenclature_item_id = id
        self.productline_suffix = productline_suffix
        self.object_type = object_type
        self.operation = operation
        self.impacted_end_lines = [self.goods_nomenclature_item_id]


class QuotaDefinitionChange(object):
    def __init__(self, sid, object_type, operation):
        self.sid = sid
        self.object_type = object_type
        self.operation = operation
        self.impacted_end_lines = []

        self.get_end_lines()
        
    def get_end_lines(self):
        # For each of these we need to get end lines
        
        try:
            my_list = g.definition_list["sid_" + str(self.sid)]
            for item in my_list:
                code_key = "codes_" + item[0]
                code_list = g.code_lists[code_key]
                found = False
                is_leaf = False
                index = -1
                number_indents = None

                for code in code_list:
                    index += 1
                    if (code.goods_nomenclature_item_id == item) and (str(code.productline_suffix) == "80"):
                        found = True
                        if item[-8:] == "00000000":
                            number_indents = -1
                        else:
                            number_indents = code.number_indents
            
                        if int(code.leaf) == 1:
                            is_leaf = True
                        break

                if is_leaf == False and found == True:
                    for loop in range(index + 1, len(code_list) - 1):
                        next_code = code_list[loop]
                        if next_code.leaf == 1:
                            self.impacted_end_lines.append(next_code.goods_nomenclature_item_id)
                        
                        if (next_code.number_indents <= number_indents) or (next_code.goods_nomenclature_item_id[-8:]) == "00000000":
                            break
                
                if is_leaf == True or found == False:
                    self.impacted_end_lines.append(item)
        except:
            pass