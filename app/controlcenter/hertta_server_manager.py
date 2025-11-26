"""Contains the Hertta Server Process Manager."""
import threading
import subprocess
import os
import sys


class HerttaServerManager:
    def __init__(self, log_signal, finished_signal):
        self._process = None
        self._command = ["cargo", "run"]
        self._workdir = os.path.join("C:\\", "data", "GIT", "Hertta")
        self._stopped = False
        self.log_signal = log_signal
        self.finished_signal = finished_signal

    def start_hertta_server(self):
        self._stopped = False
        if not os.path.exists(self._workdir):
            self.log_signal.emit(f"Hertta Server path {self._workdir} not found")
            return False
        cf = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0  # Don't show console when frozen
        try:
            self._process = subprocess.Popen(
                self._command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self._workdir,
                creationflags=cf,
            )
        except OSError as e:
            self.log_signal.emit("[OSError] Hertta Server failed to start")
            return False
        threading.Thread(target=self._log_stdout, args=(self._process.stdout,), daemon=True).start()
        threading.Thread(target=self._log_stderr, args=(self._process.stderr,), daemon=True).start()
        return True

    def shutdown(self):
        self._stopped = True
        if self._process is not None:
            self._process.terminate()

    def _log_stdout(self, stdout):
        for line in iter(stdout.readline, b""):
            line = line.decode("UTF8", "replace").strip()
            self.log_signal.emit(line)
        stdout.close()

    def _log_stderr(self, stderr):
        for line in iter(stderr.readline, b""):
            line = line.decode("UTF8", "replace").strip()
            self.log_signal.emit(line)
        stderr.close()
