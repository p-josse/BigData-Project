import time
import json
import requests
from bs4 import BeautifulSoup as bs

def make_request(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Request Error:", err)
    return None

def extract_car_info(title, raw_data):
    ad = {'Marque': None, 'Modele': None, 'Annee': None, 'Kilometrage': None, 'Transmission': None, 'Energie': None}

    words = title.lower().split()

    for brand_set, model_set in [(one_w_brands, two_w_model), (two_w_brands, three_w_model), (three_w_brands, None)]:
        brand_key = ' '.join(words[:len(brand_set)])
        if brand_key in brand_set:
            ad['Marque'] = brand_key.title()
            rest = title.replace(brand_key, '').split()
            model_key = ' '.join(rest[:4]) if model_set else rest[0]
            ad['Modele'] = model_key.title() if model_set and model_key in model_set else rest[0].title()
            break

    ad['Annee'] = int(raw_data[0].text.replace(" ", ""))
    ad['Kilometrage'] = int(raw_data[1].text.replace(" ", "").replace("km", ""))
    ad['Transmission'] = raw_data[2].text.title()
    ad['Energie'] = raw_data[3].text.title()

    return ad

base_url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page="
number_of_pages = 2

one_w_brands = {"abarth", "ac", "aiways", "aixam", ...}
two_w_brands = {"alfa romeo", "aston martin", ...}
three_w_brands = {"lynk & co"}
two_w_model = {"punto evo", "e city", ...}
three_w_model = {"e-tron s sportback", "rs e-tron gt", ...}
four_w_model = {"serie 8 gran coupe"}

ads = []
session = requests.Session()

for page in range(1, number_of_pages + 1):
    url = f"{base_url}{page}"
    html_content = make_request(url)

    if html_content:
        soup = bs(html_content, 'html.parser')
        all_titles = soup.find_all('h2')
        raw_data = soup.find_all('div', class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')

        if len(all_titles) * 4 == len(raw_data):
            for title, raw in zip(all_titles, [raw_data[i:i+4] for i in range(0, len(raw_data), 4)]):
                ad = extract_car_info(title.text, raw)
                ads.append(ad)
    else:
        print("Request failed for page", page)

    time.sleep(2)

session.close()

with open('ads.json', 'w', encoding="utf-8") as json_file:
    json.dump(ads, json_file, indent=4, ensure_ascii=False)
