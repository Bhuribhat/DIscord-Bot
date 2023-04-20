import cv2
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


# https://dev.to/knassar702/steal-some-memes-with-python-lpe
def meme_stealer(page=None):
    if page == None: page = np.random.randint(1, 30)
    req = requests.get(f'https://imgflip.com/?page={page}').content
    soup = BeautifulSoup(req, "html.parser")
    ancher = soup.find_all('div', {'class': "base-unit clearfix"})

    # get all images in that page
    links = []
    for pt in ancher:
        image = pt.find('img', {'class': 'base-img'})
        if image:
            link = image['src'].replace(image['src'][0:2],'https://')
            links.append(link)

    # select 1 random image
    select = np.random.choice(links)
    r = requests.get(select)
    image = Image.open(BytesIO(r.content))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('.\\assets\\meme.png', image)


if __name__ == '__main__':
    meme_stealer()