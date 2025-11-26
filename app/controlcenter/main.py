"""Starts Control Center app."""
import sys
import os
import pathlib
import tomllib
from PySide6.QtWidgets import QApplication
from controlcenter import ControlCenter
from config import TOKENFILE


def main():
    """Creates main window GUI and starts main event loop."""
    if not setup():
        return -1
    app = QApplication()
    app.setApplicationName("Control Center")
    window = ControlCenter()
    window.show()
    return_code = app.exec()
    return return_code


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


if __name__ == "__main__":
    sys.exit(main())
