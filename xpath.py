import glob
import os
import sys
from dotenv import load_dotenv
from classes.xpath_query import XpathQuery
from classes.xpath_markdown import XpathMarkdown


def cater_for_shortcuts(query_class):
    if query_class in ("m", "measures"):
        query_class = "measure"
    if query_class in ("c", "commodities"):
        query_class = "commodity"
    if query_class in ("mt", "measure_types"):
        query_class = "measure_type"
    return query_class

if len(sys.argv) < 3:
    print("Provide class and instance")
    sys.exit()
else:
    query_class = sys.argv[1]
    query_id = sys.argv[2]

query_class = cater_for_shortcuts(query_class)

# query_class = "commodity"
# query_id = "2933199070"

# query_class = "measure"
# query_id = "20138292"

load_dotenv('.env')
folder = os.getenv('DIT_DATA_FOLDER')
# folder = "/Users/mattlavis/sites and projects/1. Online Tariff/tariff data/DIT/"
files = glob.glob(folder + '/*.xml')
files = sorted(files)
records = []
for filename in files:
    xpq = XpathQuery(filename, query_class, query_id)
    ret = xpq.run_query()
    records += ret

a = 1
xpm = XpathMarkdown(records, query_class, query_id)
xpm.write_markdown()
