import glob
import os
import sys
from dotenv import load_dotenv
from classes.xpath_query import XpathQuery
from classes.xpath_markdown import XpathMarkdown


def cater_for_shortcuts(query_class):
    if query_class in ("m", "measures"):
        query_class = "measure"
    elif query_class in ("c", "commodities"):
        query_class = "commodity"
    elif query_class in ("mt", "measure_types"):
        query_class = "measure_type"
    elif query_class in ("geo", "geography", "geographical_areas", "g", "geographical_area_id"):
        query_class = "geographical_area"
    elif query_class in ("cm", "mc", "measure_commodity"):
        query_class = "commodity_measure"
    return query_class

def cleanse_scope(scope):
    if scope in ("eu", "xi"):
        scope = "tgb"
    elif scope in ("uk"):
        scope = "dit"
    elif scope in ("cds"):
        scope = "cds"
    return scope

if len(sys.argv) < 4:
    print("Provide class, instance and scope")
    sys.exit()
else:
    query_class = sys.argv[1]
    query_id = sys.argv[2]
    scope = sys.argv[3]

query_class = cater_for_shortcuts(query_class)
scope = cleanse_scope(scope)

load_dotenv('.env')

if scope == "dit":
    folder = os.getenv('DIT_DATA_FOLDER')
elif scope == "tgb":
    folder = os.getenv('TGB_DATA_FOLDER')
else:
    folder = os.getenv('CDS_DATA_FOLDER')

files = glob.glob(folder + '/*.xml')
files = sorted(files)
records = []
for filename in files:
    xpq = XpathQuery(filename, query_class, query_id, scope)
    ret = xpq.run_query()
    records += ret

a = 1
xpm = XpathMarkdown(records, query_class, query_id, scope)
xpm.write_markdown()
