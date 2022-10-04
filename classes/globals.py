from classes.reference_data import (
    ActionCodeList,
    MeasureTypeList,
    ConditionCodeList,
    GeographyList,
    QuotaOrderNumberList,
)

# Get a list of all geographical areas descriptions by id and hjid
list = GeographyList()
list.load()

geography_dict = list.geography_dict
geography_hjid_dict = list.geography_hjid_dict

# Get a list of all measure type descriptions by measure type id
list = MeasureTypeList()
list.load()

measure_type_dict = list.measure_type_dict

# Get a list of all action codes
list = ActionCodeList()
list.load()

action_code_dict = list.action_code_dict

# Get a list of all condition codes
list = ConditionCodeList()
list.load()

condition_code_dict = list.condition_code_dict

# Get a list of all condition codes
list = QuotaOrderNumberList()
list.load()

quota_order_number_dict = list.quota_order_number_dict

change_list = []
code_lists = []
definition_list = {}
