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


lineup_table_names = ['lineup_base_per_100_stats', 'lineup_scoring_totals_stats', 'lineup_advanced_totals_stats']
## Build query parameter dictionary for lineup api call
measure_type_per_mode = {'lineup_base_per_100_stats': {'measure_type': 'Base', 'per_mode': 'Per100Possessions'},
                        'lineup_scoring_totals_stats': {'measure_type': 'Scoring', 'per_mode': 'Totals'},
                        'lineup_advanced_totals_stats': {'measure_type': 'Advanced', 'per_mode': 'Totals'}}


def lineup_df_to_database(table_name, lineup_df):
    ## Create new `tickets` table with most recent ticket data
    lineup_df.to_sql(table_name, engine, index=False, if_exists='replace')
    with engine.connect() as conn:
        conn.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY (id);')
        ## conn.execute(f'ALTER TABLE team_colors ADD FOREIGN KEY (lineup_id) REFERENCES lineup(id);')
        conn.close()
        print(f'    SUCCESSFULLY UPDATED {table_name}')


lineup_path = 'leaguedashlineups'




for lineup_table in lineup_table_names:
    measure_type_per_mode_dict = measure_type_per_mode[lineup_table]
    home_away_flag = ''
    measure_type = measure_type_per_mode_dict['measure_type']
    per_mode = measure_type_per_mode_dict['per_mode']
    season = '2017-18'
    lineup_stats_parameters = {'Conference': '',
                                'DateFrom': '',
                                'DateTo': '',
                                'Division': '',
                                'GameID': '',
                                'GameSegment': '',
                                'GroupQuantity': 5,
                                'LastNGames': 0,
                                'LeagueID': '00',
                                'Location': home_away_flag,
                                'MeasureType': measure_type,
                                'Month': 0,
                                'OpponentTeamID': 0,
                                'Outcome': '',
                                'PORound': 0,
                                'PaceAdjust': 'N',
                                'PerMode': per_mode,
                                'Period': 0,
                                'PlusMinus': 'N',
                                'Rank': 'N',
                                'Season': season,
                                'SeasonSegment': '',
                                'SeasonType': 'Regular Season',
                                'ShotClockRange': '',
                                'TeamID': 0,
                                'VsConference': '',
                                'VsDivision': ''}
    lineup_json = nba_api.nba_get_request(lineup_path, lineup_stats_parameters)
    lineup_df = nba_api.nba_json_to_df(lineup_json)
    lineup_df.reset_index(inplace=True)
    lineup_df.rename(columns={'index': 'id'}, inplace=True)
    lineup_df_to_database(lineup_table, lineup_df)
