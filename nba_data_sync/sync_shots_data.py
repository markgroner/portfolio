import pandas as pd
import nba_api
##import sqlalchemy
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from config import nba_db_credentials
import time
from sqlalchemy.sql import func
from sqlalchemy import (
    create_engine,
    MetaData,
    update,
    Column,
    Integer,
    String,
    Float,
    DateTime)


'''
Create sqlalchemy engine
'''
nba_db_username = nba_db_credentials['nba_db_username']
nba_db_password = nba_db_credentials['nba_db_password']
engine = create_engine(f'postgres://{nba_db_username}:{nba_db_password}@nba.cjcg4ksti8rr.us-east-2.rds.amazonaws.com:5432/nba')


'''
Create a session
'''
session = Session(engine)


'''
Create a MetaData object
'''
metadata = MetaData()

## Declare a Base using `automap_base()`
Base = automap_base()

## Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

'''
Reflect database tables onto the MetaData object
'''
metadata.reflect(engine, only=['players'])

'''
Produce a set of mappings from this MetaData and call prepare to set up mapped
classes and relationships
'''
Base = automap_base(metadata=metadata)
Base.prepare()


'''
Map class back to objects to be used in queries
'''
players  = Base.classes.players

raw_response = session.query(players.PLAYER_ID, players.TEAM_ID).filter(players.date_shots_updated == None).all()
all_players = [{'PLAYER_ID': response[0], 'TEAM_ID': response[1]} for response in raw_response]


def log_player_shots_update(player_id, team_id, season):
    session.query(players).filter(players.PLAYER_ID==player_id,\
                                players.TEAM_ID==team_id,\
                                players.season==season)\
                            .update({players.date_shots_updated: datetime.now()})
    session.commit()
    print(f'    SUCCESSFULLY LOGGED SHOT UPDATED RECORD FOR PLAYER_ID - {player_id}')


def shots_df_to_database(table_name, shots_df):
    ## Create new `tickets` table with most recent ticket data
    shots_df.to_sql(table_name, engine, index=False, if_exists='append')
    log_player_shots_update(player_id,  team_id, season)
    ## with engine.connect() as conn:
    ##     conn.execute(f'ALTER TABLE {table_name} ADD PRIMARY KEY (id);')
    ##     conn.execute(f'ALTER TABLE team_colors ADD FOREIGN KEY (shots_id) REFERENCES lineup(id);')
    ##     conn.close()
    print(f'    SUCCESSFULLY UPDATED {table_name}')

for i in range(0, len(all_players)):
    player = all_players[i]
    player_id = player['PLAYER_ID']
    team_id = player['TEAM_ID']
    shots_table = 'shots'
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
    shots_df_to_database(shots_table, shots_df)
    print(f'    {i+1} players updated - {len(all_players) - i} remaining')
    time.sleep(3)
