from bs4 import BeautifulSoup
import faster_than_requests as requests
from fuzzywuzzy import process
from pprint import pprint


class SearchDupropio():
    def search_dupropio(self, place_name,page_number):

        dupro_dict = {
            'Ahuntsic ': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1893&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Anjou': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=16&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Beaconsfield': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=62&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Baie-D''Urfé': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=62&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Côte-St-Luc': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1884&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Hampstead': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1884&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Montréal-Ouest': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1884&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Côte-des-Neiges': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1883&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Notre-Dame-de-Grâce': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1883&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Dollard-Des-Ormeaux': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=254&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Dorval / L''Île Dorval': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=256&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Griffintown': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=24619&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Kirkland': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=409&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'L''Ile Des Soeurs': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1863&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'L''île-Bizard ': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=381&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Sainte-Geneviève': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=381&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'LaSalle': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=596&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Lachine': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=574&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Le Plateau-Mont-Royal': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1887&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Le Sud-Ouest': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1916&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Mercier': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1897&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Hochelaga': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1897&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Maisonneuve': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1897&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Mont-Royal': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1029&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Montréal-Nord': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=732&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Outremont': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=809&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Pierrefonds': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=834&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Roxboro': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=834&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Pointe-Aux-Trembles': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=850&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Montréal-Est': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=850&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Pointe-Claire': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=853&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Rivière des Prairies': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1888&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Rosemont ': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1889&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'La Petite Patrie': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1889&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Saint-Laurent': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1423&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Saint-Léonard': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1433&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Senneville': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=972&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Ste-Anne-De-Bellevue': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1594&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Verdun': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1069&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Ville-Marie': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1885&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Villeray': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1892&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'St-Michel ': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1892&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Parc-Extension': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1892&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Westmount': 'https://duproprio.com/en/rental/search/list?search=true&cities%5B0%5D=1096&is_rental=1&parent=1&pageNumber=1&sort=-published_at',
            'Laval': "https://duproprio.com/en/rental/search/list?search=true&regions%5B0%5D=13&is_rental=1&parent=1&pageNumber=1&sort=-published_at"
        }

        result = []
        options = []
        for key in dupro_dict:
            options.append(key)

        query = process.extractOne(place_name, options)

        url_split = dupro_dict[query[0]].split("pageNumber=1")
        url_head = url_split[0]
        url_mid  = f"pageNumber={page_number}"
        url_tail = url_split[1]
        url_endpoint=url_head+url_mid+url_tail
        pprint(url_endpoint)
        response = requests.get(url_endpoint)

        print(query)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = soup.find_all(class_="search-results-listings-list__item-description__price")
        addresses = soup.find_all(
            class_="search-results-listings-list__item-description__item search-results-listings-list__item-description__address")
        urls = soup.find_all(class_="search-results-listings-list__item")
        for index in range(0, len(prices)):
            try:
                final_price = str(prices[index].text).split(" ")[0].split("$")[1]
            except IndexError:
                final_price = str(prices[index].text).split('$')[0]
            final_address = str(addresses[index].text).strip()
            url_final = (urls[index].find(name="a"))
            try:
                page_url = str(url_final).split('href="')[1].split('"')[0]
            except IndexError:
                page_url = str(url_final).split('href="')[0]
            try:
                img_url = str(url_final).split('src="')[1].split('"')[0]
                if img_url.split("/")[1].split("/")[0] == "filesystem":
                    img_url = "https://iravzdhanju.github.io/Image/logohouse.jpg"
            except IndexError:
                img_url = str(url_final).split('src="')[0]

            ans = {
                "price": final_price,
                "address": final_address,
                "url": page_url,
                "img_url": img_url}
            result.append(ans)

        return result

