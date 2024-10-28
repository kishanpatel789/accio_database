# %%
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_PATH
import models
from seed_db import Session

# %%
# create db engine and sessionmaker
url = f"sqlite:///{DB_PATH}"
engine = create_engine(url, echo=True)  # remove echo=True in prod
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# %%
query = select(
        models.Book
)
print(str(query))

# %%
with Session() as db:
    results = db.execute(query).scalars().unique().all()


# %%
with Session() as db:
    book_0 = results[0]
    book_0.chapters
# %%
