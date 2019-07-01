import os
import sys
import hashlib
import time
import glob

from image_crawler import ImageCrawler
from image_downloader import ImageDownloader
from baiduyun import BaiduYun
from tqdm import *

SEP = '-' * 70 + '\n'
n_scroll = 3
engine = 'baidu'

# BaiduYun instance
bdy = None


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


def upload(keyword):
    print(SEP + 'Upload images to BaiduYun\n' + SEP)
    keywordHash = get_md5(keyword)

    # try to make dir
    bdy.mkdir("/data")
    bdy.mkdir("/data/images")
    bdy.mkdir("/data/links")
    bdy.mkdir(os.path.join("/data/images", keywordHash))
    bdy.mkdir(os.path.join("/data/links", keywordHash))

    for fileType in ["images", "links"]:
        print("uploading %s" % fileType)
        filenames = list(glob.glob("../data/%s/%s/*" % (fileType, keywordHash)))
   
        for i in tqdm(range(len(filenames)), ncols=70):
            filename = filenames[i]
            localFilename = os.path.abspath(filename)

            remoteDir = os.path.join("/data/%s" % fileType, keywordHash)
            bdy.upload(localFilename, remoteDir)
    print()

def check_parameter():
    # check parameter
    if len(sys.argv)<3:
        print("Usage: python3.x crawler.py startLineNum endLineNum")
        print("       lineNum starts from 1")
        exit()


def main():
    # get parameters
    startLine, endLine = int(sys.argv[1])-1, int(sys.argv[2])-1

    # loading hierachy
    hierachy = os.path.join('../hierarchy', 'hierarchy.yml')
    f = open(hierachy, "r" , encoding='utf-8')
    lines = f.read().split("\n")
    f.close()

    # loop through
    for i in range(len(lines)):
        if startLine <= i and i<=endLine:
            keyword = lines[i]
            if len(keyword) > 6 and keyword[:6] == "   "*2 and not keyword.endswith("类"):
                keyword = keyword.strip()
                print("crawl: "+keyword)
                crawl(keyword, n_scroll, 'baidu')
                upload(keyword)

                print("sleep: 10")
                time.sleep(10)

if __name__ == "__main__":
    check_parameter()
    bdy = BaiduYun()
    main()

