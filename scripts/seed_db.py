# %%
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
from datetime import datetime
import hashlib


from models import metadata_obj, Book, Chapter, Character, Potion, Spell
from config import DB_PATH, CSV_DIR

# %%
seed_map = [
    {
        "name": "book",
        "cls": Book,
        "file": "book.csv",
        "dt_cols": ["release_date"],
    },
    {
        "name": "chapter",
        "cls": Chapter,
        "file": "chapter.csv",
        "dt_cols": [],
    },
    {
        "name": "character",
        "cls": Character,
        "file": "character.csv",
        "dt_cols": [],
    },
    {
        "name": "potion",
        "cls": Potion,
        "file": "potion.csv",
        "dt_cols": [],
    },
    {
        "name": "spell",
        "cls": Spell,
        "file": "spell.csv",
        "dt_cols": [],
    },
]


# %%
# def get_unique_columns(model):
#     columns = []
#     inspector = inspect(model)
#     for c in inspector.columns:
#         if any([c.unique, c.primary_key]):
#             columns.append(c.name)

#     return columns


# %%
# create db engine and sessionmaker
url = f"sqlite:///{DB_PATH}"
engine = create_engine(url, echo=False)  # remove echo=True in prod
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# %%
error_file_name = "errors.txt"
with open(error_file_name, "wt") as f:
    pass

with Session() as db:
    metadata_obj.drop_all(bind=engine)
    metadata_obj.create_all(bind=engine)

    # models
    for mapper in seed_map:
        print(f"\n============= {mapper["name"]} =============")
        mod_inst_items = []
        row_id_hashes = set()

        with open(CSV_DIR / mapper["file"], newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print(row)

                # check for duplicate id
                row_id_hash = hashlib.sha256(row["id"].encode()).hexdigest()
                if row_id_hash in row_id_hashes:
                    with open(error_file_name, "at") as f:
                        print(
                            f"Duplicate record found in '{mapper['name']}': {row}", file=f
                        )
                    continue
                else:
                    row_id_hashes.add(row_id_hash)

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
        for mod_inst in mod_inst_items:
            db.add(mod_inst)

        db.commit()

        print(f"    Wrote {len(mod_inst_items):,} records to database")


# %%
