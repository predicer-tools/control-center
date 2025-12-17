import sys
import os
import time
import datetime
import tomllib
import pathlib
from .connectivity_api import post_request
from .config import (
    TOKENFILE, URLS, BUCKETS, MEASUREMENTS,
    TAGS, FIELDS, TIME, PRECISION, FIELD_TYPES, LIMIT_AND_PAGES, PROCESSING_TIME,
    ORG, INFLUXDB_URL
)
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def setup():
    """Loads tokens to environment variables."""
    p = pathlib.Path(__file__).parent.resolve() / TOKENFILE
    if not p.is_file():
        print(f"{TOKENFILE} missing")
        return False
    with open(p, "rb") as f:
        contents = tomllib.load(f)
        datalake_token = contents.get("datalake_token", "")
        influxdb_token = contents.get("influxdb_token", "")
    if not datalake_token:
        print(f"Key 'datalake_token' missing from {TOKENFILE}")
        return False
    if not influxdb_token:
        print(f"Key 'influxdb_token' missing from {TOKENFILE}")
        return False
    os.environ["DATALAKE_TOKEN"] = datalake_token
    os.environ["INFLUXDB_TOKEN"] = influxdb_token
    return True


def delete_measurement(start):
    """Deletes given measurement and all time series it contains from influxdb from given start time to current time."""
    influxdb_token = os.environ.get("INFLUXDB_TOKEN")
    client = InfluxDBClient(url=INFLUXDB_URL, token=influxdb_token, org=ORG)
    stop = datetime.datetime.now()
    measurement_name = MEASUREMENTS[dataset]
    bucket = BUCKETS[dataset]
    client.delete_api().delete(start, stop, f"_measurement={measurement_name}", bucket, ORG)
    client.close()


def main(args):
    datalake_token = os.environ.get("DATALAKE_TOKEN")
    influxdb_token = os.environ.get("INFLUXDB_TOKEN")
    client = InfluxDBClient(url=INFLUXDB_URL, token=influxdb_token, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    url = URLS[dataset]
    measurement = MEASUREMENTS[dataset]
    bucket = BUCKETS[dataset]
    tags_list = TAGS[dataset]
    fields_list = FIELDS[dataset]
    timestamp = TIME[dataset]
    precision = PRECISION[dataset]
    field_types = FIELD_TYPES[dataset]
    limit, pages = LIMIT_AND_PAGES[dataset]
    page_processing_time = PROCESSING_TIME[dataset]
    for page in range(pages):
        page_start_time = time.time()
        if dataset == "live_frequency":
            page = 0  # Get data from the latest page because the latest value is always at index 0
        ok, response = post_request(url, limit, page, datalake_token)
        if ok:
            for i in range(len(response["data"])):
                d = response["data"][i]
                p_as_dict = {
                    "measurement": measurement,
                    "tags": {t: d[t] for t in tags_list},
                    "fields": {f: d[f] for f in fields_list},
                }
                if timestamp is not None:
                    p_as_dict["time"] = d[timestamp]
                point = Point.from_dict(
                    p_as_dict,
                    write_precision=precision,
                    field_types=field_types,
                )
                write_api.write(bucket=bucket, org=ORG, record=point)
            elapsed_t = time.time() - page_start_time
            print(f"Page {page} with {limit} points processed in {elapsed_t:0.2f}s")
            t_to_sleep = page_processing_time - elapsed_t
            if t_to_sleep > 0:
                time.sleep(t_to_sleep)
        else:
            print(f"Request failed: {response}")
            break
    write_api.close()


if __name__ == "__main__":
    if not setup():
        sys.exit()
    # dataset is one of "live_frequency", "weather", "electricity_cons", "heat_cons", or "build_to_weath_map"
    dataset = "weather"
    # dataset = "electricity_cons"
    # dataset = "heat_cons"
    # dataset = "live_frequency"
    main(sys.argv)
    # start = datetime.datetime(year=2021, month=1, day=1, hour=10, minute=0, second=0)
    # delete_measurement(start)
