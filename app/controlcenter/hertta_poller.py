"""Thread for polling the Hertta Server status."""

import threading
import hertta_client_lib as lib
from time import sleep


class HerttaJobPoller(threading.Thread):
    def __init__(self, logger_signal, status_signal, client, ds, job_id, finished_signal):
        super().__init__(name="HerttaJobThread")
        self._logger_signal = logger_signal
        self._status_signal = status_signal
        self.keep_going = True
        self._client = client
        self._ds = ds
        self._job_id = job_id
        self._finished_signal = finished_signal

    def run(self):
        current_state = "NA"
        while self.keep_going:
            new_state, message = lib.get_job_status(self._client, self._ds, self._job_id)
            if new_state != current_state:
                self._status_signal.emit(new_state, self._job_id)
                if new_state == lib.JobState.FAILED.value or new_state == lib.JobState.FINISHED.value:
                    break
                current_state = new_state
            if message is not None:
                self._logger_signal.emit(f"Job message: {message}", self._job_id)
            sleep(2.0)
        output = lib.job_outcome(self._client, self._ds, self._job_id)
        self._finished_signal.emit(output, self._job_id)
