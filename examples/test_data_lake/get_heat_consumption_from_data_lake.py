"""Test query data from data lake."""

import requests
import json

token = ""   # ** Add token or this script won't work **

url = "https://api.centerdenmark.com/api/v1/dataset/1c16f324-235f-473b-84fd-8c6f69b38cb5/query"
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

# response.json():
# {
#     'pagination':
#         {
#             'totalRecords': 2487840, 'nextPage': 1, 'totalPages': 248784
#         },
#     'data':
#         [
#             {'return_temperature': 38.6, 'cluster_id': '99', 'heating_consumption': 0, 'volume_consumption': 0.019, 'flow_rate': 17.7, 'forward_temperature': 56.9, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 38.2, 'cluster_id': '98', 'heating_consumption': 1, 'volume_consumption': 0.029, 'flow_rate': 32.2, 'forward_temperature': 57.1, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 41.9, 'cluster_id': '97', 'heating_consumption': 0, 'volume_consumption': 0.023, 'flow_rate': 19, 'forward_temperature': 51.4, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 39, 'cluster_id': '96', 'heating_consumption': 1, 'volume_consumption': 0.038, 'flow_rate': 37.4, 'forward_temperature': 56, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 37.4, 'cluster_id': '95', 'heating_consumption': 0, 'volume_consumption': 0.029, 'flow_rate': 27.6, 'forward_temperature': 56.2, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 46, 'cluster_id': '94', 'heating_consumption': 0, 'volume_consumption': 0.049, 'flow_rate': 47, 'forward_temperature': 55.6, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 42.3, 'cluster_id': '93', 'heating_consumption': 0, 'volume_consumption': 0.032, 'flow_rate': 30.4, 'forward_temperature': 51.8, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 39.7, 'cluster_id': '92', 'heating_consumption': 0, 'volume_consumption': 0.03, 'flow_rate': 30.4, 'forward_temperature': 49.8, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 40, 'cluster_id': '91', 'heating_consumption': 1, 'volume_consumption': 0.024, 'flow_rate': 21.3, 'forward_temperature': 58.2, 'timestamp': '2022-08-31T23:00:00Z'},
#             {'return_temperature': 38.3, 'cluster_id': '90', 'heating_consumption': 1, 'volume_consumption': 0.027, 'flow_rate': 22.6, 'forward_temperature': 55.8, 'timestamp': '2022-08-31T23:00:00Z'}
#         ]
# }
