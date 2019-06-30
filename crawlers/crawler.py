import os
import sys

from image_crawler import ImageCrawler
from image_downloader import ImageDownloader

SEP = '-' * 70 + '\n'
n_scroll = 2
engine = 'baidu'

if len(sys.argv)<2:
    print("Usage: python3.x crawler.py keyword")
    exit()

keyword = sys.argv[1]


def crawl(keyword, n_scroll, engine='baidu'):
    # ---------------------------------------------------
    # Basic settings for ImageCrawler and ImageDownloader
    # ---------------------------------------------------
    print(SEP + 'Basic settings for ImageCrawler and ImageDownloader\n' + SEP)

    link_save_dir = os.path.join('../data/links', keyword)
    image_save_dir = os.path.join('../data/images', keyword)

    print('Keyword:', keyword)
    print('Number of scrolling:', n_scroll)
    print('Links saved in:', link_save_dir)
    print('Images saved in:', image_save_dir)
    print()

    # ----------------------------------
    # Save images' links by ImageCrawler
    # ----------------------------------

    print(SEP + "Save images' links by ImageCrawler\n" + SEP)

    # Search images in baidu
    links_name = '%s_links.csv' % engine

    ic = ImageCrawler(engine)
    ic.run(keyword, n_scroll)
    ic.save_links(link_save_dir, links_name)

    print("Images' links are saved in: " + link_save_dir + '\n')

    # ------------------------------
    # Save images by ImageDownloader
    # ------------------------------

    print(SEP + 'Save images by ImageDownloader\n' + SEP)

    # Download images to directory
    ider = ImageDownloader(link_save_dir)
    ider.run(image_save_dir)

    print('Images are saved in: ' + image_save_dir + '\n')

if __name__ == "__main__":
    crawl(keyword, n_scroll, 'baidu')

