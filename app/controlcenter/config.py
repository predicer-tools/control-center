"""Configs and Constants for retrieving data from the Danish Data Lake Portal."""
import os
from influxdb_client import WritePrecision

TOKENFILE = "tokens.toml"
ORG = "ELEXIA"
INFLUXDB_URL = "http://localhost:8086"
URLS = {"live_frequency": "https://api.centerdenmark.com/api/v1/dataset/472ed84f-5378-4b12-8401-700e3451e3c3/query",
        "weather": "https://api.centerdenmark.com/api/v1/dataset/9224b1fe-d45f-4150-b326-5d51fd2b72cd/query",
        "electricity_cons": "https://api.centerdenmark.com/api/v1/dataset/89efeff5-f96d-43c5-96d6-c3f6aeb22007/query",
        "heat_cons": "https://api.centerdenmark.com/api/v1/dataset/1c16f324-235f-473b-84fd-8c6f69b38cb5/query",
        "build_to_weath_map": "https://api.centerdenmark.com/api/v1/dataset/106cf0f7-b39d-4daf-a457-488956fa61b0/query"}
BUCKETS = {"live_frequency": "Denmark-LiveFrequencyDK2V.1",
           "weather": "Denmark-Weather",
           "electricity_cons": "Denmark-ElectricityConsumption",
           "heat_cons": "Denmark-HeatConsumption",
           "build_to_weath_map": "Denmark-BuildingToWeatherMapping"}
MEASUREMENTS = {"live_frequency": "Frequency",
                "weather": "Weather",
                "electricity_cons": "ElectricityConsumption",
                "heat_cons": "HeatConsumption",
                "build_to_weath_map": "Mapping"}
MEASUREMENTS_BY_BUCKETS = {"Denmark-LiveFrequencyDK2V.1": "Frequency",
                           "Denmark-Weather": "Weather",
                           "Denmark-ElectricityConsumption": "ElectricityConsumption",
                           "Denmark-HeatConsumption": "HeatConsumption",
                           "Denmark-BuildingToWeatherMapping": "Mapping"}
TAGS = {"live_frequency": [],
        "weather": ["station_id"],
        "electricity_cons": ["cluster_id"],
        "heat_cons": ["cluster_id"],
        "build_to_weath_map": ["cluster_id"]}
FIELDS = {"live_frequency": ["value"],
          "weather": [
                  "wind_speed_past1h",
                  "temp_mean_past1h",
                  "wind_dir_past1h",
                  "humidity_past1h",
                  "radia_glob_past1h"
          ],
          "electricity_cons": [
                  "active_power_consumption"
          ],
          "heat_cons": [
                  "heating_consumption",
                  "forward_temperature",
                  "return_temperature",
                  "volume_consumption",
                  "flow_rate"
          ],
          "build_to_weath_map": ["station_id"]}
TIME = {"live_frequency": "timestamp",
        "weather": "timestamp",
        "electricity_cons": "timestamp",
        "heat_cons": "timestamp",
        "build_to_weath_map": None}
PRECISION = {"live_frequency": WritePrecision.S,
             "weather": WritePrecision.S,
             "electricity_cons": WritePrecision.S,
             "heat_cons": WritePrecision.S,
             "build_to_weath_map": WritePrecision.NS}  # Should be the default
FIELD_TYPES = {"live_frequency": {"value": "float"},
               "weather": {
                       "wind_speed_past1h": "float",
                       "temp_mean_past1h": "float",
                       "wind_dir_past1h": "float",
                       "humidity_past1h": "float",
                       "radia_glob_past1h": "float",
               },
               "electricity_cons": {"active_power_consumption": "float"},
               "heat_cons": {
                       "heating_consumption": "float",
                       "forward_temperature": "float",
                       "return_temperature": "float",
                       "volume_consumption": "float",
                       "flow_rate": "float",
               },
               "build_to_weath_map": {}}
# How many records to read (limit) and how many times (pages)
LIMIT_AND_PAGES = {"live_frequency": [1, 30],  # {'totalRecords': 13749458, 'nextPage': 1, 'totalPages': 1374946} as of 1.11.2024. New value every second
                   "weather": [100, 10],
                   "electricity_cons": [500, 10], # 500, 10  # Contains 2385653 items i.e. 23857 pages with 100 points per page
                   "heat_cons": [100, 10], # 100, 100 # Contains 2487840 records i.e. 248784 pages with 10 records per page
                   "build_to_weath_map": [100, 3]}  # {'totalRecords': 284, 'nextPage': 1, 'totalPages': 29}
PROCESSING_TIME = {"live_frequency": 1,
                   "weather": 5,
                   "electricity_cons": 5,
                   "heat_cons": 1,
                   "build_to_weath_map": 1}
