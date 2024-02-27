import requests
import io
import os
from PIL import Image
from bs4 import BeautifulSoup as b
import re

def make_directory(path):
    # If dir not exists, it makes a new dir named as the path basename
    if not os.path.exists(path):
        os.mkdir(path)

def get_flags_url():
    # First we get our flags from this wikipedia's url
    wikiurl = 'https://es.wikipedia.org/wiki/Anexo:Países'
    flagswiki = requests.get(wikiurl).content

    # Using beautifulsoup to pull out our data using lxml parser
    soup = b(flagswiki,"lxml")
    flags = {}

    # Now we go through the data searching for each <tr> markup
    # Finding our image in <img> markup and getting a better image quality
    # And finallly saving our image url in a dict with its name as a key
    for country in soup.findAll("tr",{"bgcolor":"#efefef"}):
        url = country.find("img")
        img = 'https:' + url['src'].replace('50px','500px')
        name = re.sub("(.*\(|\).*)","",country.find('td').text.strip())
        indexsvg = img.rfind('.svg')
        img = img[:indexsvg] + img[indexsvg + len('.svg'):]
        flags[name] = img

    return flags

def save_images(path,flags_list):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'}

    # First we would look over each item on flags_list if it not exists it will save it on the flags_images dir
    for name in flags_list:
        img_path = os.path.join(path,name.replace('/',' ') + '.png')
        if os.path.exists(img_path):
            continue
        r = requests.get(flags_list[name],headers=headers)
        fil = io.BytesIO(r.content)
        img = Image.open(fil)
        img.save(img_path)
        print('Create and save Image for ' + name)

# if __name__ == '__main__':
#     cwd = os.getcwd()
#     target_path = os.path.join(cwd,'flags_images')
#     make_directory(target_path)
#     urls = get_flags_url()
#     save_images(target_path,urls)
