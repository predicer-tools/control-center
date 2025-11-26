"""Contains a class for running the main loop."""
import threading
import time
from PySide6.QtCore import QObject, Slot


class MainLoop(QObject):
    def __init__(self, task_started_signal, task_finished_signal, case_finished_signal):
        super().__init__()
        self._task_started_signal = task_started_signal  # Task name or ID
        self._task_finished_signal = task_finished_signal  # Task name or ID and finish state
        self._case_finished_signal = case_finished_signal  # Case name
        self.keep_going = True
        self.task_threads = dict()
        self._task_methods = {
            1: self.fetch_input_data_from_data_lake,
            2: self.transmit_input_data_to_influxdb_and_hertta_server,
            3: self.load_predicer_model,
            4: self.run_predicer,
            5: self.collect_output_data_from_predicer,
            6: self.transmit_output_data_to_influxdb_and_data_lake,
        }
        self._task_finished_signal.connect(self.run_next_task)

    def start_loop(self):
        """The loop:
            1: "Fetching input data from data lake",
            2: "Transmitting input data to InFluxDb and Hertta Server",
            3: "Loading Predicer model",
            4: "Running Predicer",
            5: "Collecting output data from Predicer",
            6: "Transmitting output data to InFluxDb and data lake",
        """
        self.task_threads[1] = TaskThread(1, self._task_started_signal, self._task_finished_signal)
        self.task_threads[1].start()

    @Slot(int, bool)
    def run_next_task(self, finished_task_id, success):
        t = self.task_threads.pop(finished_task_id)
        t.join()
        next_task = finished_task_id + 1
        if next_task > 6:
            self._case_finished_signal.emit()
            return
        if not self.keep_going:
            self._case_finished_signal.emit()
            return
        self.task_threads[next_task] = TaskThread(next_task, self._task_started_signal, self._task_finished_signal)
        self.task_threads[next_task].start()

    def fetch_input_data_from_data_lake(self):
        """Returns the data fetched from data lake."""
        self._task_started_signal.emit(1)
        time.sleep(1)
        self._task_finished_signal.emit(1, True)

    def transmit_input_data_to_influxdb_and_hertta_server(self):
        self._task_started_signal.emit(2)
        time.sleep(1)
        self._task_finished_signal.emit(2, True)

    def load_predicer_model(self):
        """Loads input data to Predicer."""
        self._task_started_signal.emit(3)
        time.sleep(1)
        self._task_finished_signal.emit(3, True)

    def run_predicer(self):
        """Runs Predicer."""
        self._task_started_signal.emit(4)
        time.sleep(1)
        self._task_finished_signal.emit(4, True)

    def collect_output_data_from_predicer(self):
        self._task_started_signal.emit(5)
        time.sleep(1)
        self._task_finished_signal.emit(5, True)

    def transmit_output_data_to_influxdb_and_data_lake(self):
        self._task_started_signal.emit(6)
        time.sleep(1)
        self._task_finished_signal.emit(6, True)


class TaskThread(threading.Thread):
    def __init__(self, task_id, task_started, task_finished):
        super().__init__(name="MainLoopTaskThread")
        self._task_id = task_id
        self._task_started = task_started
        self._task_finished = task_finished

    def run(self):
        self._task_started.emit(self._task_id)
        time.sleep(1)
        self._task_finished.emit(self._task_id, True)
