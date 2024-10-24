# %%
import requests
import json
from pathlib import Path
import csv
from schemas import schemas
import time

# %%
api_server = "https://api.potterdb.com"

CSV_DIR = Path(__file__).parents[1] / "data/csv"


# %%
def generate_column_names(table_schema: dict):
    column_names = ["id"]
    if table_schema.get("id_ref") is not None:
        column_names.append(table_schema["id_ref"] + "_id")
    column_names.extend(table_schema["attributes"])

    return column_names


def generate_sub_column_names(table: str, array_attribute: str):
    sub_column_names = [f"{table}_id", array_attribute]

    return sub_column_names


def make_api_get_request(url, payload=None, max_retries=5):
    retry_delay = 1  # 1 second
    for _ in range(max_retries):
        try:
            response = requests.get(url, params=payload)
            print(f"Called '{response.request.url}'")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            if response.status_code == 429:
                print("Reached rate limit and received 429. Will try again...")
                time.sleep(retry_delay)
                retry_delay *= 2  # double the delay for next attempt
            else:
                raise
    raise Exception("Maximum retry attempts reached. Try again in an hour.")


def write_to_csv(response_json, table, table_schema, column_names):
    # open csv file to append
    with open(CSV_DIR / f"{table}.csv", "at", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=column_names, quoting=csv.QUOTE_ALL)

        for record in response_json["data"]:
            # write base csv
            row = dict(id=record["id"])
            if table_schema.get("id_ref") is not None:
                row.update({table_schema["id_ref"] + "_id": ""})
            row.update({k: record["attributes"][k] for k in table_schema["attributes"]})
            writer.writerow(row)

            # write array attributes as sub csv
            for array_attribute in table_schema.get('array_attributes'):
                with open(
                    CSV_DIR / f"{table}_{array_attribute}.csv", "at", newline=""
                ) as f_sub:
                    sub_column_names = generate_sub_column_names(table, array_attribute)
                    sub_writer = csv.DictWriter(f_sub, fieldnames=sub_column_names, quoting=csv.QUOTE_ALL)

                    for value in record["attributes"][array_attribute]:
                        sub_row = {
                            sub_column_names[0]: record["id"],
                            sub_column_names[1]: value,
                        }

                        sub_writer.writerow(sub_row)

                
                


def call_and_write(table, table_schema, column_names, url=None):
    # create base url
    if url is None:
        url = f"{api_server}/{table_schema['api_endpoint']}"
    url_payload = table_schema.get("api_query")

    # call api as many times as needed
    while url is not None:
        r_json = make_api_get_request(url, url_payload)

        # write to csv file
        write_to_csv(r_json, table, table_schema, column_names)

        # get ready for next page
        url = r_json["links"].get("next")
        url_payload = None


# %%
CONTROL = {
    "book": 0,
    "chapter": 0,
    "character": 0,
    "movie": 1,
    "potion": 0,
    "spell": 0,
}
tables_to_get = [k for k, v in CONTROL.items() if v == 1]

# loop through schemas
# if id_ref is present
#   open ref csv file and loop through rows
#   call api function for each row
# else: call api function

# create endpoint
#


# %%
for table in tables_to_get:
    print(f"\n============= {table} =============")
    table_schema = schemas[table]

    # identify final table columns
    column_names = generate_column_names(table_schema)

    # initialize base csv file
    with open(CSV_DIR / f"{table}.csv", "wt", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=column_names, quoting=csv.QUOTE_ALL)
        writer.writeheader()

    # initialize sub-attribute csv files
    if table_schema.get("array_attributes") is not None:
        for array_attribute in table_schema["array_attributes"]:
            with open(
                CSV_DIR / f"{table}_{array_attribute}.csv", "wt", newline=""
            ) as f:
                sub_column_names = generate_sub_column_names(table, array_attribute)
                writer = csv.DictWriter(
                    f, fieldnames=sub_column_names, quoting=csv.QUOTE_ALL
                )
                writer.writeheader()

    if table_schema.get("id_ref") is not None:
        with open(CSV_DIR / f"{table_schema['id_ref']}.csv", "rt", newline="") as f:
            reader_column_names = generate_column_names(
                schemas[f"{table_schema['id_ref']}"]
            )
            reader = csv.DictReader(f, fieldnames=reader_column_names)
            _ = next(reader)  # read header

            for ref_row in reader:
                print(ref_row["id"], ref_row["slug"])

                api_endpoint = table_schema["api_endpoint"].format(rel_id=ref_row["id"])
                url = f"{api_server}/{api_endpoint}"

                call_and_write(table, table_schema, column_names, url)

    else:
        call_and_write(table, table_schema, column_names)

# %%
