import pandas as pd
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from config import nba_db_credentials



nba_db_username = nba_db_credentials['nba_db_username']
nba_db_password = nba_db_credentials['nba_db_password']
## Create sqlalchemy engine
engine = create_engine(f'postgres://{nba_db_username}:{nba_db_password}@nba.cjcg4ksti8rr.us-east-2.rds.amazonaws.com:5432/nba')

## Create a session
session = Session(engine)

## Declare a Base using `automap_base()`
Base = automap_base()

## Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

teams_path = os.path.join('data', 'teams.csv')
teams_df = pd.read_csv(teams_path)

## Create new `tickets` table with most recent ticket data
teams_df.to_sql('teams', engine, index=False, if_exists='replace')
with engine.connect() as conn:
    conn.execute('ALTER TABLE teams ADD PRIMARY KEY (id);')
    conn.close()
