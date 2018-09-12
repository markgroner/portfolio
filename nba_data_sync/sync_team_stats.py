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


def team_df_to_database(table_name, lineup_df):
    ## Create new `tickets` table with most recent ticket data
    lineup_df.to_sql(table_name, engine, index=False, if_exists='replace')
    with engine.connect() as conn:
        conn.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY (id);')
        ## conn.execute(f'ALTER TABLE team_colors ADD FOREIGN KEY (lineup_id) REFERENCES lineup(id);')
        conn.close()
        print(f'    SUCCESSFULLY UPDATED {table_name}')


lineup_path = 'leaguedashteamstats'
season = '2017-18'

team_stats_parameters = {'Conference': '',
                        'DateFrom': '',
                        'DateTo': '',
                        'Division': '',
                        'GameScope': '',
                        'GameSegment': '',
                        'LastNGames': 0,
                        'LeagueID': '00',
                        'Location': '',
                        'MeasureType': 'Base',
                        'Month': 0,
                        'OpponentTeamID': 0,
                        'Outcome': '',
                        'PORound': 0,
                        'PaceAdjust': 'N',
                        'PerMode': 'PerGame',
                        'Period': 0,
                        'PlayerExperience': '',
                        'PlayerPosition': '',
                        'PlusMinus': 'N',
                        'Rank': 'N',
                        'Season': season,
                        'SeasonSegment': '',
                        'SeasonType': 'Regular Season',
                        'ShotClockRange': '',
                        'StarterBench': '',
                        'TeamID': 0,
                        'VsConference': '',
                        'VsDivision': ''
                        }
team_json = nba_api.nba_get_request(lineup_path, team_stats_parameters)
team_df = nba_api.nba_json_to_df(team_json)
team_df['SEASON_ID'] = season
team_df.reset_index(inplace=True)
team_df.rename(columns={'index': 'id'}, inplace=True)
team_df_to_database('team_total_stats', team_df)
