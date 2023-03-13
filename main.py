import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import numpy as np
from polyfuzz import PolyFuzz


eth_base_url = "https://www.allrecipes.com/cuisine-a-z-6740455"

r = requests.get(eth_base_url).text

soup = BeautifulSoup(r, 'html.parser')

lis = soup.find_all("li", {"class": "comp link-list__item"})

link_dict = {}

for li in lis:
    print("\n\n")
    link_dict[li.a.text.strip("\n")] = li.a["href"]

def get_recipes(cuisine):

    cusisine_dict = {}

    req = requests.get(link_dict[cuisine]).text
    time.sleep(1)
    req = BeautifulSoup(req, 'html.parser')

    cards = req.find_all('a', {"class": "comp mntl-card-list-items mntl-document-card mntl-card card card--no-image"})

    for card in cards:
        name = list(card.find("span", {"class": "card__title"}).children)[0].text
        link = card['href']

        cusisine_dict[name] = link

    return cusisine_dict

def get_recipe_ing(recipe_link):

    req = requests.get(recipe_link).text
    req = BeautifulSoup(req, 'html.parser')

    ings = req.find_all('span', {"data-ingredient-name": "true"})
    ings = list(ings)
    ings = [e.text for e in ings]
    
    return ings

def save_dat_to_csv():

    to_pd_dict = {}

    all_cusi = list(link_dict.keys())

    # all_cusi = all_cusi[:20]

    for cusi in tqdm(all_cusi):
        to_pd_dict[cusi] = []

        ddic = get_recipes(cusi)

        for k, v in tqdm(ddic.items()):
            to_add = get_recipe_ing(v)
            time.sleep(1)
            for ele in to_add:
                to_pd_dict[cusi].append(ele)


    df = pd.DataFrame.from_dict(to_pd_dict, orient='index')
    df = df.transpose()

    df.to_csv('testBig.csv')

save_dat_to_csv()


