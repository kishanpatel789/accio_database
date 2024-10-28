# %%
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
from datetime import datetime

from models import metadata_obj, Book, Chapter, Potion, Spell
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
# create db engine and sessionmaker
url = f"sqlite:///{DB_PATH}"
engine = create_engine(url, echo=True)  # remove echo=True in prod
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# %%
with Session() as db:
    metadata_obj.drop_all(bind=engine)
    metadata_obj.create_all(bind=engine)

    # models
    for mapper in seed_map:
        print(mapper["name"])
        mod_inst_items = []

        with open(CSV_DIR / mapper["file"], newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                mod_inst = mapper["cls"]()
                for key, value in row.items():
                    if value == "":  # overwrite empty value with None (null)
                        value = None
                    if key in mapper["dt_cols"] and value != None:
                        value = datetime.strptime(value, "%Y-%m-%d")
                    setattr(mod_inst, key, value)
                mod_inst_items.append(mod_inst)

        for mod_inst in mod_inst_items:
            db.add(mod_inst)

    db.commit()

# %%
