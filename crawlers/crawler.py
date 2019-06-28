import os

from image_crawler import ImageCrawler
from image_downloader import ImageDownloader

SEP = '-' * 70 + '\n'

# ---------------------------------------------------
# Basic settings for ImageCrawler and ImageDownloader
# ---------------------------------------------------

print(SEP + 'Basic settings for ImageCrawler and ImageDownloader\n' + SEP)

n_scroll = 5
keyword = 'panda'

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
engine = 'baidu'
baidu_links_name = 'baidu_links.csv'

baidu_ic = ImageCrawler(engine)
baidu_ic.run(keyword, n_scroll)
baidu_ic.save_links(link_save_dir, baidu_links_name)

# Search images in bing
engine = 'bing'
bing_links_name = 'bing_links.csv'

bing_ic = ImageCrawler(engine)
bing_ic.run(keyword, n_scroll)
bing_ic.save_links(link_save_dir, bing_links_name)

# Search images in google
engine = 'google'
google_links_name = 'google_links.csv'

google_ic = ImageCrawler(engine)
google_ic.run(keyword, n_scroll)
google_ic.save_links(link_save_dir, google_links_name)


print("Images' links are saved in: " + link_save_dir + '\n')


# ------------------------------
# Save images by ImageDownloader
# ------------------------------

print(SEP + 'Save images by ImageDownloader\n' + SEP)

# Download images to directory
ider = ImageDownloader(link_save_dir)
ider.run(image_save_dir)

print('Images are saved in: ' + image_save_dir + '\n')
