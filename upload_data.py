import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('sqlite:///data.db')
pd.read_csv('data/titanic.csv') \
  .to_sql(
    name='titanic',
    con=engine,
    if_exists='replace',
    index=False
)


pd.read_csv('data/cars.csv', parse_dates=["offer_timestamp"]) \
  .to_sql(
    name='cars',
    con=engine,
    if_exists='replace',
    index=False
)
