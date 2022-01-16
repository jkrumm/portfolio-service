import requests

from project.server.main.utils.utils import os_get


def pushover(title, msg, priority, html):
    url = "https://api.pushover.net/1/messages.json"

    payload = {'token': os_get('PUSHOVER_TOKEN'),
               'user': os_get('PUSHOVER_USER'),
               'message': str(msg),
               'title': str(title),
               'priority': str(priority),
               'html': str(html)}

    requests.request("POST", url, data=payload)
