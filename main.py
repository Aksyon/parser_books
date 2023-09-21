import os.path
import requests
from bs4 import BeautifulSoup
import json
import csv


def get_data():
    url = 'https://api.litres.ru/foundation/api/search?limit=200&q=%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0&types=text_book&types=audiobook&types=podcast&types=podcast_episode'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 116.0.0.0 Safari / 537.36',
        'Access-Control-Allow-Headers': 'DNT, User - Agent, X - Requested - With, If - Modified - Since, Cache - Control, Vary, Content - Type, Range, Authorization, Accept, Session - Id, Client - Host, Client - Country - Name, Client - Country - Code, Client - City - Name, Ui - Language - Code, App - Id, Basket, Wishlist, Safemode - Enabled, Cache - User - Id - Enabled, Ui - Currency, Reset - Rate - Limit - API - Key, Accept - Version, X - Request - Id'
    }

    req = requests.get(url=url, headers=headers)

    if not os.path.exists('data'):
        os.mkdir('data')

    # with open('data/page.json', 'w', encoding='utf-8') as file:
    #     json.dump(req.json(), file, indent=4, ensure_ascii=False)

    with open('data/page.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)


    with open('data/books_available.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'заголовок',
                'ссылка на книгу',
                'ссылка на обложку',
                'цена',
                'авторы'
            )
        )

    data_list = []


    data = json_data['payload']['data']
    for item in data:
        if item['instance']['availability']==1:
            book_title = item['instance']['title']
            book_url = 'https://www.litres.ru'+item['instance']['url']
            book_cover_image = 'https://www.litres.ru'+item['instance']['cover_url']
            book_price = item['instance']['prices']['final_price']

            author = []

            for person in item['instance']['persons']:
                try:
                    book_author = person['full_name']
                    author_url = 'https://www.litres.ru'+person['url']
                except Exception:
                    continue

                author.append(
                    {
                        book_author:author_url
                    }
                )

            with open('data/books_available.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_url,
                        book_cover_image,
                        book_price,
                        author
                    )
                )
            print(f'файл books_available.csv дополнен')


def main():
    get_data()


if __name__ == '__main__':
    main()