import pandas as pd
import nba_api
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



## Build query parameter dictionary for lineup api call
measure_type_per_mode = {'shots_base_per_100_stats': {'measure_type': 'Base', 'per_mode': 'Per100Possessions'},
                        'shots_scoring_totals_stats': {'measure_type': 'Scoring', 'per_mode': 'Totals'},
                        'shots_advanced_totals_stats': {'measure_type': 'Advanced', 'per_mode': 'Totals'}}


def shots_df_to_database(table_name, shots_df):
    ## Create new `tickets` table with most recent ticket data
    shots_df.to_sql(table_name, engine, index=False, if_exists='replace')
    with engine.connect() as conn:
        conn.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY (id);')
        ## conn.execute(f'ALTER TABLE team_colors ADD FOREIGN KEY (shots_id) REFERENCES lineup(id);')
        conn.close()
        print(f'    SUCCESSFULLY UPDATED {table_name}')



shots_table = 'shots'
player_id = 2544 ## lebron
team_id = 1610612739 ## cavs 2017-18
season = '2017-18'
shots_path = 'shotchartdetail'
shots_params = {'PlayerID': player_id,
                'PlayerPosition': '',
                'Season': season,
                'ContextMeasure': 'FGA',
                'DateFrom': '',
                'DateTo': '',
                'GameID': '',
                'GameSegment': '',
                'LastNGames': 0,
                'LeagueID': '00',
                'Location': '',
                'OpponentTeamID': 0,
                'Month': 0,
                'Outcome': '',
                'Period': 0,
                'Position': '',
                'RookieYear': '',
                'SeasonSegment': '',
                'SeasonType': 'Regular Season',
                'TeamID': team_id,
                'VsConference': '',
                'VsDivision': ''
                }
shots_json = nba_api.nba_get_request(shots_path, shots_params)
shots_df, _ = nba_api.nba_json_to_df(shots_json)
shots_df.reset_index(inplace=True)
shots_df.rename(columns={'index': 'id'}, inplace=True)

shots_df_to_database(shots_table, shots_df)
