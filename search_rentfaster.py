from bs4 import BeautifulSoup
from pprint import pprint
import requests
url_head = "https://www.louer.com/"
url_tail = "+apartments+condos-for-rent/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def search_louer(place_name):
    place_name = place_name.lower()
    final_url = f"{url_head}{place_name}{url_tail}"
    response = requests.get(url=final_url, headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    print(soup.prettify())

search_louer("montreal")