import os
import ssl
import json
import time
import pandas as pd

from tqdm import *
from selenium import webdriver


class ImageCrawler(object):

    SETTINGS = {
        'baidu': {'url': 'https://image.baidu.com/search/index?tn=baiduimage&word=${KEYWORD}',
                  'see_more': None,
                  'xpath': '//div[@id="imgContainer"]//li[@class="imgitem"]',
                  'item': 'data-objurl',
                  'item_attr': None},
        'bing': {'url': 'https://www.bing.com/images/search?q=${KEYWORD}',
                 'see_more': '//div[@class="mm_seemore"]/a[@class="btn_seemore"]',
                 'xpath': '//div[@class="imgpt"]/a[@class="iusc"]',
                 'item': 'm',
                 'item_attr': 'murl'},
        'google': {'url': 'https://www.google.com.hk/search?q=${KEYWORD}&source=lnms&tbm=isch',
                   'see_more': '//*[@id="smb"]',
                   'xpath': '//div[contains(@class,"rg_meta")]',
                   'item': 'innerHTML',
                   'item_attr': 'ou'}
    }

    def __init__(self, engine='google'):

        self.engine = engine
        self.url = self.SETTINGS[engine]['url']
        self.see_more = self.SETTINGS[engine]['see_more']
        self.xpath = self.SETTINGS[engine]['xpath']
        self.item = self.SETTINGS[engine]['item']
        self.item_attr = self.SETTINGS[engine]['item_attr']

        self.image_links = set()
        self._init_ssl()
        return

    def run(self, keyword, n_scroll):

        self.n_scroll = n_scroll

        self.keyword = keyword
        print('Searching keyword: ', keyword)
        print('Searching engine: ', self.engine)
        self._generate_links()

        print()
        return

    def save_links(self, save_dir, file_name):

        self._create_dir(save_dir)

        links_file = os.path.join(save_dir, file_name)
        links_df = pd.DataFrame(data=list(self.image_links),
                                columns=['links'])

        links_df.to_csv(links_file, index=False)
        return

    def _init_ssl(self):
        ssl._create_default_https_context = \
            ssl._create_unverified_context()

    def _generate_links(self):

        browser_driver = webdriver.Chrome()
        browser_driver.get(self.url.replace('${KEYWORD}', self.keyword))

        for _ in tqdm(range(self.n_scroll), ncols=70):
            browser_driver.execute_script('window.scrollBy(0, 1000000)')
            time.sleep(1)

            if self.see_more is not None:
                try:
                    browser_driver.find_element_by_xpath(self.see_more).click()
                except Exception as e:
                    print('Error:', str(e))

        image_blocks = browser_driver.find_elements_by_xpath(self.xpath)
        for image_block in image_blocks:
            image_link = image_block.get_attribute(self.item)

            if self.item_attr is not None:
                try:
                    image_link = json.loads(image_link)[self.item_attr]
                except Exception as e:
                    print('Error:', str(e))

            self.image_links.add(image_link)

        browser_driver.quit()
        return

    def _create_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
