import faster_than_requests as requests
from bs4 import BeautifulSoup
from pprint import pprint

search_url = "https://www.centris.ca/en/properties~for-"
search_end = "?view=Thumbnail"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

link_head = "https://www.centris.ca"

image_link_tail = "t=pi&w=320&h=240&sm=c"


class SearchCentris:

    def search_centris(self, place_name, rent_sale):
        result = []
        search_endpoint = search_url + rent_sale + "~" + place_name + search_end
        response = requests.get(search_endpoint, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prices = (soup.find_all(name="div", class_="price"))
        addresses = (soup.find_all(name="span", class_="address"))
        urls = soup.find_all(class_="thumbnail")
        final_url = []
        final_img_url = []

        for url in urls:
            link = url.find(name="a")
            link = link_head + (str(link).split('"')[1])
            final_url.append(link)
            img_url = url.find(name="img")
            final_img_url.append(str(img_url).split('src="')[1].split('"')[0].split("amp")[0] + image_link_tail)
        for index in range(0, len(prices)):
            ans = {
                "price": str(prices[index].text).strip().split("$")[1].split('/')[0].split('+')[0].strip(),
                "address": str(addresses[index].text).strip(),
                "url": str(final_url[index]).strip(),
                "img_url": final_img_url[index]
            }

            result.append(ans)
            return result


