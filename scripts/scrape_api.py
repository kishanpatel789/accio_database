

# %%
import requests
import json
from pathlib import Path
import csv
from schemas import schemas

# %%
api_server = "https://api.potterdb.com"

endpoints = [
    "v1/books",
    "v1/books/{id}/chapters",
]

csv_dir = Path(__file__).parents[1] / 'data/csv'


# %%
# get data

response = requests.get(f"{api_server}/v1/books")

# %%
if response.status_code == 200:
    r_json = response.json()
    data = r_json.get('data')

# %%
# look for next page
next_page_url = r_json['links'].get('next')
if next_page_url:
    pass
    # TODO: call endpoint again

# %%
# save as csv

# %%
with open(csv_dir / 'book.csv', 'wt', newline='') as f:
    column_names = ['id'] + schemas['book']
    writer = csv.DictWriter(f, fieldnames=column_names, quoting=csv.QUOTE_ALL)

    writer.writeheader()

    for book in data:
        writer.writerow(dict(
            id=book['id'],
            **book['attributes']
        ),
        )

# %%
##### chapters #####
with open(csv_dir / 'book.csv', 'rt', newline='') as f:
    reader_column_names = ['id'] + schemas['book']
    reader = csv.DictReader(f, fieldnames=reader_column_names)
    _ = next(reader) # read header

    with open(csv_dir / 'chapter.csv', 'wt', newline='') as fc:
        column_names = ['id', 'book_id'] + schemas['chapter']
        writer = csv.DictWriter(fc, fieldnames=column_names, quoting=csv.QUOTE_ALL)

        writer.writeheader()

        for book in reader:
            print(book['id'], book['slug'])

            endpoint_url = f"{api_server}/v1/books/{book['id']}/chapters"

            while endpoint_url:
                response = requests.get(endpoint_url)

                if response.status_code == 200:
                    r_json = response.json()
                    data = r_json.get('data')
                    endpoint_url = r_json['links'].get('next')
                else:
                    print(f"Error occurred: {response.status_code}")
                    raise
                    
                for chapter in data:
                    writer.writerow(dict(
                        id=chapter['id'],
                        book_id=book['id'],
                        **chapter['attributes']
                    ),
                    )



# %%

response = requests.get(f"{api_server}/" + "v1/books/{id}/chapters".format(id='6751e7f7-a8b7-488b-bde7-8606822d2338'))

# %%
if response.status_code == 200:
    r_json = response.json()
    data = r_json.get('data')
else:
    print(f"Error occurred: {response.status_code}")

# %%
