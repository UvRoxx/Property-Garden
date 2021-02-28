from bs4 import BeautifulSoup
import requests
from pprint import pprint

import json

# url = "https://www.zumper.com/apartments-for-rent/montreal-qc"
# current method only queries for rent but can be modified for either


# For this site the enddpoint tail must contain the province code with a - to process the request
# eg montreal-qc
build_url = "https://www.zumper.com"

final_address = []
final_url = []
final_price = []
result = []

# headers = {'User-Agent': 'Mozilla/5.0'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class SearchZumper:
    def search_zumper(self, place_name, page_number):

        URL_ENDPOINT = "https://www.zumper.com/apartments-for-rent/"
        URL_ENDPOINT_TAIL = f"-qc?page={page_number}"

        url = URL_ENDPOINT + place_name + URL_ENDPOINT_TAIL
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        addresses = soup.find_all(class_="Listables_listItemContainer__2j0Fo")

        for address in addresses:
            final_address.append(address.find_all(name="a")[0].text)
            link = (str(address.find_all(name="a")).split('href="')[1]).split(' ')[0]
            link = build_url + link
            final_url.append(link)
            final_price.append(
                str(address).split('div class="ListItemDesktopView_priceAndViewing"')[0].split("$")[1].split('<')[0])
            pprint(address.find(name="img"))
        for index in range(0, len(final_price)):
            ans = {
                "price": str(final_price[index]),
                "address": str(final_address[index]),
                "url": str(final_url[index]),
                "img_url": "https://iravzdhanju.github.io/Image/logohouse.jpg"
            }
            if ans not in result:
                result.append(ans)

        return result
