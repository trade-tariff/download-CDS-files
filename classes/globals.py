import os
from dotenv import load_dotenv
from classes.geography_list import GeographyList
from classes.reference_data import ActionCodeList, MeasureTypeList, ConditionCodeList


# Get a list of all geo areas
obj = GeographyList()
geography_dict = obj.geography_dict
geography_hjid_dict = obj.geography_hjid_dict

# Get a list of all measure types
obj = MeasureTypeList()
measure_type_dict = obj.measure_type_dict

# Get a list of all action codes
obj = ActionCodeList()
action_code_dict = obj.action_code_dict

# Get a list of all condition codes
obj = ConditionCodeList()
condition_code_dict = obj.condition_code_dict

change_list = []
code_lists = []
definition_list = {}
