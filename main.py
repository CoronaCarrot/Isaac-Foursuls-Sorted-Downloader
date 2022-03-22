import os
import time
import uuid
import warnings
from shutil import make_archive

import requests as requests
from selenium import webdriver
from tqdm import tqdm
from termcolor import colored

warnings.filterwarnings("ignore", category=DeprecationWarning)

if not os.path.exists("./Downloads"):
    os.mkdir("./Downloads")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
try:
    print(colored("""
█████████""", "red") + colored("""  THE BINDING OF
""", "yellow") + colored("""   ███   █████   ██████    ██████    ██████                
   ███  ███          ███       ███  ███  ███ 
   ███   █████   ███████   ███████  ███     
   ███      ███ ███  ███  ███  ███  ███  ███
   ███  ██████   ████████  ████████  ██████
""", "red") + colored("""█████████""", "red") + """                CARD DOWNLOADER""" + colored("""        
                                  
https://github.com/CoronaCarrot/Isaac-Foursuls-Sorted-Downloader""", "white"))
    print(
        "\n\nPlease enter a search filter link from https://foursouls.com/card-search"
        "\nwith the cards you wish to download.\n")
    loop = True
    while loop:
        web = input("> ")
        if web.startswith("https://foursouls.com/card-search/?"):
            loop = False
            browser.get(web)
            browser.switch_to.window(browser.window_handles[0])
        else:
            print("Invalid link, please try again.")

    filename = str(uuid.uuid1())
    os.mkdir(f"./Downloads/{filename}")
except:
    exit()

cardcount = browser.find_element_by_xpath("//*[contains(text(), 'cards found')]")
pages = browser.find_elements_by_xpath("//*[contains(@class, 'page-numbers')]")
prev = 0
for page in pages:
    if int(page.text) > prev:
        prev = int(page.text)
cardcount = str(cardcount.text).strip(" CARDS FOUND")

print(f"Downloading {cardcount} cards from {prev} pages.")

cardhref = []

runc = 0
while prev > 0:

    if prev != 1:
        page = web.replace("card-search/", f"card-search/page/{prev}/")
    else:
        page = web
    browser.get(page)
    prev -= 1
    cards = browser.find_elements_by_xpath("//*[contains(@href, 'https://foursouls.com/cards/')]")
    for card in cards:
        href = card.get_attribute("href")
        if href != "https://foursouls.com/cards/":
            cardhref.append(href)
    time.sleep(1)

for card in tqdm(cardhref):
    browser.get(card)
    try:
        cards = browser.find_element_by_xpath("//*[contains(@alt, 'Treasure Card Back')]")
        type = "treasure"
    except:
        try:
            cards = browser.find_element_by_xpath("//*[contains(@alt, 'Soul Card Back')]")
            type = "soul"
        except:
            try:
                cards = browser.find_element_by_xpath("//*[contains(@alt, 'Character Card Back')]")
                type = "character"
            except:
                try:
                    cards = browser.find_element_by_xpath("//*[contains(@alt, 'Eternal Card Back')]")
                    type = "eternal"
                except:
                    try:
                        cards = browser.find_element_by_xpath("//*[contains(@alt, 'Loot Card Back')]")
                        type = "loot"
                    except:
                        try:
                            cards = browser.find_element_by_xpath("//*[contains(@alt, 'Monster Card Back')]")
                            type = "monster"
                        except:
                            try:
                                cards = browser.find_element_by_xpath("//*[contains(@alt, 'Room Card Back')]")
                                type = "room"
                            except:
                                type = "unsorted"
    cardimg = browser.find_element_by_xpath("//*[contains(@class, 'cardFront')]")
    url = cardimg.get_attribute("src")
    imgname = card.split("/")
    imgname = imgname[len(imgname) - 2]

    if not os.path.exists(f"Downloads/{filename}/{type}"):
        os.mkdir(f"Downloads/{filename}/{type}")
    with open(f'Downloads/{filename}/{type}/{imgname}.png', 'wb') as f:
        f.write(requests.get(url.replace("-308x420", "")).content)
        f.close()

make_archive(f'./Downloads/{filename}/Output', 'zip', root_dir=f'./Downloads/{filename}/')
