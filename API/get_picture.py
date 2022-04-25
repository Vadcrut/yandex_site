import requests


def make_get(address):
    response = requests.get(
        f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json')
    if response:
        a = response.json()
        return a


def get_coords(address):
    a = make_get(address)
    return a['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']


def do(address='Кострома, ул.Сусанина 10', mashtab=(0.001, 0.001)):
    x, y = get_coords(address).split()
    map_request = f'http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={mashtab[0]},{mashtab[1]}&l=map&pt={x},{y},pm2dom'
    response = requests.get(map_request)
    map_file = "static/image/map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)