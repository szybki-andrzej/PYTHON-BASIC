import requests
from bs4 import BeautifulSoup
import json
import time
from threading import Thread
import concurrent.futures
import os


api_key = "2VHYpROswYZxDxqqOEgBjjO3hygNXnmGljVUJiIA"
apod_endpoint = 'https://api.nasa.gov/planetary/apod'
output_images = './output'


def get_apod_metadata_normal(start_date: str, end_date: str, api_key: str) -> list:
    url = apod_endpoint + '?api_key=' + api_key +\
          '&start_date=' + start_date + '&end_date=' + end_date

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').text
    metadata = [data['url'] for data in json.loads(soup) if data['url'].endswith('.jpg')]
    return metadata


def download_apod_images_normal(metadata: list):
    for image_url in metadata:
        img_data = requests.get(image_url).content
        with open(f'images/{image_url[38:-4]}.jpg', 'wb') as handler:
            handler.write(img_data)


def main_normal():
    metadata = get_apod_metadata_normal(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=api_key,
    )
    download_apod_images_normal(metadata=metadata)


def download_apod_images(image_url):
    img_data = requests.get(image_url).content
    with open(f'images/{image_url[38:-4]}.jpg', 'wb') as handler:
        handler.write(img_data)


def main():
    metadata = get_apod_metadata_normal(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=api_key,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
        ex.map(download_apod_images, metadata)


if __name__ == '__main__':
    if not os.path.exists('./images'):
        os.makedirs('./images')
    start_normal = time.time()
    main_normal()
    print(time.time() - start_normal)

    start = time.time()
    main()
    print(time.time() - start)
