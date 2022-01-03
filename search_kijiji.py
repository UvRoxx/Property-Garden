from bs4 import BeautifulSoup
import faster_than_requests as requests
from fuzzywuzzy import process
from pprint import pprint


class SearchKijiji():
    def search_kijiji(self, place_name, page_number):
        # Data Building and Storing Variables
        kijiji_dict = {

            'ahuntsic': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/ahuntsic/page-1/k0c37l1700281?sort=relevancyDesc&radius=1000.0&address=Montréal%2C+QC&ll=45.501689,-73.567256&rb=true',
            'Anjou': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/anjou/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Beaconsfield': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/beaconsfield/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Côte-St-Luc': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/côte-st-luc/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Hampstead': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/hampstead/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Montréal-Ouest': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/montréal-ouest/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Côte-des-Neiges': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/côte-des-neiges/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Notre-Dame-de-Grâce': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-1/notre-dame-de-grâce/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Dollard-Des-Ormeaux': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-1/dollard-des-ormeaux/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Dorval': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/dorval/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Griffintown': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/griffintown%27/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Kirkland': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/kirkland/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'L''Ile Des Soeurs': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/l%27ile-des-soeurs/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'L''île-Bizard ': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/l%27île-bizard/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Sainte-Geneviève': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/sainte-geneviève/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'LaSalle': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/lasalle/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Lachine': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/lachine/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Le Plateau-Mont-Royal': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/le-plateau-mont-royal/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Le Sud-Ouest': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/le-sud-ouest/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Mercier': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/mercier/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Hochelaga': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/hochelaga/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Maisonneuve': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/maisonneuve/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Mont-Royal': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/mont-royal/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Montréal-Nord': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/montréal-nord/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Outremont': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/outremont/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Pierrefonds': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/pierrefonds/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Roxboro': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/roxboro/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'La Petite Patrie': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/la-petite-patrie/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'saint laurent': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/saint-laurent/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Saint-Léonard': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/saint-léonard/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Senneville': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/senneville/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Verdun': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/verdun/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Ville-Marie': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/ville-marie/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Villeray': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/villeray/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'St-Michel': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/st-michel/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Parc-Extension': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/parc-extension/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
            'Westmount': 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/westmount/page-1/k0c37l1700281?rb=true&ll=45.501689%2C-73.567256&address=Montréal%2C+QC&sort=relevancyDesc&radius=1000.0',
        }

        result = []
        options = []
        for key in kijiji_dict:
            options.append(key)

        query = process.extractOne(place_name, options)

        url_split = kijiji_dict[query[0]].split("page-1/")
        url_endpoint_head = url_split[0]
        url_endpoint_mid = f"page-{page_number}/"
        url_endpoint_tail = url_split[1]
        endpoint_url = url_endpoint_head + url_endpoint_mid + url_endpoint_tail

        print(endpoint_url)

        url_head = "https://www.kijiji.ca"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(url=endpoint_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        addresses = soup.find_all(class_="search-item")
        for item in addresses:
            # Adding Address here
            add = (item.find_all(class_="intersection"))
            try:
                final_addresses = (f"{add[0].text}-{add[1].text}")
            except IndexError:
                final_addresses = ("No address registered")
            # Adding and Filtering The Price data here
            price = ("".join(map(str, (
                [ele.replace("xa0", '').replace('\xa0', '') for ele in
                 (str(item.find(class_="price").text).strip())])))).split(",")[0]
            final_prices = (price)

            # Adding Image URL Here
            image_urls = str(item.find(class_="image").find(name="img")).split('src="')[1].split('"')[0]
            final_image_url = (image_urls)

            # Adding Listing URL Here
            link = item.find_all(class_="title", name="a")
            url = url_head + str(link).split('href="')[1].split('"')[0]
            final_urls = (url)
            ans = {
                "price": final_prices,
                "address": final_addresses,
                "url": final_urls,
                "img_url": final_image_url
            }
            result.append(ans)

        return result
