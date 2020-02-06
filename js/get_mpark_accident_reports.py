import requests
from bs4 import UnicodeDammit
from os import path
from random import shuffle
from time import sleep


def run():
    while True:
        try:
            with open('mpark_accident_links.txt', 'r') as f:
                lines = [x.strip() for x in f.readlines()]
                shuffle(lines)
                for url in lines:
                    page = requests.get(url)
                    dammit = UnicodeDammit(page.content)
                    page.encoding = dammit.original_encoding
                    car_id = url.split('=')[-1]
                    dst = path.join('mpark_accident_reports', f'{car_id}.html')
                    with open(dst, 'w') as writer:
                        writer.write(page.text)
        except Exception as e:
            print(str(e))
        finally:
            sleep(5)


if __name__ == '__main__':
    run()
