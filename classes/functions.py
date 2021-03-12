def parse_date(d):
    d2 = d[6:8] + "/" + d[4:6] + "/" + d[0:4]
    return (d2)

def get_nodes(path):
    pass

def xml_to_xlsx_filename(filename):
    parts = filename.split("T")
    part0 = parts[0]
    parts = part0.split("-")
    part1 = parts[1]
    excel_filename = "CDS updates " + part1[0:4] + "-" + part1[4:6] + "-" + part1[6:] + ".xlsx"
    return (excel_filename)
