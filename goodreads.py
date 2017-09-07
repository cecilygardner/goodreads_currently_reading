import json
from pprint import pprint
import random
import xml.etree.ElementTree as ET

import asana
import requests


def read_config():
    with open('config.json') as config_fobj:
        return json.load(config_fobj)


def grab_currently_reading(config):
    params = {
        "id": config['user_id'],
        "shelf": "currently-reading",
        "key": config['key'],
        "v": 2
    }

    response_1 = requests.get(
        "https://www.goodreads.com/review/list", params=params)

    root_1 = ET.fromstring(response_1.text.encode("utf-8"))
    
    print("Grabbing currently reading shelf")
    return root_1


def parse_currently_reading(root_1):

    currently_reading = []

    for book in root_1.iter('book'):
        book_dict = {child.tag: child.text for child in book}
        authors = [author_element.text for author_element in book.findall(
            'authors/author/name')]
        book_dict['author_list'] = authors
        currently_reading.append(book_dict)

    pprint(currently_reading)
    return currently_reading


def grab_books(config):
    params = {
        "id": config['user_id'],
        "shelf": "to-read",
        "key": config['key'],
        "v": 2
    }

    response = requests.get(
        "https://www.goodreads.com/review/list", params=params)

    root = ET.fromstring(response.text.encode("utf-8"))
    
    print("Grabbing to-read shelf") 
    return root


def parse_books(config, root, currently_reading):

    books = []

    for book in root.iter('book'):
        book_dict = {child.tag: child.text for child in book}
        books.append(book_dict)

    ideal_books_to_read = config['ideal_books_reading']
    num_recs = ideal_books_to_read - len(currently_reading)
    if num_recs < 1:
        if num_recs is 0:
            print("You have all the books you need!")
        else:
            print("You're reading too many books!")
    else:
        if num_recs is 1:
            print("You need 1 book recomendation")

        else:
            print("You need {} book recomendations".format(num_recs))

    for i in range(num_recs):
        single_book = random.choice(books)
        isbn = single_book['isbn']
        name = "Recommendation: {}".format(single_book['title'])
        description = (single_book['description']).replace('<br />', '')
        if single_book['num_pages'] is not None:
            pages = single_book['num_pages']
        link = single_book['link']
        image = single_book['image_url']
        book_deets = (
            u"{}\n\n<b>ISBN</b>: {}\n\n<b>Goodreads URL:</b> {}".format(
                description, isbn, link))
        params = {
            'workspace': config['workspace_id'],
            'projects': [config['project_id']],
            'name': name,
            'html_notes': book_deets,
            'assignee': "cecilygardner@asana.com"
        }
        asana_client = asana.Client.access_token(
            config['personal_access_token'])
        asana_client.tasks.create(params)
        print("I'm finished!")


def main():
    config = read_config()
    root_1 = grab_currently_reading(config)
    currently_reading = parse_currently_reading(root_1)
    root = grab_books(config)
    parse_books(config, root, currently_reading)


if __name__ == "__main__":
    main()
