# Elexia Control Center

[![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue.svg)](https://www.python.org/downloads/release/python-379/)

A desktop application for managing connections between Hertta, Predicer, InfluxDb, and Center Denmark's 
Data Portal.

## Prerequisites
- Python 3.11+
- InfluxDb
- Grafana
- InfluxDb access token
- Personal access token from Center Denmark's portal

## Installation

* cd to <repo-root>/app folder (the one containing pyproject.toml)

* Make a virtual environment


    python -m venv .venv
* Activate virtual environment


    .venv\Scripts\activate
* Install Python requirements


    pip install -e .


* Get access token from https://portal.centerdenmark.com/en-US/
* Create an InfluxDb token

The token is a string of 100+ characters.

* **Create a new file called `tokens.toml` into directory <repo-root>/app/controlcenter/**

The format of `tokens.toml` is

```text
datalake_token = "paste datalake token here inside the quotes"
influxdb_token = "paste influxdb token here inside the quotes"
```

** In case you don't have the influxDb token, set the second key to eg. `infuxdb_token = "abc"`

* Start the app from command prompt


    python main.py
