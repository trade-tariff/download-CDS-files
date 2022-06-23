from classes.database import Database


class GeographyList(object):
    def __init__(self):
        print("Creating list of geographical areas")
        self.geography_list = []
        self.geography_dict = {}
        self.geography_hjid_dict = {}
        sql = """SELECT g.geographical_area_sid,
        g.parent_geographical_area_group_sid,
        geo1.geographical_area_id,
        geo1.description,
        g.geographical_code,
        g.validity_start_date,
        g.validity_end_date, g.hjid
        FROM geographical_area_descriptions geo1,
        geographical_areas g
        WHERE g.geographical_area_id::text = geo1.geographical_area_id::text AND (geo1.geographical_area_description_period_sid IN ( SELECT max(geo2.geographical_area_description_period_sid) AS max
        FROM geographical_area_descriptions geo2
        WHERE geo1.geographical_area_id::text = geo2.geographical_area_id::text))
        ORDER BY geo1.geographical_area_id;"""
        d = Database()
        rows = d.run_query(sql)
        for row in rows:
            hjid = int(row[7])
            geo = GeographicalArea(row[0], row[1], row[2], row[3], row[4], row[5], row[6], hjid)
            self.geography_list.append(geo)
            self.geography_dict[row[2]] = row[3]
            self.geography_hjid_dict[hjid] = row[2] + " - " + row[3]


class GeographicalArea(object):
    def __init__(self, geographical_area_sid, parent_geographical_area_group_sid, geographical_area_id, description, geographical_code, validity_start_date, validity_end_date, hjid):
        self.geographical_area_sid = geographical_area_sid
        self.parent_geographical_area_group_sid = parent_geographical_area_group_sid
        self.geographical_area_id = geographical_area_id
        self.description = description
        self.geographical_code = geographical_code
        self.validity_start_date = validity_start_date
        self.validity_end_date = validity_end_date
        self.hjid = hjid
