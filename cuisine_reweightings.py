import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

eth_base_url = "https://www.allrecipes.com/cuisine-a-z-6740455"

r = requests.get(eth_base_url).text

soup = BeautifulSoup(r, 'html.parser')

lis = soup.find_all("li", {"class": "comp link-list__item"})

link_dict = {}

for li in lis:
    print("\n\n")
    link_dict[li.a.text.strip("\n")] = li.a["href"]


all_cuis = list(link_dict.keys())

def get_recipes(cuisine):

    cuissine_dict = {}

    req = requests.get(link_dict[cuisine]).text
    time.sleep(1)
    req = BeautifulSoup(req, 'html.parser')

    cards = req.find_all('a', {"class": "comp mntl-card-list-items mntl-document-card mntl-card card card--no-image"})

    for card in cards:
        name = list(card.find("span", {"class": "card__title"}).children)[0].text
        link = card['href']

        cuissine_dict[name] = link

    return cuissine_dict
cuis_pop_weights = {}
for cuis in all_cuis:

    cuis_pop_weights[cuis] = len(get_recipes(cuis))

    print(cuis)
    print(int(len(get_recipes(cuis))))
    print("\n")


df = pd.DataFrame.from_dict(cuis_pop_weights, orient='index')
print(df)
df.to_csv('pop_weights.csv')