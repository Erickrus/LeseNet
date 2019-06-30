import os
import sys
import hashlib
import time

from image_crawler import ImageCrawler
from image_downloader import ImageDownloader

SEP = '-' * 70 + '\n'
n_scroll = 2
engine = 'baidu'


def get_md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return  m.hexdigest()

def crawl(keyword, n_scroll, engine='baidu'):
    # ---------------------------------------------------
    # Basic settings for ImageCrawler and ImageDownloader
    # ---------------------------------------------------
    print(SEP + 'Basic settings for ImageCrawler and ImageDownloader\n' + SEP)

    keywordHash = get_md5(keyword)

    link_save_dir = os.path.join('../data/links', keywordHash)
    image_save_dir = os.path.join('../data/images', keywordHash)

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

    if len(sys.argv)<3:
        print("Usage: python3.x crawler.py startLine endLine")
        exit()
    startLine, endLine = int(sys.argv[1])-1, int(sys.argv[2])-1

    hierachy = os.path.join('../hierarchy', 'hierarchy.yml')
    f = open(hierachy, "r")
    lines = f.read().split("\n")
    f.close()
    for i in range(len(lines)):
        if startLine <= i and i<=endLine:
            keyword = lines[i]
            if len(keyword) > 6 and keyword[:6] == "   "*2 and not keyword.endswith("类"):
                keyword = keyword.strip()
                print("crawl: "+keyword)
                crawl(keyword, n_scroll, 'baidu')
                print("sleep: 10")
                time.sleep(10)

