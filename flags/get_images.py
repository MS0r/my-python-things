import requests
import io
import os
from PIL import Image
from bs4 import BeautifulSoup as b
import re

cwd = os.getcwd()

def make_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_flags_url():
    wikiurl = 'https://es.wikipedia.org/wiki/Anexo:Países'
    flagswiki = requests.get(wikiurl).content
    soup = b(flagswiki,"lxml")
    flags = {}

    for country in soup.findAll("tr",{"bgcolor":"#efefef"}):
        url = country.find("img")
        name = re.sub("(.*\(|\).*)","",country.find('td').text.strip())
        img = 'https:' + url['src'].replace('50px','500px')
        indexsvg = img.rfind('.svg')
        img = img[:indexsvg] + img[indexsvg + len('.svg'):]
        flags[name] = img

    return flags

def save_images(path,flags_list):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'}
    for name in flags_list:
        img_path = os.path.join(path,name.replace('/',' ') + '.png')
        if os.path.exists(img_path):
            continue
        r = requests.get(flags_list[name],headers=headers)
        fil = io.BytesIO(r.content)
        img = Image.open(fil)
        img.save(img_path)
        print('Create and save Image for ' + name)

if __name__ == '__main__':
    target_path = os.path.join(cwd,'flags_images')
    make_directory(target_path)
    urls = get_flags_url()
    save_images(target_path,urls)
