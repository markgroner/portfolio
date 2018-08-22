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

team_colors_path = os.path.join('data', 'team_colors.csv')
team_colors_df = pd.read_csv(team_colors_path)

## Create new `tickets` table with most recent ticket data
team_colors_df.to_sql('team_colors', engine, index=False, if_exists='replace')
with engine.connect() as conn:
    conn.execute('ALTER TABLE team_colors ADD PRIMARY KEY (id);')
    conn.execute('ALTER TABLE team_colors ADD FOREIGN KEY (team_id) REFERENCES teams(id);')
    conn.close()
