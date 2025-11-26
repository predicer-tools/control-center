"""Thread for fetching data from Data Lake."""
import os
import threading
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from urllib3.exceptions import NewConnectionError
from config import (
    URLS, BUCKETS, MEASUREMENTS,
    TAGS, FIELDS, TIME, PRECISION, FIELD_TYPES, LIMIT_AND_PAGES, PROCESSING_TIME,
    ORG, INFLUXDB_URL
)
from connectivity_api import post_request, post_request_hertta


class FetchThread(threading.Thread):
    def __init__(self, dataset, log_signal, limit, pages, finished_signal):
        """Init thread.

        Args:
            dataset (str): Dataset name. See config file for accepted names
            log_signal (Signal): Signal for emitting messages to main thread
            limit (int): Batch size to fetch
            pages (range): Iterable giving the pages to fetch
            finished_signal (Signal): Emitted after the thread is finished to clean up the thread
        """
        super().__init__(name=f"{dataset} Thread")
        self._dataset = dataset
        self.keep_running = True
        self.log_signal = log_signal
        self._limit = limit
        self._pages = pages
        self.finished_signal = finished_signal

    def run(self):
        """Fetches data."""
        datalake_token = os.environ.get("DATALAKE_TOKEN")
        influxdb_token = os.environ.get("INFLUXDB_TOKEN")
        client = InfluxDBClient(url=INFLUXDB_URL, token=influxdb_token, org=ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        url = URLS[self._dataset]
        measurement = MEASUREMENTS[self._dataset]
        bucket = BUCKETS[self._dataset]
        tags_list = TAGS[self._dataset]
        fields_list = FIELDS[self._dataset]
        timestamp = TIME[self._dataset]
        precision = PRECISION[self._dataset]
        field_types = FIELD_TYPES[self._dataset]
        page_processing_time = PROCESSING_TIME[self._dataset]
        for page in self._pages:
            if not self.keep_running:
                break
            page_start_time = time.time()
            if self._dataset == "live_frequency":
                page = 0  # Get data from the latest page because the latest value is always at index 0
            ok, response = post_request(url, self._limit, page, datalake_token)
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
                    try:
                        write_api.write(bucket=bucket, org=ORG, record=point)
                    except NewConnectionError:
                        self.log_signal.emit("Connection to InfluxDb failed! Make sure InfluxDb is running.")
                        self.finished_signal.emit(threading.current_thread().name)
                        return
                elapsed_t = time.time() - page_start_time
                if self._dataset == "live_frequency":
                    self.log_signal.emit(f"Total pages:{self._pages}. {self._limit} point(s) processed in {elapsed_t:0.2f}s")
                else:
                    self.log_signal.emit(f"Page {page} with {self._limit} points processed in {elapsed_t:0.2f}s")
                t_to_sleep = page_processing_time - elapsed_t
                if t_to_sleep > 0:
                    time.sleep(t_to_sleep)
            else:
                self.log_signal.emit(f"Request failed: {response}")
                break
        write_api.close()
        self.finished_signal.emit(threading.current_thread().name)


class FetchPagination(threading.Thread):
    def __init__(self, statusbar_msg_signal, new_record_signal, finished_signal):
        super().__init__(name=f"FetchPaginationThread")
        self.statusbar_msg_signal = statusbar_msg_signal
        self.new_record_signal = new_record_signal
        self.finished_signal = finished_signal

    def run(self):
        """Fetches pagination data."""
        datalake_token = os.environ.get("DATALAKE_TOKEN")
        ok, response = post_request(URLS["weather"], 1, 1, datalake_token)
        if not ok:
            self.statusbar_msg_signal.emit("Fetching weather pagination failed")
            self.finished_signal.emit()
            return
        total = response["pagination"]["totalRecords"]
        self.new_record_signal.emit("weather", total)
        ok, response = post_request(URLS["electricity_cons"], 1, 1, datalake_token)
        if not ok:
            self.statusbar_msg_signal.emit("Fetching electricity consumption pagination failed")
            self.finished_signal.emit()
            return
        total = response["pagination"]["totalRecords"]
        self.new_record_signal.emit("elec_cons", total)
        ok, response = post_request(URLS["heat_cons"], 1, 1, datalake_token)
        if not ok:
            self.statusbar_msg_signal.emit("Fetching heat consumption pagination failed")
            self.finished_signal.emit()
            return
        total = response["pagination"]["totalRecords"]
        self.new_record_signal.emit("heat_cons", total)
        self.finished_signal.emit()


class FetchHerttaLocation(threading.Thread):
    def __init__(self, query, query_type, log_signal, response_dict_signal, finished_signal):
        super().__init__(name=f"FetchHerttaStatusThread")
        self.url = "http://127.0.0.1:3030/graphql"
        self.query = query
        self.query_type = query_type
        self.log_signal = log_signal
        self.response_dict_signal = response_dict_signal
        self.finished_signal = finished_signal

    def run(self):
        """Makes a query to Hertta and relays the response to the app."""
        ok, response = post_request_hertta(self.url, self.query)
        if not ok:
            self.log_signal.emit(response)
            self.finished_signal.emit()
            return
        self.log_signal.emit(str(response))
        if self.query_type == "location":
            self.response_dict_signal.emit(self.query_type, response)
        else:
            print(f"{self.query_type} has no handler yet")
        self.finished_signal.emit()

