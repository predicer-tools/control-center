import json
import requests


def post_request(url, limit, page, token, filters=None, list_filters=None, sort_list=None):
    """Posts a request to given url using the given parameters

    Args:
        url (str): URL
        limit (int): Number of records to request
        page (int): Page number
        token (str): Access token for the Danish data lake portal
        filters (list): List of filters
        list_filters (list): List of list filters (?!)
        sort_list (list): Sorters (?!)

    Returns:
        tuple: If the request succeeded, returns (True, <response as json>). If the request failed, returns (False, <error message>)
    """
    if not filters:
        filters = list()
    if not list_filters:
        list_filters = list()
    if not sort_list:
        sort_list = list()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    request_body = {
        "limit": limit,
        "page": page,
        "filters": filters,
        "listFilters": list_filters,
        "sortList": sort_list
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    if response.ok:
        return True, response.json()
    else:
        return False, str(response.status_code) + ": " + requests.status_codes._codes[response.status_code][0]


def post_request_hertta(url, query):
    """Posts a request to given url using the given query.

    Args:
        url (str): URL
        query (dict): Query to Hertta

    Returns:
        tuple: If the request succeeded, returns (True, <response as json>). If the request failed, returns (False, <error message>)
    """
    # curl -X POST -H "Content-Type: application/json" -d "{\"query\": \"{ settings { location { country } } }\"}" http://127.0.0.1:3030/graphql
    # curl -X POST -H "Content-Type: application/json" -d "{\"query\": \"{ jobStatus(jobId: 1) { state\nmessage } }\"}" http://127.0.0.1:3030/graphql
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(query))
    if response.ok:
        return True, response.json()
    else:
        return False, str(response.status_code) + ": " + requests.status_codes._codes[response.status_code][0]
