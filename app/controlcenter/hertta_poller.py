"""Thread for polling the Hertta Server status."""

import threading
from . import hertta_client_lib as lib
from time import sleep
from gql.transport.exceptions import TransportQueryError


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
        new_state, msg = lib.get_job_status(self._client, self._ds, self._job_id)

        if new_state != current_state:
            self._status_signal.emit(new_state, self._job_id)
            current_state = new_state
            if new_state in (lib.JobState.FAILED.value, lib.JobState.FINISHED.value):
                break

        if msg:
            self._logger_signal.emit(f"Job message: {msg}", self._job_id)
        sleep(2.0)

    final_state, final_msg = lib.get_job_status(self._client, self._ds, self._job_id)
    if final_state == lib.JobState.FAILED.value and final_msg:
        self._logger_signal.emit(f"Job failed: {final_msg}", self._job_id)

    if final_state == lib.JobState.FINISHED.value:
        try:
            output = lib.job_outcome(self._client, self._ds, self._job_id)
        except TransportQueryError as e:
            self._logger_signal.emit(f"GraphQL error fetching jobOutcome: {e}", self._job_id)
            output = {}
    else:
        output = {}

    self._finished_signal.emit(output, self._job_id)


