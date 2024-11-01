# Accio Database

**Objective**: This project scrapes the [Potter DB](https://potterdb.com/) API and generates a relational database. Two python scripts are used. The first script iteratively sends GET requests to the API endpoints to extract data and writes the response to CSV files. The second script initializes a SQLite database and transfers the CSV file content to database tables. 

Project Start: 2024.10.21

Associated blogpost: [Coming Soon]

## Data Source
[Potter DB API](https://docs.potterdb.com/): The Potter DB API serves data from the Harry Potter Universe. The REST API provides detailed information about characters, movies, books, and more from the magical world. The Potter DB project itself sources data from the [Harry Potter Wiki](https://harrypotter.fandom.com/wiki/Main_Page).

As of 2024-11-01, the API provides the following records:
  - 7 Books
  - 4,962 Characters
  - 11 Movies
  - 168 Potions
  - 316 Spells

## Project Outline
The core of the project is housed within the `scripts` directory: 
- `config.py`: Contains global variables to access the local project directory for CSV and SQLite files. Also features the dictionary `CONTROL` which determines which API endpoints will be requested. 
- `models.py`: Defines SQLAlchemy models used to represent relation tables. Used by the script `seed_db.py`.
- `schemas.py`: Defines traits of each API endpoint, like the endpoint URL, URL query parameters, and the target attributes to store. Used by the script `scrape_api.py`.
- `scrape_api.py`: Iteratively sends GET requests to the API and saves the results as CSV files.
- `seed_db.py`: Initializes database before scanning CSV files and inserting deduplicated records into database tables.

If curious, the OpenAPI specification of the Potter DB API is saved in `docs/openapi.json`.

## Setup Instructions
- This project can be run locally: 
  - Download or clone the repository to a local computer. 
  - Create a virtual environment for python 3.11:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## How to Run
In the root directory, run the following commands in order. Progress of each script will be printed to the standard output:
1. `python scripts/scrape_api.py`
   - Repeated GET requests are made to the various API endpoints as defined in `schemas.py`. 
   - For each record returned, primary attributes are stored in a "base" CSV file. Any nested attributes are stored in separate "sub" CSV files.
2. `python scripts/seed_db.py`
   - Uses SQLAlchemy models defined in `models.py` to initialize a SQLite database.
   - Scans CSV files and instantiates an ORM object for each record. 
   - Inserts deduplicated records into database tables via a SQLAlchemy session.
   - Writes any duplicate records that were not inserted into the database in a file `errors.txt`.
