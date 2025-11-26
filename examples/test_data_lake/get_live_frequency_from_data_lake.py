"""Test query data from data lake."""

import requests
import json

token = ""   # ** Add token or this script won't work **

url = "https://api.centerdenmark.com/api/v1/dataset/472ed84f-5378-4b12-8401-700e3451e3c3/query"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token,
}
request_body = {
  "limit": 10,
  "page": 0,
  "filters": [],
  "listFilters": [],
  "sortList": []
}

response = requests.post(url, headers=headers, data=json.dumps(request_body))

if response.ok:
    print(response.json())
else:
    print(str(response.status_code) + ": " + requests.status_codes._codes[response.status_code][0])

