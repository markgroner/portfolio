# import necessary libraries
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from config import nba_db_credentials
from flask_sqlalchemy import SQLAlchemy


from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)


app = Flask(__name__)



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


'''
Reflect database tables onto the MetaData object
'''
metadata.reflect(engine, only=['team_total_stats',
                                'lineup_advanced_totals_stats',
                                'lineup_base_per_100_stats',
                                'lineup_scoring_totals_stats'])


'''
Produce a set of mappings from this MetaData and call prepare to set up mapped
classes and relationships
'''
Base = automap_base(metadata=metadata)
Base.prepare()


'''
Map class back to objects to be used in queries
'''
lineupAdvancedTotalsStats  = Base.classes.lineup_advanced_totals_stats
lineupBasePer100Stats = Base.classes.lineup_base_per_100_stats
lineupScoringTotalsStats = Base.classes.lineup_scoring_totals_stats
teamTotalStats = Base.classes.team_total_stats


'''
Serves up the index.html
'''
@app.route('/')
def home():
    return render_template('index.html')


'''
Serves up the projects.html
'''
@app.route('/projects')
def projects():
    return render_template('projects.html')


'''
Serves up the nba_index.html
'''
@app.route('/nba/')
def nba_home():
    return render_template('nba_index.html')


'''
Serves up the lineup_comparison.html
'''
@app.route('/nba/lineup_comparison')
def lineup_comparison():
    return render_template('lineup_comparison.html')


'''
API route to return to list of lineup ids available for the selected teams lineup
drop down menus in the lineup comparison dashboard
'''
@app.route('/nba/lineup_team_name_year')
def lineup_team_name_data():
    season_id = request.args.get('seasonId')
    query = session.query(teamTotalStats.TEAM_ID, teamTotalStats.TEAM_NAME)\
                        .filter(teamTotalStats.SEASON_ID == season_id)\
                        .order_by(teamTotalStats.TEAM_NAME.asc())
    db_results = query.all()
    try:
        db_results = query.all()
        teams_dict = [{'teamId': result[0], 'teamName': result[1]} for result in db_results]
    except sqlalchemy.exc.InternalError:
        print('postgress error')
        session.rollback()
        teams_dict = {'error': 'database error'}
    return jsonify(teams_dict)


'''
API route to return to list of lineup ids available for the selected teams lineup
drop down menus in the lineup comparison dashboard
'''
@app.route('/nba/lineup_names_id')
def lineup_names_id_data():
    team_id = request.args.get('teamId')
    query = session.query(lineupAdvancedTotalsStats.GROUP_ID, lineupAdvancedTotalsStats.GROUP_NAME)\
                        .filter(lineupAdvancedTotalsStats.TEAM_ID == team_id)
    try:
        db_results = query.all()
        lineups_dict = [{'groupId': result[0], 'groupName': result[1]} for result in db_results]
    except sqlalchemy.exc.InternalError:
        print('postgress error')
        session.rollback()
        lineups_dict = {'error': 'database error'}
    return jsonify(lineups_dict)


'''
This function creates a list of 2 sql alchemy query objects for the SHOOTING graph
in the lineup comparison dashboard. The queries are ultimately executed in the
db_queries_to_data function. It takes one argument:
lineup_ids - a list of two lineup ids
'''
def get_bar_shooting_graph_data(lineup_ids):
    base_query = session.query(lineupAdvancedTotalsStats.TEAM_ABBREVIATION,
                            lineupAdvancedTotalsStats.EFG_PCT,
                            lineupAdvancedTotalsStats.TS_PCT,
                            lineupBasePer100Stats.FG3_PCT)
    team1_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[0])
    team2_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[1])
    db_queries = [team1_query, team2_query]
    return db_queries


'''
This function creates a list of 2 sql alchemy query objects for the RATINGS graph
in the lineup comparison dashboard. The queries are ultimately executed in the
db_queries_to_data function. It takes one argument:
lineup_ids - a list of two lineup ids
'''
def get_bar_ratings_graph_data(lineup_ids):
    base_query = session.query(lineupAdvancedTotalsStats.TEAM_ABBREVIATION,
                            lineupAdvancedTotalsStats.OFF_RATING,
                            lineupAdvancedTotalsStats.DEF_RATING,
                            lineupAdvancedTotalsStats.NET_RATING)
    team1_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[0])
    team2_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[1])
    db_queries = [team1_query, team2_query]
    return db_queries


'''
This function creates a list of 2 sql alchemy query objects for the SCORING graph
in the lineup comparison dashboard. The queries are ultimately executed in the
db_queries_to_data function. It takes one argument:
lineup_ids - a list of two lineup ids
'''
def get_bar_scoring_graph_data(lineup_ids):
    base_query = session.query(lineupScoringTotalsStats.TEAM_ABBREVIATION,
                            lineupScoringTotalsStats.PCT_PTS_FT,
                            lineupScoringTotalsStats.PCT_PTS_OFF_TOV,
                            lineupScoringTotalsStats.PCT_UAST_FGM)
    team1_query = base_query.filter(lineupScoringTotalsStats.GROUP_ID == lineup_ids[0])
    team2_query = base_query.filter(lineupScoringTotalsStats.GROUP_ID == lineup_ids[1])
    db_queries = [team1_query, team2_query]
    return db_queries


'''
This function creates a list of 2 sql alchemy query objects for the REBOUNDING graph
in the lineup comparison dashboard. The queries are ultimately executed in the
db_queries_to_data function. It takes one argument:
lineup_ids - a list of two lineup ids
'''
def get_bar_rebounding_graph_data(lineup_ids):
    base_query = session.query(lineupAdvancedTotalsStats.TEAM_ABBREVIATION,
                            lineupAdvancedTotalsStats.OREB_PCT,
                            lineupAdvancedTotalsStats.DREB_PCT,
                            lineupAdvancedTotalsStats.REB_PCT)
    team1_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[0])
    team2_query = base_query.filter(lineupAdvancedTotalsStats.GROUP_ID == lineup_ids[1])
    db_queries = [team1_query, team2_query]
    return db_queries


'''
This function takes sqlalchemy query objects for grouped bar chart lineup
data and executes them, and returns the data as a dictionary.
The three arguments taken are:
1. db_queries - a list with two sql alchemy query objects (one for each team)
2. stat_keys - a list of the three stats measured in the grouped bar
3. graph_title
'''
def db_queries_to_data(db_queries, stat_keys, graph_title):
    team1_query = db_queries[0]
    team2_query = db_queries[1]
    try:
        team1_results = team1_query.all()
    except sqlalchemy.exc.InternalError:
        print('postgress error')
        session.rollback()
        team1_results = {'error': 'database error'}
    try:
        team2_results = team2_query.all()
    except sqlalchemy.exc.InternalError:
        print('postgress error')
        session.rollback()
        team2_results = {'error': 'database error'}
    if team1_query[0][0] == team2_query[0][0]:
        team1_abbr = f'{team1_query[0][0]} 1'
        team2_abbr = f'{team2_query[0][0]} 2'
    else:
        team1_abbr = team1_query[0][0]
        team2_abbr = team2_query[0][0]
    graph_data = {
        'graph_title': graph_title,
        'stat_key1': stat_keys[0],
        'stat_key2': stat_keys[1],
        'stat_key3': stat_keys[2],
        'team1_abbr': team1_abbr,
        'team2_abbr': team2_abbr,
        'team1_stat1': team1_query[0][1],
        'team1_stat2': team1_query[0][2],
        'team1_stat3': team1_query[0][3],
        'team2_stat1': team2_results[0][1],
        'team2_stat2': team2_results[0][2],
        'team2_stat3': team2_results[0][3]
        }
    return graph_data

'''
Function that takes the grouped bar chart dictionary data and normalizes it
into the JSON structure the application is expecting
'''
def create_bar_chart_json(data_dict):
    data = '''
    {
      "graphTitle": "%s",
      "statKeys": [
        "%s",
        "%s",
        "%s"
      ],
      "teamAbbreviations": [
        "%s",
        "%s"
      ],
      "graphData": [{
          "teamAbbreviation": "%s",
          "%s": %.2f,
          "%s": %.2f,
          "%s": %.2f
        },{
          "teamAbbreviation": "%s",
          "%s": %.2f,
          "%s": %.2f,
          "%s": %.2f
        }
      ]
    }''' % (
        data_dict['graph_title'],
        data_dict['stat_key1'],
        data_dict['stat_key2'],
        data_dict['stat_key3'],
        data_dict['team1_abbr'],
        data_dict['team2_abbr'],
        data_dict['team1_abbr'],
        data_dict['stat_key1'],
        data_dict['team1_stat1'],
        data_dict['stat_key2'],
        data_dict['team1_stat2'],
        data_dict['stat_key3'],
        data_dict['team1_stat3'],
        data_dict['team2_abbr'],
        data_dict['stat_key1'],
        data_dict['team2_stat1'],
        data_dict['stat_key2'],
        data_dict['team2_stat2'],
        data_dict['stat_key3'],
        data_dict['team2_stat3'],
    )
    return data

'''
Api route that returns the data necesssary for the grouped bar charts
in the nba lineup comparison dashboard in JSON format. Takes three parameters
1. graphTitle
2. team1LineupId
3. team2LineupId
'''
@app.route('/nba/grouped-bar-data')
def group_bar_data():
    graph_title = request.args.get('graphTitle')
    team1_lineup_id = request.args.get('team1LineupId')
    team2_lineup_id = request.args.get('team2LineupId')
    lineup_ids = [team1_lineup_id, team2_lineup_id]
    if graph_title == 'Ratings':
        db_queries = get_bar_ratings_graph_data(lineup_ids)
        stat_keys = ['Off Rtg', 'Def Rtg', 'Net Rtg']
    elif graph_title == 'Shooting':
        db_queries = get_bar_shooting_graph_data(lineup_ids)
        stat_keys = ['eFG%', 'TS%', '3P%']
    elif graph_title == 'Scoring':
        db_queries = get_bar_scoring_graph_data(lineup_ids)
        stat_keys = ['% Pts FTs', '% Pts Off TO', '% FGM UnAST']
    elif graph_title == 'Rebounding':
        db_queries = get_bar_rebounding_graph_data(lineup_ids)
        stat_keys = ['OREB%', 'DREB%', 'REB%']
    data_dict = db_queries_to_data(db_queries, stat_keys, graph_title)
    api_data = create_bar_chart_json(data_dict)
    return api_data


if __name__ == "__main__":
    ##app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
