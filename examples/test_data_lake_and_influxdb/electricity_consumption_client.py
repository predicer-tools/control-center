"""Test reading data from data lake and uploading it to InfluxDb."""

import sys
import os
import time
import json
import datetime
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

data_lake_token = ""  # ** Add token or this script won't work **


def delete_measurement(measurement_name, start):
    """Deletes given measurement and all time series it contains from influxdb from given start time to current time."""
    client = InfluxDBClient(url=url, token=token, org=org)
    stop = datetime.datetime.now()
    client.delete_api().delete(start, stop, f"_measurement={measurement_name}", bucket, org)
    client.close()


def main(args):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    requested_page_processing_time = 5  # seconds
    # NOTE: Electricity Consumption has 2385653 items i.e. 23857 pages with 100 points per page
    limit = 100
    for page in range(100):
        page_start_time = time.time()
        ok, response = post_request(limit, page)
        if ok:
            for i in range(len(response["data"])):
                d = response["data"][i]
                # Example d is {
                #   'cluster_id': '99',
                #   'active_power_consumption': 0.117,
                #   'timestamp': '2022-08-31T23:00:00Z'
                #   }
                p_as_dict = {
                    "measurement": "ElectricityConsumption",
                    "tags": {"cluster_id": d["cluster_id"]},
                    "fields": {"active_power_consumption": d["active_power_consumption"]},
                    "time": d["timestamp"],
                }
                point = Point.from_dict(
                    p_as_dict,
                    write_precision=WritePrecision.S,
                    field_types={"active_power_consumption": "float"},
                )
                write_api.write(bucket=bucket, org="ELEXIA", record=point)
            elapsed_t = time.time() - page_start_time
            print(f"Page {page} with {limit} points processed in {elapsed_t:0.2f}s")
            time.sleep(requested_page_processing_time-elapsed_t)
        else:
            print(f"Request failed: {response}")
            break
    write_api.close()


def post_request(limit, page):
    url = "https://api.centerdenmark.com/api/v1/dataset/89efeff5-f96d-43c5-96d6-c3f6aeb22007/query"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + data_lake_token,
    }
    request_body = {
        "limit": limit,
        "page": page,
        "filters": [],
        "listFilters": [],
        "sortList": []
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    if response.ok:
        return True, response.json()
        # print(response.json())
    else:
        return False, str(response.status_code) + ": " + requests.status_codes._codes[response.status_code][0]


if __name__ == "__main__":
    # (ELEXIA organization?!) all-access token
    os.environ["INFLUXDB_TOKEN"] = ""  # ** Add token or this script won't work **
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "ELEXIA"
    url = "http://localhost:8086"
    bucket = "Denmark-ElectricityConsumption"
    main(sys.argv)
    # start = datetime.datetime(year=2021, month=1, day=1, hour=10, minute=0, second=0)
    # delete_measurement("ElectricityConsumption", start)
