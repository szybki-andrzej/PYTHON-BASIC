import requests
from bs4 import BeautifulSoup
import json
import time
import concurrent.futures
import os


api_key = "2VHYpROswYZxDxqqOEgBjjO3hygNXnmGljVUJiIA"
apod_endpoint = 'https://api.nasa.gov/planetary/apod'
output_images = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    """Function that returns tab of the images' URLs."""

    url = apod_endpoint + '?api_key=' + api_key +\
          '&start_date=' + start_date + '&end_date=' + end_date

    page = requests.get(url)
    scrapped_page_content = BeautifulSoup(page.content, 'html.parser').text
    metadata = [data['url'] for data in json.loads(scrapped_page_content) if data['url'].endswith('.jpg')]

    return metadata


def download_apod_images_one_thread(metadata: list):
    """Function that download images and save them to files using one-thread methods."""

    for image_url in metadata:
        img_data = requests.get(image_url).content
        with open(f'images/{image_url[38:-4]}.jpg', 'wb') as handler:
            handler.write(img_data)


def download_apod_images_concurrent(image_url):
    """Function that download one image and save it to file useful for mapping in concurrent methods."""

    img_data = requests.get(image_url).content
    with open(f'images/{image_url[38:-4]}.jpg', 'wb') as handler:
        handler.write(img_data)


def main():

    if not os.path.exists('./images'):
        os.makedirs('./images')

    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=api_key,
    )

    # one-thread implementation
    start_one_thread = time.time()
    download_apod_images_one_thread(metadata=metadata)
    print(f'One-thread implementation time: {time.time() - start_one_thread}')

    # concurrent implementation
    start_concurrent = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
        ex.map(download_apod_images_concurrent, metadata)
    print(f'Concurrent implementation time: {time.time() - start_concurrent}')


if __name__ == '__main__':
    main()
