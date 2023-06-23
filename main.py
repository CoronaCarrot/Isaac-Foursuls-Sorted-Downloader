import os
import time
import uuid
import warnings
from shutil import make_archive

import requests as requests
from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.common.by import By
from termcolor import colored

# Added to ignore Deprecation Warnings because I can't be bothered to switch to new system
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Checks if the Downloads folder exists
if not os.path.exists("./Downloads"):
    os.mkdir("./Downloads")

# Sets the user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# Defines options for the headless Chrome browser
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
#options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

try:
    # CLI Title
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
        # Await valid link input
        web = input("> ")
        if web.startswith("https://foursouls.com/card-search/?"):
            loop = False
            browser.get(web)
            browser.switch_to.window(browser.window_handles[0])
        else:
            print("Invalid link, please try again.")

    # generates a download file for the current download
    filename = str(uuid.uuid1())
    os.mkdir(f"./Downloads/{filename}")
except:
    exit()

# Finds the card count
cardcount = browser.find_element(By.XPATH, "//*[contains(text(), 'cards found')]")

# gets page amount
pages = browser.find_elements(By.XPATH, "//*[contains(@class, 'page-numbers')]")
prev = 0

# gets a list of all card links within those pages
for page in pages:
    if int(page.text) > prev:
        prev = int(page.text)
cardcount = str(cardcount.text).strip(" CARDS FOUND")

print(f"\nFound {cardcount} cards. beginning download...\n")

cardhref = []

runc = 0
while prev > 0:
    print("Scanning Results... {} Pages scanned...".format(runc))

    if prev != 1:
        page = web.replace("card-search/", f"card-search/page/{prev}/")
    else:
        page = web
    browser.get(page)
    prev -= 1
    cards = browser.find_elements(By.XPATH, "//*[contains(@href, 'https://foursouls.com/cards/')]")
    for card in cards:
        href = card.get_attribute("href")
        if href != "https://foursouls.com/cards/":
            cardhref.append(href)

    runc += 1
    time.sleep(1)

# runs through the full list of cards to download
for card in tqdm(cardhref, bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt} [Est. {remaining}]"):
    browser.get(card)
    try:
        cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Treasure Card Back')]")
        type = "treasure"
    except:
        try:
            cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Soul Card Back')]")
            type = "soul"
        except:
            try:
                cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Character Card Back')]")
                type = "character"
            except:
                try:
                    cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Eternal Card Back')]")
                    type = "eternal"
                except:
                    try:
                        cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Loot Card Back')]")
                        type = "loot"
                    except:
                        try:
                            cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Monster Card Back')]")
                            type = "monster"
                        except:
                            try:
                                cards = browser.find_element(By.XPATH, "//*[contains(@alt, 'Room Card Back')]")
                                type = "room"
                            except:
                                type = "unsorted"
    cardimg = browser.find_element(By.XPATH, "//*[contains(@class, 'cardFront')]")
    url = cardimg.get_attribute("src")
    imgname = card.split("/")
    imgname = imgname[len(imgname) - 2]

    # checks if the category exists, if not it creates it
    if not os.path.exists(f"Downloads/{filename}/{type}"):
        os.mkdir(f"Downloads/{filename}/{type}")
    # saves card to folder
    with open(f'Downloads/{filename}/{type}/{imgname}.png', 'wb') as f:
        f.write(requests.get(url.replace("-308x420", "")).content)
        f.close()

# zips all cards into an archive
print("\nDownload complete. Zipping files...")
make_archive(f'./Downloads/{filename}/Output', 'zip', root_dir=f'./Downloads/{filename}')
