# %%
import csv
from datetime import datetime
import hashlib
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

import models
from config import CSV_DIR, DB_PATH, ERROR_FILE_PATH

# %%
# define map for seeding database
seed_map = {
    "book": {"cls": models.Book, "dt_cols": ["release_date"]},
    "chapter": {"cls": models.Chapter, "dt_cols": []},
    "character": {"cls": models.Character, "dt_cols": []},
    "character_alias_names": {"cls": models.CharacterAliasNames, "dt_cols": []},
    "character_family_members": {"cls": models.CharacterFamilyMembers, "dt_cols": []},
    "character_jobs": {"cls": models.CharacterJobs, "dt_cols": []},
    "character_romances": {"cls": models.CharacterRomances, "dt_cols": []},
    "character_titles": {"cls": models.CharacterTitles, "dt_cols": []},
    "character_wands": {"cls": models.CharacterWands, "dt_cols": []},
    "movie": {"cls": models.Movie, "dt_cols": ["release_date"]},
    "movie_directors": {"cls": models.MovieDirectors, "dt_cols": []},
    "movie_screenwriters": {"cls": models.MovieScreenwriters, "dt_cols": []},
    "movie_producers": {"cls": models.MovieProducers, "dt_cols": []},
    "movie_cinematographers": {"cls": models.MovieCinematographers, "dt_cols": []},
    "movie_editors": {"cls": models.MovieEditors, "dt_cols": []},
    "movie_distributors": {"cls": models.MovieDistributors, "dt_cols": []},
    "movie_music_composers": {"cls": models.MovieMusicComposers, "dt_cols": []},
    "potion": {"cls": models.Potion, "dt_cols": []},
    "spell": {"cls": models.Spell, "dt_cols": []},
}


# %%
def get_engine(echo: bool = False) -> Engine:
    """
    Create and return a SQLAlchemy Engine that can produce connections to local sqlite database.

    Args:
        echo (bool, optional): Output SQL commands to stdout. Defaults to False.

    Returns:
        Engine: SQLAlchemy Engine for sqlite database.
    """

    url = f"sqlite:///{DB_PATH}"
    engine = create_engine(url, echo=echo)

    return engine

    """

    Returns:
        Session: 
    """


def create_session(engine: Engine) -> Session:
    """
    Create and return a SQLAlchemy Session to sqlite database.

    Args:
        engine (Engine): A SQLAlchemy engine to bind to the session.

    Returns:
        Session: A SQLAlchemy Session object.
    """

    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()

    return session


def initialize_error_file() -> None:
    """
    Initializes the error file to be used when seeding the database.
    """

    if not ERROR_FILE_PATH.exists():
        ERROR_FILE_PATH.touch()
    else:
        with ERROR_FILE_PATH.open("w") as f:
            f.truncate(0)


def write_row_error(table_name: str, row: Dict[str, str]) -> None:
    """
    Write duplicate row from CSV into file. Duplicate row will not be written to database.

    Args:
        table_name (str): Name of table.
        row (Dict[str, str]): Dictionary representing row from CSV that was not written to database.
    """

    with ERROR_FILE_PATH.open("a") as f:
        print(
            f"Duplicate record found in '{table_name}': {row}",
            file=f,
        )


# %%
def main():
    """
    Process CSV files to generate a database.

    Function creates database tables and then loops through `seed_map` dictionary. For each key, the CSV file contents are read row-by-row. Each row is used to instantiate a SQLAlchemy model. Model instances are then added to a SQlAlchemy Session to later insert records into database tables.

    Any duplicate rows are not written to the database. For base CSV files, duplicate rows are identified by the `id` column. For sub-CSV files, duplicate rows are identified by the combination of all columns.
    """

    # create sqlalchemy engine
    engine = get_engine()

    with create_session(engine) as db:
        # create database tables and initialize error file
        models.metadata_obj.drop_all(bind=engine)
        models.metadata_obj.create_all(bind=engine)
        initialize_error_file()
        print(f"Seeding database: '{DB_PATH}'")

        # loop through seed_map
        for table_name, mapper in seed_map.items():
            print(f"\n============= {table_name} =============")
            mod_inst_items = []
            row_id_hashes = set()
            row_hashes = set()

            with open(CSV_DIR / f"{table_name}.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # print(row)

                    # check for duplicate id or entire row
                    if hasattr(mapper["cls"], "id"):
                        row_id_hash = hashlib.sha256(row["id"].encode()).hexdigest()
                        if row_id_hash in row_id_hashes:
                            write_row_error(table_name, row)
                            continue
                        else:
                            row_id_hashes.add(row_id_hash)
                    else:
                        row_hash = hashlib.sha256(str(row).encode()).hexdigest()
                        if row_hash in row_hashes:
                            write_row_error(table_name, row)
                            continue
                        else:
                            row_hashes.add(row_hash)

                    # generate orm object
                    mod_inst = mapper["cls"]()
                    for key, value in row.items():
                        if value == "":  # overwrite empty value with None (null)
                            value = None
                        if key in mapper["dt_cols"] and value != None:
                            value = datetime.strptime(value, "%Y-%m-%d")
                        setattr(mod_inst, key, value)
                    mod_inst_items.append(mod_inst)

            # persist orm objects in db
            db.add_all(mod_inst_items)
            db.commit()

            print(f"    Wrote {len(mod_inst_items):,} records to database")


# %%
if __name__ == "__main__":
    main()
