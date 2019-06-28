import os
import pandas as pd
import urllib.error
import urllib.request

from tqdm import *
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from user_agent import generate_user_agent


class ImageDownloader(object):

    def __init__(self, links_dir):

        self.unique_links = []
        for link_file in os.listdir(links_dir):
            link_file_path = os.path.join(links_dir, link_file)
            link_df = pd.read_csv(link_file_path , header=0 , encoding='utf-8')

            if(  len(link_df.columns.tolist()) != 5 ):continue

            infos = link_df.values.tolist()
            if(len(infos)>0):
                self.unique_links += infos

        # self.unique_links = list(set(self.unique_links))
        return

    def run(self, save_dir):

        self.save_dir = save_dir
        self._download_images()

        print()
        return

    def _download_images(self):

        self._create_dir(self.save_dir)

        count = 0
        headers = {}

        for link in tqdm(self.unique_links, ncols=70):
            try:
                num = link[0]
                engine = link[1]
                kw = link[2]
                img_file_name = '%s_%s_%s' %(engine, kw , num)
                url = link[4]
                parse = urlparse(url)
                ref = parse.scheme + '://' + parse.hostname
                ua = generate_user_agent()
                headers['User-Agent'] = ua
                headers['referer'] = ref

                req = urllib.request.Request(url.strip(), headers=headers)
                response = urllib.request.urlopen(req, timeout=5)

                data = response.read()
                image = Image.open(BytesIO(data)).convert('RGB')

                ext = url.split('.')[-1]
                if('?' in ext):
                    pos = ext.find('?')
                    ext = ext[:pos]
                image_name = '{}.{}'.format(img_file_name, ext)
                image_path = os.path.join(self.save_dir, image_name)
                # print(image_path)
                image.save(image_path)

                count += 1

            # handle exceptions
            except urllib.error.URLError as e:
                continue
            except urllib.error.HTTPError as e:
                continue
            except Exception as e:
                continue

    def _create_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
