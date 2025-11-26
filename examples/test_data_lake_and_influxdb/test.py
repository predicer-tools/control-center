"""Test InfluxDb Python client."""

import os
import sys
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def main(args):
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "ELEXIA"
    url = "http://localhost:8086"
    bucket = "PythonTestBucket"

    # Make client
    client = InfluxDBClient(url=url, token=token, org=org)
    # Write data
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for value in range(5):
        point = (Point("measurement1").tag("tagname1", "tagvalue1").field("field1", value))
        write_api.write(bucket=bucket, org="ELEXIA", record=point)
        time.sleep(1)  # separate points by 1 second
    # Read data
    query_api = client.query_api()
    query_raw = """from(bucket: "PythonTestBucket")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "measurement1")"""
    query_mean = """from(bucket: "PythonTestBucket")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "measurement1")
        |> mean()"""
    tables = query_api.query(query_mean, org="ELEXIA")
    for table in tables:
        for record in table.records:
            print(record)


if __name__ == "__main__":
    os.environ["INFLUXDB_TOKEN"] = ""  # ** Add token or this script won't work **
    main(sys.argv)
