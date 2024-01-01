import time
import requests
from bs4 import BeautifulSoup as bs
import json

base_url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page="
number_of_pages = 2

one_w_brands = {"abarth", "ac", "aiways", "aixam", "alpina", "alpine", "anaig", "ariel", "audi", "austin", "autobianchi", "bellier", "benimar", "bentley", "bmw", "bollore", "bugatti", "buick", "burstner", "byd", "cadillac", "casalini", "caterham", "challenger", "chatenet", "chevrolet", "chrysler", "citroen", "cupra", "dacia", "daewoo", "daihatsu", "dallara", "dangel", "datsun", "devinci", "dfsk", "dodge", "donkervoort", "ds", "excalibur", "ferrari", "fiat", "fisker", "ford", "fuso", "glas", "gmc", "goupil", "hanroad", "hobby", "honda", "hotchkiss", "hummer", "hyundai", "imf", "ineos", "infiniti", "innocenti", "isuzu", "iveco", "jaguar", "jeep", "karma", "kia", "ktm", "lada", "lamborghini", "lancia", "leapmotor", "lexus", "ligier", "lincoln", "lotus", "man", "marcos", "maserati", "matra", "maybach", "mazda", "mclaren", "mega", "mercedes-amg", "mercedes", "mercury", "mg", "microcar", "microdrive", "minauto", "mini", "mitsubishi", "mlt", "morgan", "morris", "nash", "nissan", "nosmoke", "oldsmobile", "opale", "opel", "packard", "panhard", "panther", "peugeot", "pgo", "piaggio", "pilote", "plymouth", "polestar", "pontiac", "porsche", "radical", "ram", "rapido", "rcb", "renault", "rover", "saab", "santana", "seat", "secma", "seres", "simca", "skoda", "smart", "ssangyong", "subaru", "sunroller", "suzuki", "tesla", "toyota", "trabant", "triumph", "tvr", "vanderhall", "volkswagen", "volvo", "westfield", "wiesmann"}
two_w_brands = {"alfa romeo", "aston martin", "austin healey", "de lorean", "de tomaso", "gac gonow", "la strada", "land rover", "mia electric", "mpm motors", "rolls royce", "talbot simca"}
three_w_brands = {"lynk & co"}

two_w_model = {"punto evo", "e city", "e coupe", "b3 s", "v12 speedster", "v12 vantage", "v8 vantage", "vantage gt8", "a4 allroad", "a6 allroad", "coupe gt", "e-tron gt", "e-tron sportback", "rs q3", "rs q8", "tt rs", "flying spur", "turbo r", "serie 1", "serie 2", "serie 3", "serie 4", "serie 5", "serie 6", "serie 7", "serie 8", "atto 3", "coupe eldorado", "serie 62", "550 gransport", "550 granturismo", "550 trofeo", "super seven", "genesis 47", "ch 26", "ch 40", "ch 44", "ch 46", "bel air", "el camino", "k20 silverado", "k5 blazer", "master deluxe", "monte carlo", "300 c", "grand voyager", "pt cruiser", "c3 aircross", "c3 picasso", "c3 pluriel", "c4 aircross", "c4 cactus", "c4 picasso", "c4 spacetourer", "c5 aircross", "c5 x", "type c", "type h", "db 721", "ecocity 35", "ram 1500", "royal custom", "ds 3", "ds 4", "ds 5", "ds 7", "ds 9", "serie 4", "512 bb", "812 gts", "f8 spider", "f8 tributo", "sf90 spider", "sf90 stradale", "500 iii", "500 l", "500 x", "doblo cargo", "grande punto", "punto evo", "tipo ii", "32 roadster", "focus c-max", "grand c-max", "hot rod", "mustang mach-e", "tourneo connect", "tourneo courier", "tourneo custom", "transit connect", "transit courier", "transit custom", "gac gonow", "sierra pick-up", "trek 4", "trek 5", "h1 van", "ioniq 5", "ioniq 6", "santa fe", "serie n", "mk ii", "mk iv", "type e", "grand cherokee", "cee d", "discovery sport", "range rover", "mark viii", "town car", "1800 gt", "3200 gt", "57 berline", "xedos 9", "600 lt", "650 s", "675 lt", "fourgon 400", "plateau ridelles", "307 d", "classe a", "classe b", "classe c", "classe clc", "classe cls", "classe e", "classe g", "classe gl", "classe glk", "classe m", "classe r", "classe s", "classe slk", "classe t", "classe v", "classe x", "glc coupe", "gle coupe", "marco polo", "mb 100", "marvel r", "mg ehs", "mg zs", "mini cabriolet", "mini clubman", "mini coupe", "mini roadster", "3000 gt", "colt czc", "eclipse cross", "fuso canter", "pajero pinin", "pajero sport", "space star", "mehari e-story", "aero 8", "plus 4", "plus 6", "plus 8", "plus four", "plus six", "roadster v6", "super 3", "200 sx", "almera tino", "king cab", "nt400 cabstar", "pick up", "qashqai +2", "combo cargo", "combo life", "crossland x", "grandland x", "mokka x", "zafira life", "zafira tourer", "super eight", "pl 17", "508 rxh", "bipper tepee", "expert tepee", "partner tepee", "pacific 62px", "road runner", "polestar 2", "trans am", "trans sport", "carrera gt", "express van", "grand espace", "grand kangoo", "grand modus", "grand scenic", "kangoo express", "kangoo van", "s 170", "super 5", "vel satis", "silver cloud", "silver seraph", "silver shadow", "silver spirit", "serie 100", "serie 200", "altea freetrack", "seres 3", "actyon sports", "tivoli xlv", "wrx sti", "grand vitara", "sx4 s-cross", "wagon r+", "model 3", "model s", "model x", "model y", "aygo x", "carina e", "corolla cross", "corolla verso", "gr 86", "land cruiser", "model f", "proace city", "proace verso", "rav 4", "urban cruiser", "yaris cross", "tr 3", "tr 4", "tr 6", "golf plus", "golf sportsvan", "grand california", "id. buzz", "karman ghia", "lt combi", "new beetle", "passat cc", "tiguan allspace"}
three_w_model = {"e-tron s sportback", "rs e-tron gt", "benivan 105 up", "serie 3 gt", "serie 5 gt", "copa c500 bahia", "grand c4 picasso", "grand c4 spacetourer", "ds 3 crossback", "ds 4 crossback", "ds 7 crossback", "grand tourneo connect", "trek 5 +", "trek 5+ xl", "daily chassis cab", "pro cee d", "range rover evoque", "range rover sport", "range rover velar", "356 mader replica", "fun extr m", "dfsk ec 35", "land cruiser sw", "proace city verso", "tr 5 pi", "v40 cross country", "v60 cross country", "v90 cross country"}
four_w_model = {"serie 8 gran coupe"}

ads = []

for page in range(1, number_of_pages + 1):

    # Add page number at the end of the base URL
    url = f"{base_url}{page}"
    html = requests.get(url)

    # Code 200 means success
    if html.status_code == 200:
        soup = bs(html.text, 'html.parser')
        all_titles = soup.find_all('h2')
        raw = soup.find_all('div', class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
        index = 0

        # Check if we have the right number of data compared to the number of ads
        if len(all_titles)*4 == len(raw):

            for title in all_titles:
                ad = {}
                title = title.text.lower()

                # Divide the title string into words, using a space as a separator
                words = title.split()

                if words[0] in one_w_brands:
                    ad['Marque'] = words[0].title()

                    # Remove the brand from the rest of the title
                    rest = title.replace(f"{words[0]}", "").split()

                    if len(rest) > 1 and (f"{rest[0]} {rest[1]}" in two_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]}".title()
                    
                    elif len(rest) > 2 and (f"{rest[0]} {rest[1]} {rest[2]}" in three_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]}".title()

                    elif len(rest) > 3 and (f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}" in four_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}".title()
                    
                    else:
                        ad['Modele'] = f"{rest[0]}".title()

                elif (f"{words[0]} {words[1]}") in two_w_brands:
                    ad['Marque'] = f"{words[0]} {words[1]}".title()
                    rest = title.replace(f"{words[0]} {words[1]}", "").split()

                    if len(rest) > 1 and (f"{rest[0]} {rest[1]}" in two_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]}".title()
                    
                    elif len(rest) > 2 and (f"{rest[0]} {rest[1]} {rest[2]}" in three_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]}".title()

                    elif len(rest) > 3 and (f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}" in four_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}".title()
                    
                    else:
                        ad['Modele'] = f"{rest[0]}".title()

                elif (f"{words[0]} {words[1]} {words[2]}") in three_w_brands:
                    ad['Marque'] = f"{words[0]} {words[1]} {words[2]}".title()
                    rest = title.replace(f"{words[0]} {words[1]} {words[2]}", "").split()

                    if len(rest) > 1 and (f"{rest[0]} {rest[1]}" in two_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]}".title()
                    
                    elif len(rest) > 2 and (f"{rest[0]} {rest[1]} {rest[2]}" in three_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]}".title()

                    elif len(rest) > 3 and (f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}" in four_w_model):
                        ad['Modele'] = f"{rest[0]} {rest[1]} {rest[2]} {rest[3]}".title()
                    
                    else:
                        ad['Modele'] = f"{rest[0]}".title()

                else:
                    break

                clean_year = raw[index].text.replace(" ", "")
                ad['Annee'] = int(clean_year)
                clean_km = raw[index+1].text.replace(" ", "").replace("km", "")
                ad['Kilometrage'] = int(clean_km)
                ad['Transmission'] = raw[index+2].text.title()
                ad['Energie'] = raw[index+3].text.title()

                index += 4

                ads.append(ad)

    else:
        print("Request failed. Statut code :", html.status_code)

    time.sleep(2)

with open('ads.json', 'w', encoding="utf-8") as json_file:
    json.dump(ads, json_file, indent=4, ensure_ascii=False)