"""Test query data from data lake."""

import requests
import json

token = ""  # ** Add token or this script won't work **

url = "https://api.centerdenmark.com/api/v1/dataset/106cf0f7-b39d-4daf-a457-488956fa61b0/query"

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
#             'totalRecords': 284, 'nextPage': 1, 'totalPages': 29
#         },
#     'data':
#         [
#             {'cluster_id': '12', 'station_id': 'e22f3e0d'},
#             {'cluster_id': '15', 'station_id': 'e6a94c27'},
#             {'cluster_id': '3', 'station_id': '3a8b14af'},
#             {'cluster_id': '10', 'station_id': '3a8b14af'},
#             {'cluster_id': '1', 'station_id': 'e22f3e0d'},
#             {'cluster_id': '11', 'station_id': 'e6a94c27'},
#             {'cluster_id': '16', 'station_id': 'e6a94c27'},
#             {'cluster_id': '4', 'station_id': 'e22f3e0d'},
#             {'cluster_id': '9', 'station_id': 'e22f3e0d'},
#             {'cluster_id': '13', 'station_id': 'e6a94c27'}
#         ]
# }
