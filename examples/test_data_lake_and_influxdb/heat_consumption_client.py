"""Test reading data from data lake and uploading it to InfluxDb."""


import sys
import os
import time
import json
import datetime
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def delete_measurement(measurement_name, start):
    """Deletes given measurement and all time series it contains from influxdb from given start time to current time."""
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    stop = datetime.datetime.now()
    client.delete_api().delete(start, stop, f"_measurement={measurement_name}", bucket, org)
    client.close()


def main(args):
    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    requested_page_processing_time = 1 # seconds
    # NOTE: Heat Consumption contains 2487840 records i.e. 248784 pages with 10 records per page
    limit = 100
    for page in range(100):
        page_start_time = time.time()
        ok, response = post_request(limit, page)
        if ok:
            for i in range(len(response["data"])):
                d = response["data"][i]
                # Example d: {
                #   'return_temperature': 38.6,
                #   'cluster_id': '99',
                #   'heating_consumption': 0,
                #   'volume_consumption': 0.019,
                #   'flow_rate': 17.7,
                #   'forward_temperature': 56.9,
                #   'timestamp': '2022-08-31T23:00:00Z'
                #   }
                p_as_dict = {
                    "measurement": "HeatConsumption",
                    "tags": {"cluster_id": d["cluster_id"]},
                    "fields": {
                        "heating_consumption": d["heating_consumption"],
                        "forward_temperature": d["forward_temperature"],
                        "return_temperature": d["return_temperature"],
                        "volume_consumption": d["volume_consumption"],
                        "flow_rate": d["flow_rate"],
                    },
                    "time": d["timestamp"],
                }
                point = Point.from_dict(
                    p_as_dict,
                    write_precision=WritePrecision.S,
                    field_types={
                        "heating_consumption": "float",
                        "forward_temperature": "float",
                        "return_temperature": "float",
                        "volume_consumption": "float",
                        "flow_rate": "float",
                    },
                )
                write_api.write(bucket=bucket, org="ELEXIA", record=point)
            elapsed_t = time.time() - page_start_time
            print(f"Page {page} with {limit} points processed in {elapsed_t:0.2f}s")
            t_to_sleep = requested_page_processing_time - elapsed_t
            if t_to_sleep > 0:
                time.sleep(t_to_sleep)
        else:
            print(f"Request failed: {response}")
            break
    write_api.close()


def post_request(limit, page):
    url = "https://api.centerdenmark.com/api/v1/dataset/1c16f324-235f-473b-84fd-8c6f69b38cb5/query"
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
    influxdb_url = "http://localhost:8086"
    bucket = "Denmark-HeatConsumption"
    main(sys.argv)
    # start = datetime.datetime(year=2021, month=1, day=1, hour=10, minute=0, second=0)
    # delete_measurement("HeatConsumption", start)
