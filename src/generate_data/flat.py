import logging
import os
import random
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from urllib.request import urlretrieve
from src.bot.config import IMG_PATH
from src.database.database import BaseDatabase
from src.generate_data.config import ERROR_504
from src.model.flat import Flat
from src.repository.flat import FlatRepository
from src.repository.landlord import LandlordRepository


class ParserFlats:
    def __init__(self, db: BaseDatabase):
        self.__landlord_repo = LandlordRepository(db)
        self.__flat_repo = FlatRepository(db)
        self.__driver = webdriver.Chrome(desired_capabilities=DesiredCapabilities().CHROME)
        self.__driver.implicitly_wait(10)
        self.__owner_ids = [landlord.id for landlord in self.__landlord_repo.get_landlords()]

    def __del__(self):
        self.__driver.close()

    def get_html(self, url: str) -> str:
        self.__driver.get(url)
        return self.__driver.page_source

    def get_flats(self, url: str, page: int) -> list[tuple[Flat, str]]:
        cur_url = f'{url}?Page={page}'
        html = self.get_html(cur_url)
        if self.__driver.title == ERROR_504:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        soup_flats = soup.find('div', class_='search-results__itemCardList___RdWje').find_all('a')
        flats: list[tuple[Flat, str]] = []
        for flat in soup_flats:
            photo_url = flat.find('div', class_='card-photo__imageWrapper___2tUR3').find_next('div').find('img')['src']
            photo = os.path.join(IMG_PATH, f'{photo_url.split("/")[-1]}.jpg')
            urlretrieve(photo_url, photo)

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
                flats.append((
                    Flat(
                        flat_id=-1,
                        owner_id=random.choice(self.__owner_ids),
                        price=int(re.sub(r'[^\d]', '', price)),
                        rooms=int(re.search(r'\d+(?=-)', place)[0]),
                        square=float(re.search(r'\d+[.\s]\d*', place)[0]),
                        address=address,
                        metro=metro,
                        floor=int(re.search(r'\d+(?=/)', place)[0]),
                        max_floor=int(re.search(r'(?<=/)\d+', place)[0]),
                        description=description
                    ),
                    photo
                ))
            except TypeError:
                logging.debug(f'Unable to get flat with title \'{place}\'')

        return flats

    def add_flats(self, url: str, n: int = 100):
        if n <= 0:
            return

        cur_page = 1
        count_flats = 0
        parsing = True

        while parsing:
            logging.info(f'Parsing page {cur_page}...')
            flats = self.get_flats(url, cur_page)
            parsing = bool(flats)

            for flat in flats:
                parsing = count_flats < n
                if not parsing:
                    break

                new_flat = self.__flat_repo.add_flat(flat[0])
                self.__flat_repo.add_photo(new_flat.id, flat[1])
                count_flats += 1

            cur_page += 1
