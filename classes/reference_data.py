import time
import random
import os
import sys
import requests
import traceback

from dotenv import load_dotenv

load_dotenv(".env")


class ReferenceDataHandler(object):
    def __init__(self, path, yield_response=False):
        self._url = os.getenv("OTT_HOST") + path
        self._headers = {"content-type": "application/json"}
        self._yield_response = yield_response

    def __enter__(self):
        return self.retry_with_backoff(self.do_fetch)

    def __exit__(self, _a, _b, _c):
        pass

    def instrument_response(self, response):
        if not response.status_code == 200:
            print(
                "URL: ",
                response.url,
            )
            print("Status: ", response.status_code)
            print("History: ", [r.url for r in response.history])
            print("Body: ", response.text)

    def do_fetch(self):
        response = requests.get(self._url, headers=self._headers, allow_redirects=True)

        self.instrument_response(response)

        response_json = response.json()

        if self._yield_response:
            return response_json
        else:
            return response_json["data"]

    def retry_with_backoff(self, callback, retries=6, backoff_in_seconds=1):
        for number_of_retries in range(1, retries + 1):
            try:
                return callback()
            except Exception:
                if number_of_retries == retries:
                    print("Failed to download reference data", self._url)
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_traceback)
                    sys.exit(1)

                sleep = backoff_in_seconds * 2**number_of_retries + random.uniform(
                    0, 1
                )
                time.sleep(sleep)


class GeographyList(object):
    class GeographicalAreas(dict):
        def __missing__(self, key):
            return f"Geographical area for {key} not found"

    def __init__(self):
        self.geography_dict = GeographyList.GeographicalAreas()
        self.geography_hjid_dict = GeographyList.GeographicalAreas()

    def load(self):
        with ReferenceDataHandler(
            "/api/v2/geographical_areas?filter[exclude_none]=true"
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


class QuotaOrderNumberList(object):
    def __init__(self):
        self.quota_order_number_dict = {}

    def load(self):
        with ReferenceDataHandler(
            "/api/v2/quota_order_numbers", yield_response=True
        ) as response:
            included = response["included"]

            def is_quota_definition(include):
                return include["type"] == "quota_definition"

            def is_measure(include):
                return include["type"] == "measure"

            all_quota_definitions = list(filter(is_quota_definition, included))
            all_measures = list(filter(is_measure, included))

            for quota_definition in all_quota_definitions:
                quota_definition_commodity_codes = set(())
                quota_definition_measures = []

                for measure in quota_definition["relationships"]["measures"]["data"]:
                    quota_definition_measures.append(measure["id"])

                def is_applicable_measure(include):
                    return include["id"] in quota_definition_measures

                applicable_measures = list(filter(is_applicable_measure, all_measures))

                for measure in applicable_measures:
                    quota_definition_commodity_codes.add(
                        measure["attributes"]["goods_nomenclature_item_id"]
                    )

                if applicable_measures:
                    self.quota_order_number_dict[
                        quota_definition["attributes"]["quota_order_number_id"]
                    ] = sorted(quota_definition_commodity_codes)


class MeasurementUnitList(object):
    def __init__(self):
        self.measurement_unit_dict = {
            "ASV": "% vol",
            "NAR": "item",
            "CCT": "ct/l",
            "CEN": "100 p/st",
            "CTM": "c/k",
            "DTN": "100 kg",
            "GFI": "gi F/S",
            "GRM": "g",
            "HLT": "hl",
            "HMT": "100 m",
            "KGM": "kg",
            "KLT": "1,000 l",
            "KMA": "kg met.am.",
            "KNI": "kg N",
            "KNS": "kg H2O2",
            "KPH": "kg KOH",
            "KPO": "kg K2O",
            "KPP": "kg P2O5",
            "KSD": "kg 90 % sdt",
            "KSH": "kg NaOH",
            "KUR": "kg U",
            "LPA": "l alc. 100%",
            "LTR": "l",
            "MIL": "1,000 items",
            "MTK": "m2",
            "MTQ": "m3",
            "MTR": "m",
            "MWH": "1,000 kWh",
            "NCL": "ce/el",
            "NPR": "pa",
            "TJO": "TJ",
            "TNE": "tonne",
        }
