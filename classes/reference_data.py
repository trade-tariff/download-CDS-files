import os
import sys
import requests

from dotenv import load_dotenv

load_dotenv(".env")


class ReferenceDataHandler(object):
    def __init__(self, path):
        self._url = os.getenv("OTT_HOST") + path
        self._headers = {"content-type": "application/json"}

    def __enter__(self):
        try:
            response_json = requests.request(
                "GET", self._url, headers=self._headers
            ).json()

            return response_json["data"]
        except Exception:
            print("Failed to download reference data", self._url)
            sys.exit()

    def __exit__(self, _a, _b, _c):
        pass


class GeographyList(object):
    def __init__(self):
        self.geography_dict = {}
        self.geography_hjid_dict = {}

    def load(self):
        with ReferenceDataHandler(
            "/api/v2/geographical_areas?filter['exclude_none']=true"
        ) as geographical_areas:
            for geographical_area in geographical_areas:
                self.geography_dict[geographical_area["id"]] = geographical_area[
                    "attributes"
                ]["description"]

                self.geography_hjid_dict[
                    geographical_area["attributes"]["hjid"]
                ] = geographical_area["attributes"]["description"]

class MeasureTypeList(object):
    def __init__(self):
        self.measure_type_dict = {}

    def load(self):
        with ReferenceDataHandler("/api/v2/measure_types") as measure_types:
            for measure_type in measure_types:
                self.measure_type_dict[measure_type["id"]] = measure_type["attributes"][
                    "description"
                ]


class ActionCodeList(object):
    def __init__(self):
        self.action_code_dict = {}

    def load(self):
        with ReferenceDataHandler("/api/v2/measure_actions") as measure_actions:
            for measure_action in measure_actions:
                self.action_code_dict[measure_action["id"]] = measure_action[
                    "attributes"
                ]["description"]


class ConditionCodeList(object):
    def __init__(self):
        self.condition_code_dict = {}

    def load(self):
        with ReferenceDataHandler(
            "/api/v2/measure_condition_codes"
        ) as measure_condition_codes:
            for measure_condition_code in measure_condition_codes:
                self.condition_code_dict[
                    measure_condition_code["id"]
                ] = measure_condition_code["attributes"]["description"]
