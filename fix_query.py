import requests
from pprint import pprint
import os


def get_place_name(input):
    key = os.environ["PLACES_KEY"]
    try:
        end_point = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype=" \
                    f"textquery&fields=name&key={key}"
        response = requests.get(url=end_point)
        return str(response.json()["candidates"][0]["name"]).replace(" ", "-")

    except IndexError:
        return input
