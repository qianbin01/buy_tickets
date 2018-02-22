from urllib.parse import quote

stations = {}


def init_doc():
    with open('station_name.txt', 'r') as f:
        locations = f.readlines()
        for loc in locations:
            if loc:
                stations[loc.split(' ')[0]] = quote(','.join([i.strip() for i in loc.split(' ')]))


init_doc()


def get_stations():
    return stations
