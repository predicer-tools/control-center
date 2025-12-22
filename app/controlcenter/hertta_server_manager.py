"""Contains the Hertta Server Process Manager."""
import threading
import subprocess
import os
import sys
from time import sleep, time
import requests

class HerttaServerManager:
    def __init__(self, log_signal, finished_signal):
        self._process = None
        self._command = ["cargo", "run"]
        here = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
        # Path to the Hertta submodule: control-center/hertta
        self._workdir = os.path.join(project_root, "hertta")
        self._stopped = False
        self.log_signal = log_signal
        self.finished_signal = finished_signal

    def start_hertta_server(self):
        self._stopped = False
        if not os.path.exists(self._workdir):
            self.log_signal.emit(f"Hertta Server path {self._workdir} not found")
            return False
        cf = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0  # Don't show console when frozen
        
        env = os.environ.copy()
        # Adjust level as you like: "error", "info", "debug", "trace"
        env.setdefault("RUST_LOG", "debug")
        
        try:
            self._process = subprocess.Popen(
                self._command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self._workdir,
                creationflags=cf,
                env=env,
                text=True,
                bufsize=1,
            )
        except OSError as e:
            self.log_signal.emit(f"[OSError] Hertta Server failed to start: {e}")
            return False

        sleep(0.3)
        if self._process.poll() is not None:
            # Process already exited → cargo failed
            self.log_signal.emit(
                f"Hertta Server exited immediately (code {self._process.returncode})"
            )
            return False
    
        threading.Thread(target=self._log_stdout, args=(self._process.stdout,), daemon=True).start()
        threading.Thread(target=self._log_stderr, args=(self._process.stderr,), daemon=True).start()
        threading.Thread(target=self._wait_until_ready, daemon=True).start()
        return True

    def shutdown(self):
        self._stopped = True
        if self._process is not None:
            self._process.terminate()

    def _log_stdout(self, stdout):
        for line in stdout:
            if line.strip():
                self.log_signal.emit(f"[HERTTA STDOUT] {line.strip()}")

    def _log_stderr(self, stderr):
        for line in stderr:
            if line.strip():
                self.log_signal.emit(f"[HERTTA STDERR] {line.strip()}")

    def _wait_until_ready(self, timeout_s: float = 600.0, poll_interval_s: float = 2.0):
        """
        Poll http://127.0.0.1:3030/health until it returns HTTP 200, or until timeout.
        """
        url = "http://127.0.0.1:3030/health"

        self.log_signal.emit(
            "Waiting for Hertta server to become ready (first build may take a while)..."
        )

        deadline = time() + timeout_s

        while not self._stopped and time() < deadline:

            if self._process is None:
                self.log_signal.emit("Hertta process handle missing")
                return

            if self._process.poll() is not None:
                self.log_signal.emit(
                    f"Hertta server process exited (code {self._process.returncode})"
                )
                return

            try:
                resp = requests.get(url, timeout=3.0)
                if resp.status_code == 200:
                    self.log_signal.emit("Hertta server started")
                    self.finished_signal.emit("Hertta server started")
                    return
            except requests.exceptions.RequestException:
                pass

            sleep(poll_interval_s)

        self.log_signal.emit("Timed out waiting for Hertta server to start")
        self.finished_signal.emit("Timed out waiting for Hertta server to start")


