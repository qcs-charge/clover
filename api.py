"""
print(ping())

station_id = get_station()

print(station_id)

aruco_id = get_aruco(station_id)

print(aruco_id)

status = get_status(station_id)

print(status)
"""


import requests


TOKEN = 'INSECURE-does2-tjb1o-lo721-9pl3n'
API_LINK = f'http://qcs.pythonanywhere.com/api/flight/?token={TOKEN}'


def ping():
    return requests.get(f'{API_LINK}&request=ping').status_code == 200


def get_station():
    return requests.get(f'{API_LINK}&request=getStation').text


def get_aruco(station_id: int | str):
    return requests.get(f'{API_LINK}&request=getAruco&id={station_id}').text


def get_status(station_id: int | str):
    response = requests.get(f'{API_LINK}&request=getStatus&id={station_id}').text
    return {
        'opened': bool(int(response[0])),
        'done': bool(int(response[1])),
    }
