# %%
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_PATH, CSV_DIR
import models
import pandas as pd

# %%
# create db engine and sessionmaker
url = f"sqlite:///{DB_PATH}"
engine = create_engine(url, echo=True)  # remove echo=True in prod
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# %%
query = select(
        models.Movie
).where(models.Movie.id == '678d2264-9c10-4eaa-9b9c-7f70fc331614').limit(20)
print(str(query))

# %%
with Session() as db:
    results = db.execute(query).scalars().unique().all()

# %%
results[0].distributors
# %%
# %%
df_char = pd.read_csv(CSV_DIR/ 'character.csv')
# %%
df_char_agg = df_char.groupby('slug').size().to_frame(name='cnt')
df_char_agg[df_char_agg['cnt']>1]