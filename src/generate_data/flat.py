import logging
import os
import random
import re
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from urllib.request import urlretrieve

from src.database.config import DB_ADMIN_PARAMS
from src.database.database import PostgresDB
from src.generate_data.config import MOSCOW_FLATS_URL, ERROR_504, IMG_PATH


class ParseFlats:
    def __init__(self, db: PostgresDB):
        self.__db = db
        self.__driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities().CHROME)
        self.__driver.implicitly_wait(10)
        self.__owner_ids = [landlord[0] for landlord in db.get_landlords()]

    def __del__(self):
        self.__driver.close()

    def get_html(self, url: str) -> str:
        self.__driver.get(url)
        return self.__driver.page_source

    def get_flats(self, url: str, page: int) -> list[dict[str, int | float | str]]:
        cur_url = f'{url}?Page={page}'
        html = self.get_html(cur_url)
        if self.__driver.title == ERROR_504:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        soup_flats = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a')
        flats = []
        for flat in soup_flats:
            photo_url = flat.find('div', class_='card-photo__imageWrapper___2tUR3').find_next('div').find('img')['src']
            photo = f'./img/{photo_url.split("/")[-1]}.jpg'
            urlretrieve(photo_url, f'../img/{photo_url.split("/")[-1]}.jpg')

            info_block = flat.find('div', class_='long-item-card__information___YXOtb').find('div')
            price = info_block.find('div', class_='long-item-card__informationHeaderLeft___3a-pz').find('span').text
            place = info_block.find('div', class_='long-item-card__informationHeaderRight___3bkKw').find('span').text

            info_block = flat.find('div', class_='long-item-card__informationMain___LnRL6')
            metro = info_block.find('div').find('span')
            if metro:
                metro = metro.text
            address = info_block.find('span', class_='long-item-card__address___PVI5p').text
            description = info_block.find('div', class_='long-item-card__descriptionLogoContainer___4HJmL').text

            try:
                flats.append({
                    'photo': photo,
                    'price': int(re.sub(r'[^\d]', '', price)),
                    'rooms': int(re.search(r'\d+(?=-)', place)[0]),
                    'square': float(re.search(r'\d+[.\s]\d*', place)[0]),
                    'floor': int(re.search(r'\d+(?=/)', place)[0]),
                    'max_floor': int(re.search(r'(?<=/)\d+', place)[0]),
                    'metro': metro,
                    'address': address,
                    'description': description,
                    'owner_id': random.choice(self.__owner_ids)
                })
            except TypeError:
                logging.error(f'Unable to get flat with title \'{place}\'')

        return flats

    def add_flats(self, url: str):
        cur_page = 1

        while True:
            flats = self.get_flats(url, cur_page)
            for flat in flats:
                print(flat['photo'])
                new_flat = self.__db.add_flat(flat['owner_id'], flat['price'], flat['rooms'], flat['square'],
                                              flat['address'], flat['metro'], flat['floor'], flat['max_floor'],
                                              flat['description'])
                self.__db.add_photo(new_flat[0], flat['photo'])
            cur_page += 1
            break


if __name__ == '__main__':
    sys.path.append('../')
    _db = PostgresDB(DB_ADMIN_PARAMS)

    parse = ParseFlats(_db)
    parse.add_flats(MOSCOW_FLATS_URL)
