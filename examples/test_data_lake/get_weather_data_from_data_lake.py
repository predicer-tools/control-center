"""Test query data from data lake."""

import requests
import json

token = ""   # ** Add token or this script won't work **

url = "https://api.centerdenmark.com/api/v1/dataset/9224b1fe-d45f-4150-b326-5d51fd2b72cd/query"
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

