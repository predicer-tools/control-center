"""Contains the class for Control Center App main window."""
import os
import sys
import math
import datetime
from enum import unique, Enum
from PySide6.QtWidgets import QMainWindow, QApplication, QStyleFactory
from PySide6.QtCore import Qt, Slot, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon, QColor, QDesktopServices, QMovie
from influxdb_client import InfluxDBClient
from influxdb_client.rest import ApiException
from gql import dsl
from gql.transport.exceptions import TransportConnectionFailed
from . import hertta_client_lib as lib
import requests
from .ui.mainwindow import Ui_MainWindow
from .config import BUCKETS, MEASUREMENTS_BY_BUCKETS, LIMIT_AND_PAGES, PROCESSING_TIME, ORG, INFLUXDB_URL
from .fetch_thread import FetchThread, FetchPagination, FetchHerttaLocation
from .hertta_server_manager import HerttaServerManager
from .hertta_poller import HerttaJobPoller
from . import hertta_client_manager as hertta_client_manager
from . import hertta_client_manager_new as hertta_client_manager_new
from .main_loop import MainLoop


@unique
class TaskState(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    STOPPED = "STOPPED"


class ControlCenter(QMainWindow):

    append_freq_msg = Signal(str)
    append_weather_msg = Signal(str)
    append_elec_msg = Signal(str)
    append_heat_msg = Signal(str)
    append_hertta_server_msg = Signal(str)
    hertta_client_msg = Signal(str)
    hertta_job_msg = Signal(str, int)
    hertta_job_status_signal = Signal(str, int)
    hertta_job_finished_signal = Signal(dict, int)
    statusbar_msg_signal = Signal(str)
    new_record_signal = Signal(str, int)
    new_response_signal = Signal(str, dict)
    fetch_pagination_finished_signal = Signal()
    fetch_thread_finished_signal = Signal(str)
    task_started_signal = Signal(int)
    task_finished_signal = Signal(int, bool)
    case_finished_signal = Signal()

    def __init__(self):
        super().__init__(flags=Qt.WindowType.Window)
        self.set_app_style()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addAction(self.ui.actionQuit)
        self._fetch_records_thread = None
        self._live_freq_thread = None
        self._weather_thread = None
        self._query_hertta_thread = None
        self._elec_thread = None
        self._heat_thread = None
        self._n_weather_records = None
        self._n_elec_records = None
        self._n_heat_records = None
        self._hertta_server_manager = None
        self._hertta_jobs = dict()
        self._ml = None
        self._case_name = "abc"
        self._loop_nr = 0
        self._case_root_item = None
        self._current_task_item = None
        self.tasks = {
            1: "Fetching input data from data lake",
            2: "Transmitting input data to InFluxDb and Hertta Server",
            3: "Loading Predicer model",
            4: "Running Predicer",
            5: "Collecting output data from Predicer",
            6: "Transmitting output data to InFluxDb and data lake",
        }
        self.tasks_model = QStandardItemModel()
        self.ui.treeView_tasks.setModel(self.tasks_model)
        self._case_animation = QMovie(":/icons/ajax-loader.gif")
        self._task_animation = QMovie(":/icons/ajax-loader.gif")
        self.init_widgets()
        self.connect_signals()
        self._test_connection_to_hertta()

    def connect_signals(self):
        """Connects signals to slots."""
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.toolButton_start_master_loop.clicked.connect(self._start_loop)
        self.ui.toolButton_stop_master_loop.clicked.connect(self._stop_loop)
        self.ui.toolButton_fetch_total_records.clicked.connect(self.fetch_total_records)
        self.ui.toolButton_play_live_frequency.clicked.connect(self.start_live_frequency)
        self.ui.toolButton_stop_live_frequency.clicked.connect(self.stop_live_frequency)
        self.ui.toolButton_play_weather.clicked.connect(self.start_weather)
        self.ui.toolButton_play_weather_backwards.clicked.connect(self.start_weather_backwards)
        self.ui.toolButton_stop_weather.clicked.connect(self.stop_weather)
        self.ui.toolButton_play_electricity_consumption.clicked.connect(self.start_elec)
        self.ui.toolButton_play_electricity_consumption_backwards.clicked.connect(self.start_elec_backwards)
        self.ui.toolButton_stop_electricity_consumption.clicked.connect(self.stop_elec)
        self.ui.toolButton_play_heat_consumption.clicked.connect(self.start_heat)
        self.ui.toolButton_play_heat_consumption_backwards.clicked.connect(self.start_heat_backwards)
        self.ui.toolButton_stop_heat_consumption.clicked.connect(self.stop_heat)
        self.ui.toolButton_delete_data_from_influxdb.clicked.connect(self.delete_measurements)
        self.ui.toolButton_start_hertta_server.clicked.connect(self.start_hertta_server)
        self.ui.toolButton_run_building_optimization.clicked.connect(self.run_building_optimization)
        self.ui.toolButton_query_hertta_settings.clicked.connect(self.query_hertta_settings)
        self.ui.toolButton_update_hertta_settings.clicked.connect(self.update_hertta_settings)
        self.ui.toolButton_open_hertta_settings_file.clicked.connect(self._open_hertta_settings)
        self.statusbar_msg_signal.connect(self.show_statusbar_msg)
        self.new_record_signal.connect(self.update_total_records_label)
        self.new_response_signal.connect(self.process_hertta_response)
        self.fetch_pagination_finished_signal.connect(self.fetch_total_records_thread_finished)
        self.fetch_thread_finished_signal.connect(self.fetch_thread_finished)
        self.append_freq_msg.connect(self.append_to_freq_log)
        self.append_weather_msg.connect(self.append_to_common_log)
        self.append_elec_msg.connect(self.append_to_common_log)
        self.append_heat_msg.connect(self.append_to_common_log)
        self.append_hertta_server_msg.connect(self.append_to_hertta_log)
        self.hertta_client_msg.connect(self.append_to_hertta_client_log)
        self.hertta_job_msg.connect(self.append_hertta_job_msg)
        self.hertta_job_status_signal.connect(self.set_hertta_job_status)
        self.hertta_job_finished_signal.connect(self.handle_hertta_job_output)
        self.task_started_signal.connect(self.handle_task_started)
        self.task_finished_signal.connect(self.handle_task_finished)
        self.case_finished_signal.connect(self.handle_case_finished)
        self._case_animation.frameChanged.connect(self._update_case_animation)
        self._task_animation.frameChanged.connect(self._update_task_animation)

    def init_widgets(self):
        self.ui.comboBox_bucket.addItem("Select a bucket...")
        self.ui.comboBox_bucket.addItems(BUCKETS.values())
        self.ui.spinBox_limit_freq.setValue(LIMIT_AND_PAGES["live_frequency"][0])
        self.ui.spinBox_page_freq.setValue(LIMIT_AND_PAGES["live_frequency"][1])
        self.ui.spinBox_limit_weather.setValue(LIMIT_AND_PAGES["weather"][0])
        self.ui.spinBox_page_weather.setValue(LIMIT_AND_PAGES["weather"][1])
        self.ui.spinBox_limit_elec.setValue(LIMIT_AND_PAGES["electricity_cons"][0])
        self.ui.spinBox_page_elec.setValue(LIMIT_AND_PAGES["electricity_cons"][1])
        self.ui.spinBox_limit_heat.setValue(LIMIT_AND_PAGES["heat_cons"][0])
        self.ui.spinBox_page_heat.setValue(LIMIT_AND_PAGES["heat_cons"][1])

    @Slot(bool)
    def _start_loop(self, _=False):
        """Starts the main event loop of Control Center if all subprocesses are ready to go
        (Hertta server, InFluxDb server, Grafana server).
        """
        self._loop_nr += 1
        self._case_name = "abc" + "-" + str(self._loop_nr)
        self._ml = MainLoop(self.task_started_signal, self.task_finished_signal, self.case_finished_signal)
        icon = QIcon(self._case_animation.currentPixmap())
        self._case_root_item = QStandardItem(icon, self._case_name)
        self.tasks_model.appendRow(self._case_root_item)
        self.ui.treeView_tasks.expand(self._case_root_item.index())
        self._case_animation.start()
        self._ml.start_loop()
        self.ui.toolButton_start_master_loop.setEnabled(False)
        self.ui.toolButton_stop_master_loop.setEnabled(True)

    @Slot(int)
    def handle_task_started(self, task_nr):
        self.ui.label_current_task.setText(self.tasks[task_nr])
        icon = QIcon(self._task_animation.currentPixmap())
        self._current_task_item = QStandardItem(icon, "Task #" + str(task_nr))
        self._case_root_item.setChild(task_nr-1, self._current_task_item)
        self._task_animation.start()
        self.ui.treeView_tasks.scrollToBottom()

    @Slot(int, bool)
    def handle_task_finished(self, task_nr, success):
        self._task_animation.stop()
        if not self._ml.keep_going:
            icon = self.make_icon(TaskState.STOPPED)
        else:
            icon = self.make_icon(TaskState.SUCCEEDED) if success else self.make_icon(TaskState.FAILED)
        self._current_task_item.setIcon(icon)

    @Slot()
    def handle_case_finished(self):
        self._case_animation.stop()
        if not self._ml.keep_going:
            icon = self.make_icon(TaskState.STOPPED)
            self._case_root_item.setIcon(icon)
            self.ui.toolButton_start_master_loop.setEnabled(True)
            self.ui.toolButton_stop_master_loop.setEnabled(False)
            self.ui.label_current_task.setText("Press Start to continue")
            self._ml.deleteLater()
            self._ml = None
            return
        icon = self.make_icon(TaskState.SUCCEEDED)
        self._case_root_item.setIcon(icon)
        self._ml.deleteLater()
        self._ml = None
        self._start_loop()

    @Slot(bool)
    def _stop_loop(self, _=False):
        if self._ml is not None:
            self._ml.keep_going = False

    @Slot(bool)
    def fetch_total_records(self, _=False):
        self.ui.toolButton_fetch_total_records.setEnabled(False)
        self._fetch_records_thread = FetchPagination(
            self.statusbar_msg_signal, self.new_record_signal, self.fetch_pagination_finished_signal
        )
        self._fetch_records_thread.start()

    @Slot()
    def fetch_total_records_thread_finished(self):
        self._fetch_records_thread.join()
        self._fetch_records_thread = None
        self.ui.toolButton_fetch_total_records.setEnabled(True)

    @Slot(str, int)
    def update_total_records_label(self, dataset, nr_of_records):
        if dataset == "weather":
            limit = self.ui.spinBox_limit_weather.value()
            n_pages = math.ceil(nr_of_records/limit)
            self.ui.label_weather_total_records.setText(f"Records: {nr_of_records} Pages: {n_pages}")
            self._n_weather_records = nr_of_records
        elif dataset == "elec_cons":
            limit = self.ui.spinBox_limit_elec.value()
            n_pages = math.ceil(nr_of_records/limit)
            self.ui.label_elec_total_records.setText(f"Records: {nr_of_records} Pages: {n_pages}")
            self._n_elec_records = nr_of_records
        elif dataset == "heat_cons":
            limit = self.ui.spinBox_limit_heat.value()
            n_pages = math.ceil(nr_of_records/limit)
            self.ui.label_heat_total_records.setText(f"Records: {nr_of_records} Pages: {n_pages}")
            self._n_heat_records = nr_of_records
        else:
            self.show_statusbar_msg(f"Unknown {dataset}")

    @Slot(bool)
    def start_live_frequency(self, _=False):
        """Starts fetching live frequency data."""
        limit = self.ui.spinBox_limit_freq.value()
        pages = self.ui.spinBox_page_freq.value()
        self._live_freq_thread = FetchThread(
            "live_frequency", self.append_freq_msg, limit, range(pages), self.fetch_thread_finished_signal
        )
        self.append_freq_msg.emit(f"Downloading Live Frequency -> InfluxDb bucket {BUCKETS['live_frequency']}"
                                  f"Updates every {PROCESSING_TIME['live_frequency']}s.")
        self._live_freq_thread.start()
        self.ui.toolButton_play_live_frequency.setEnabled(False)

    @Slot(bool)
    def stop_live_frequency(self, _=False):
        if self._live_freq_thread is not None:
            self.append_freq_msg.emit("Stopping Live Frequency")
            self._live_freq_thread.keep_running = False

    @Slot(bool)
    def start_weather(self, _=False):
        """Starts fetching weather data."""
        limit = self.ui.spinBox_limit_weather.value()
        pages = self.ui.spinBox_page_weather.value()
        self.start_weather_thread(limit, range(pages))

    @Slot(bool)
    def start_weather_backwards(self, _=False):
        """Starts fetching weather data from the last page towards the beginning.
        The number of records must be known for this to work."""
        limit = self.ui.spinBox_limit_weather.value()
        pages = self.ui.spinBox_page_weather.value()
        if not self._n_weather_records:
            self.show_statusbar_msg("Click refresh first!")
            return
        pages_range = self.make_pages_iterable(int(self._n_weather_records), limit, pages)
        self.start_weather_thread(limit, pages_range)

    def start_weather_thread(self, limit, pages_range):
        """Creates a Fetch Thread for downloading Weather data and starts it.

        Data from: 2021-09-01
        Data to: 2022-08-31

        Args:
            limit (int): Batch size
            pages_range (range): Iterable containing the page indexes to fetch
        """
        self._weather_thread = FetchThread(
            "weather", self.append_weather_msg, limit, pages_range, self.fetch_thread_finished_signal
        )
        self.append_weather_msg.emit(f"[{pages_range}] Downloading Weather data -> InfluxDb bucket {BUCKETS['weather']}. "
                                     f"Updates every {PROCESSING_TIME['weather']}s.")
        self._weather_thread.start()
        self.ui.toolButton_play_weather.setEnabled(False)
        self.ui.toolButton_play_weather_backwards.setEnabled(False)

    @Slot(bool)
    def stop_weather(self, _=False):
        if self._weather_thread is not None:
            self._weather_thread.keep_running = False

    @Slot(bool)
    def start_elec(self, _=False):
        """Starts fetching Electricity Consumption data."""
        limit = self.ui.spinBox_limit_elec.value()
        pages = self.ui.spinBox_page_elec.value()
        self.start_elec_thread(limit, range(pages))

    @Slot(bool)
    def start_elec_backwards(self, _=False):
        """Starts fetching Electricity Consumption data from the last page towards the beginning.
        The number of records must be known beforehand."""
        limit = self.ui.spinBox_limit_elec.value()
        pages = self.ui.spinBox_page_elec.value()
        if not self._n_elec_records:
            self.show_statusbar_msg("Click refresh first!")
            return
        pages_range = self.make_pages_iterable(int(self._n_elec_records), limit, pages)
        self.start_elec_thread(limit, pages_range)

    def start_elec_thread(self, limit, pages_range):
        """Creates a Fetch Thread for downloading Electricity Consumption data and starts it.

        Data from: 2021-09-01
        Data to: 2022-08-31

        Args:
            limit (int): Batch size
            pages_range (range): Iterable containing the page indexes to fetch
        """
        self._elec_thread = FetchThread(
            "electricity_cons", self.append_elec_msg, limit, pages_range, self.fetch_thread_finished_signal
        )
        self.append_elec_msg.emit(f"[{pages_range}] Downloading Electricity Consumption data -> InfluxDb bucket "
                                  f"{BUCKETS['electricity_cons']}. Updates every "
                                  f"{PROCESSING_TIME['electricity_cons']}s.")
        self._elec_thread.start()
        self.ui.toolButton_play_electricity_consumption.setEnabled(False)
        self.ui.toolButton_play_electricity_consumption_backwards.setEnabled(False)

    @Slot(bool)
    def stop_elec(self, _=False):
        if self._elec_thread is not None:
            self._elec_thread.keep_running = False

    @Slot(bool)
    def start_heat(self, _=False):
        """Starts fetching Heat Consumption data."""
        limit = self.ui.spinBox_limit_heat.value()
        pages = self.ui.spinBox_page_heat.value()
        self.start_heat_thread(limit, range(pages))

    @Slot(bool)
    def start_heat_backwards(self, _=False):
        """Starts fetching Heat Consumption data from the last page towards the beginning.
        The number of records must be known beforehand."""
        limit = self.ui.spinBox_limit_heat.value()
        pages = self.ui.spinBox_page_heat.value()
        if not self._n_heat_records:
            self.show_statusbar_msg("Click refresh first!")
            return
        pages_range = self.make_pages_iterable(int(self._n_heat_records), limit, pages)
        self.start_heat_thread(limit, pages_range)

    def start_heat_thread(self, limit, pages_range):
        """Creates a Fetch Thread for downloading Heat Consumption data and starts it.

        Data from: 2021-09-01
        Data to: 2022-08-31

        Args:
            limit (int): Batch size
            pages_range (range): Iterable containing the page indexes to fetch
        """
        self._heat_thread = FetchThread(
            "heat_cons", self.append_heat_msg, limit, pages_range, self.fetch_thread_finished_signal
        )
        self.append_heat_msg.emit(f"[{pages_range}] Downloading Heat Consumption data -> InfluxDb bucket "
                                  f"{BUCKETS['heat_cons']}. Updates every "
                                  f"{PROCESSING_TIME['heat_cons']}s.")
        self._heat_thread.start()
        self.ui.toolButton_play_heat_consumption.setEnabled(False)
        self.ui.toolButton_play_heat_consumption_backwards.setEnabled(False)

    @Slot(bool)
    def stop_heat(self, _=False):
        if self._heat_thread is not None:
            self._heat_thread.keep_running = False

    @Slot(str)
    def fetch_thread_finished(self, thread_name):
        self.statusbar_msg_signal.emit(f"{thread_name} finished")
        if thread_name == "live_frequency Thread":
            self._live_freq_thread.join()
            self._live_freq_thread = None
            self.ui.toolButton_play_live_frequency.setEnabled(True)
        elif thread_name == "weather Thread":
            self._weather_thread.join()
            self._weather_thread = None
            self.ui.toolButton_play_weather.setEnabled(True)
            self.ui.toolButton_play_weather_backwards.setEnabled(True)
        elif thread_name == "electricity_cons Thread":
            self._elec_thread.join()
            self._elec_thread = None
            self.ui.toolButton_play_electricity_consumption.setEnabled(True)
            self.ui.toolButton_play_electricity_consumption_backwards.setEnabled(True)
        elif thread_name == "heat_cons Thread":
            self._heat_thread.join()
            self._heat_thread = None
            self.ui.toolButton_play_heat_consumption.setEnabled(True)
            self.ui.toolButton_play_heat_consumption_backwards.setEnabled(True)
        else:
            self.append_to_common_log(f"Error! {thread_name} not found")

    @Slot(bool)
    def delete_measurements(self, _=False):
        """Deletes a measurement and all time series it
        contains from influxdb from given start time to
        current time."""
        bucket = self.ui.comboBox_bucket.currentText()
        if bucket not in BUCKETS.values():
            self.ui.statusbar.showMessage("Select a bucket from the drop-down menu", timeout=2000)
            return
        influxdb_token = os.environ.get("INFLUXDB_TOKEN")
        client = InfluxDBClient(url=INFLUXDB_URL, token=influxdb_token, org=ORG)
        measurement_name = MEASUREMENTS_BY_BUCKETS[bucket]
        start = datetime.datetime(year=2021, month=1, day=1, hour=10, minute=0, second=0)
        stop = datetime.datetime.now()
        try:
            client.delete_api().delete(start, stop, f"_measurement={measurement_name}", bucket, ORG)
        except ApiException as e:
            # print(e)  # for details
            self.ui.statusbar.showMessage(f"Failed! Make sure the bucket exists and InFluxDb is running", timeout=10000)
        else:
            self.ui.statusbar.showMessage(f"Bucket {bucket} has been wiped clean", timeout=4000)
        finally:
            client.close()

    @Slot(bool)
    def start_hertta_server(self, _=False):
        """Starts Hertta Server thread."""
        self._hertta_server_manager = HerttaServerManager(self.append_hertta_server_msg, self.statusbar_msg_signal)
        if not self._hertta_server_manager.start_hertta_server():
            self.set_hertta_disconnected()
            return
        self.set_hertta_connected()

    def shutdown_hertta_server(self):
        if self._hertta_server_manager is not None:
            self._hertta_server_manager.shutdown()
        self._hertta_server_manager = None
        self.set_hertta_disconnected()

    @Slot(bool)
    def query_hertta_settings(self):
        """Queries country from Hertta Server settings."""
        if not self._test_connection_to_hertta():
            self.hertta_client_msg.emit("Hertta Server offline")
            return
        URL = "http://127.0.0.1:3030/graphql"
        client, dsl_schema = lib.client_and_dsl(URL)
        # Query.Settings
        field = dsl_schema.Query.settings.select(
            dsl_schema.Settings.location.select(
                dsl_schema.LocationSettings.country, dsl_schema.LocationSettings.place
            )
        )
        dsl_query_location = dsl.DSLQuery(field)
        location_operation = dsl.dsl_gql(dsl_query_location)
        self.set_hertta_job_in_progress()
        try:
            loc = client.execute(location_operation)
        except requests.exceptions.ConnectionError:
            self.set_hertta_disconnected()
            return False
        print(f"LocationSettings:{loc}")
        self.hertta_client_msg.emit(str(loc))
        # Query.Model.TimeLineSettings
        field = dsl_schema.Query.model.select(
            dsl_schema.Model.timeLine.select(
                dsl_schema.TimeLineSettings.step.select(
                    dsl_schema.Duration.hours, dsl_schema.Duration.minutes, dsl_schema.Duration.seconds
                ), dsl_schema.TimeLineSettings.duration.select(
                    dsl_schema.Duration.hours, dsl_schema.Duration.minutes, dsl_schema.Duration.seconds
                )
            )
        )
        dsl_query_time_line = dsl.DSLQuery(field)
        tl_operation = dsl.dsl_gql(dsl_query_time_line)
        try:
            tl = client.execute(tl_operation)
        except requests.exceptions.ConnectionError:
            self.set_hertta_disconnected()
            return False
        self.set_hertta_connected()
        self.hertta_client_msg.emit(str(tl))
        print(f"TimeLineSettings:{tl}")
        return True

    @Slot(bool)
    def update_hertta_settings(self, _=False):
        """Gets current time_line and location settings and writes them to Hertta Server settings."""
        time_line_step = self.ui.spinBox_time_line_step.value()
        time_line_duration = self.ui.spinBox_time_line_duration.value()
        location_country = self.ui.lineEdit_location_country.text().strip()
        location_place = self.ui.lineEdit_location_place.text().strip()
        print(f"step:{time_line_step} duration:{time_line_duration} country:{location_country} place:{location_place}")
        # self.hertta_settings = dict()

    @Slot(bool)
    def _open_hertta_settings(self, _=False):
        # QStandardPaths.StandardLocation.ConfigLocation == C:/Users/ttepsa/AppData/Local/Control Center
        appdata_local_dir, _ = os.path.split(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation))
        settings_fpath = os.path.join(appdata_local_dir, "hertta", "config", "settings.toml")
        if not os.path.exists(settings_fpath):
            self.statusbar_msg_signal.emit(f"{settings_fpath} does not exist")
            return
        url = "file:///" + settings_fpath
        QDesktopServices.openUrl(QUrl(url, QUrl.ParsingMode.TolerantMode))

    @Slot(bool)
    def _test_connection_to_hertta(self, _=False):
        """Queries country from Hertta Server settings."""
        URL = "http://127.0.0.1:3030/graphql"
        client, dsl_schema = lib.client_and_dsl(URL)
        field = dsl_schema.Query.settings.select(
            dsl_schema.Settings.location.select(
                dsl_schema.LocationSettings.country
            )
        )
        dsl_query = dsl.DSLQuery(field)
        operation = dsl.dsl_gql(dsl_query)
        try:
            client.execute(operation)
        except (TransportConnectionFailed, requests.exceptions.ConnectionError) as e:
            self.set_hertta_disconnected()
            return False
        self.set_hertta_connected()
        return True

    @Slot(bool)
    def run_building_optimization(self):
        if not self._test_connection_to_hertta():
            self.hertta_client_msg.emit(f"[ConnectionError] Hertta Server did not respond at {hertta_client_manager.URL}")
            return
        client, ds, job_id = hertta_client_manager.start_optimization()
        t = self._hertta_jobs[job_id] = HerttaJobPoller(self.hertta_job_msg, self.hertta_job_status_signal, client, ds, job_id, self.hertta_job_finished_signal)
        t.start()

    @Slot(str, int)
    def set_hertta_job_status(self, status, job_id):
        if status == "QUEUED":
            self.hertta_job_msg.emit(f"Job is queued", job_id)
        elif status == "IN_PROGRESS":
            self.hertta_job_msg.emit(f"Job is in progress", job_id)
            self.set_hertta_job_in_progress()
        elif status == "FAILED":
            self.hertta_job_msg.emit(f"Job failed", job_id)
            self.set_hertta_job_finished(True)
        elif status == "FINISHED":
            self.hertta_job_msg.emit(f"Job finished", job_id)
            self.set_hertta_job_finished(False)
        else:
            self.hertta_job_msg.emit(f"Unrecognized job status:{status}", job_id)

    @Slot(dict, int)
    def handle_hertta_job_output(self, outcome, job_id):
        if outcome is not None:
            self.hertta_job_msg.emit(str(outcome), job_id)
        t = self._hertta_jobs.pop(job_id)
        t.join()

    def set_hertta_disconnected(self):
        self.ui.progressBar_hertta_status.setRange(0, 1)
        self.ui.progressBar_hertta_status.setValue(1)
        self.ui.progressBar_hertta_status.setStyleSheet("QProgressBar"
                                                        "{border: 1px solid grey; border-radius: 5px;}"
                                                        "QProgressBar::chunk"
                                                        "{background-color: red; margin-top: 5px;"
                                                        "margin-bottom: 5px; border-radius: 3px;}")
        self.ui.label_hertta_server_status.setText("offline")

    def set_hertta_connected(self):
        self.ui.progressBar_hertta_status.setRange(0, 1)
        self.ui.progressBar_hertta_status.setValue(1)
        self.ui.progressBar_hertta_status.setStyleSheet("QProgressBar"
                                                        "{border: 1px solid grey; border-radius: 5px;}"
                                                        "QProgressBar::chunk"
                                                        "{background-color: blue; margin-top: 5px;"
                                                        "margin-bottom: 5px; border-radius: 3px;}")
        self.ui.label_hertta_server_status.setText("online")

    def set_hertta_job_in_progress(self):
        self.ui.progressBar_hertta_status.setRange(0, 0)
        self.ui.progressBar_hertta_status.setStyleSheet("QProgressBar"
                                                        "{border: 1px solid grey; border-radius: 5px;}"
                                                        "QProgressBar::chunk"
                                                        "{background-color: green; margin-top: 10px;"
                                                        "margin-bottom: 10px;}")
        self.ui.label_hertta_server_status.setText("busy")

    def set_hertta_job_finished(self, failed):
        ss = "QProgressBar"
        "{border: 1px solid grey; border-radius: 5px;}"
        "QProgressBar::chunk"
        "{background-color: light-green; margin-top: 5px;"
        "margin-bottom: 5px; border-radius: 3px;}"
        if failed:
            ss = "QProgressBar"
            "{border: 1px solid grey; border-radius: 5px;}"
            "QProgressBar::chunk"
            "{background-color: pink; margin-top: 5px;"
            "margin-bottom: 5px; border-radius: 3px;}"
        self.ui.progressBar_hertta_status.setRange(0, 1)
        self.ui.progressBar_hertta_status.setValue(1)
        self.ui.progressBar_hertta_status.setStyleSheet(ss)
        self.ui.label_hertta_server_status.setText("idle")

    @Slot(bool)
    def query_hertta_location(self, _=False):
        """Queries Hertta Server location."""
        query = {'query': '{ settings { location { country } } }'}
        query_type = "location"
        self.start_hertta_thread(query, query_type)

    def start_hertta_thread(self, query, t):
        self._query_hertta_thread = FetchHerttaLocation(
            query, t, self.append_hertta_server_msg, self.new_response_signal, self.query_hertta_finished_signal
        )
        self._query_hertta_thread.start()

    @Slot()
    def query_hertta_thread_finished(self):
        self._query_hertta_thread.join()
        self._query_hertta_thread = None

    @Slot(str, dict)
    def process_hertta_response(self, response_type, response):
        if response_type == "location":
            data = response.get("data", None)
            if not data:
                print("data key missing")
                return
            settings = data.get("settings", None)
            if not settings:
                print("settings key missing")
                return
            location = settings.get("location", "NA")
            if location == "NA":
                print("location key missing")
                return
            self.ui.label_hertta_location.setText(location)
        else:
            print(f"response_type:{response_type} does not have a handler")

    @Slot(str)
    def append_to_freq_log(self, msg):
        self.ui.textBrowser_freq.append(msg)

    @Slot(str)
    def append_to_common_log(self, msg):
        self.ui.textBrowser_log.append(msg)

    @Slot(str)
    def append_to_hertta_log(self, msg):
        self.ui.textBrowser_hertta_output.append(msg)

    @Slot(str)
    def append_to_hertta_client_log(self, msg):
        self.ui.textBrowser_hertta_client_output.append(msg)

    @Slot(str, int)
    def append_hertta_job_msg(self, msg, job_id):
        self.ui.textBrowser_hertta_client_output.append(f"[{str(job_id)}] " + msg)

    @Slot(str)
    def show_statusbar_msg(self, txt):
        self.ui.statusbar.showMessage(txt, timeout=5000)

    def make_icon(self, state):
        if state == TaskState.STOPPED:
            color = QColor("orange")
        elif state == TaskState.FAILED:
            color = QColor("red")
        elif state == TaskState.SUCCEEDED:
            color = QColor("green")
        else:
            self.statusbar_msg_signal.emit(f"Unknown state:{state}")
            return QIcon()
        pixmap = QPixmap(20, 20)
        pixmap.fill(color)
        return QIcon(pixmap)

    def _update_case_animation(self):
        self._case_root_item.setIcon(QIcon(self._case_animation.currentPixmap()))

    def _update_task_animation(self):
        self._current_task_item.setIcon(QIcon(self._task_animation.currentPixmap()))

    def closeEvent(self, event):
        """Closing the app."""
        self.shutdown_hertta_server()

    @staticmethod
    def make_pages_iterable(n_records, limit, pages):
        """Calculates an iterable going from the last page towards the beginning.

        Args:
            n_records (int): Number of records in the data set
            limit (int): Batch size to fetch
            pages (int): Number of pages to fetch

        Returns:
            range: Iterable containing integers going from the last page towards the beginning
        """
        # Number of pages with the selected batch size is: ceiling(n_records/limit)
        n_pages = math.ceil(n_records/limit)  # Number of pages with data
        # Iterable with selected number of page indexes, going from the last page towards the first page
        if pages >= n_pages:
            # Return iterable [n_pages, n_pages-1, n_pages-2, ... 0]
            retval = range(n_pages, 0, -1)
        else:
            retval = range(n_pages, n_pages-pages, -1)
        return retval

    @staticmethod
    def set_app_style():
        """Sets App style on Windows to 'windowsvista'."""
        if sys.platform == "win32":
            if "windowsvista" not in QStyleFactory.keys():
                return
            QApplication.setStyle("windowsvista")
