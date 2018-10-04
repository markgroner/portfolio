import pandas as pd
## import sqlalchemy
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
from math import sqrt, atan, degrees, sin, cos

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
                                'lineup_scoring_totals_stats',
                                'shots_w_id'])


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
shots = Base.classes.shots_w_id


'''
URL for the portfolio homepage
'''
@app.route('/')
def home():
    return render_template('index.html')


'''
URL for the projects page
'''
@app.route('/projects')
def projects():
    return render_template('projects.html')


'''
URL for the nba homepage
'''
@app.route('/nba/')
def nba_home():
    return render_template('nba_index.html')


'''
URL for the nba lineups dashboard
'''
@app.route('/nba/lineup-comparison')
def lineup_comparison():
    return render_template('lineup_comparison.html')

'''
Redirects NBA lineup comparison from old rout
'''
@app.route('/nba/lineup_comparison')
def lineup_comparison_redirect():
    return redirect(url_for('lineup_comparison'), code=302)


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
    try:
        db_results = query.all()
        teams_dict = [{'teamId': result[0], 'teamName': result[1]} for result in db_results]
    except sqlalchemy.exc.InternalError:
        print('postgress error')
        session.rollback()
        teams_dict = {'error': 'database error'}
    return jsonify(teams_dict)


'''
Function to clean the lineup names and make them more readable before displaying them in the apps.
Should move this to the ingestion side at some point
'''
def clean_lineup_names(raw_group_names):
    names_list = raw_group_names.split(' - ')
    names_list = [f'{name[name.find(",")+1:name.find(",")+2]}. {name[:name.find(",")]}' for name in names_list]
    group_names = ' - '.join(names_list)
    return group_names


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
        lineups_dict = [{'groupId': result[0], 'groupName': clean_lineup_names(result[1])} for result in db_results]
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
def create_bar_shooting_graph_query(lineup_ids):
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
def create_bar_ratings_graph_query(lineup_ids):
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
def create_bar_scoring_graph_query(lineup_ids):
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
def create_bar_rebounding_graph_query(lineup_ids):
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
      "graphTitle": graph_title,
      "statKeys": [
        stat_keys[0],
        stat_keys[1],
        stat_keys[2]
      ],
      "teamAbbreviations": [
        team1_abbr,
        team2_abbr
      ],
      "graphData": [{
          "teamAbbreviation": team1_abbr,
          stat_keys[0]: round(team1_results[0][1], 2),
          stat_keys[1]: round(team1_results[0][2], 2),
          stat_keys[2]: round(team1_results[0][3], 2)
        },{
          "teamAbbreviation": team2_abbr,
          stat_keys[0]: round(team2_results[0][1], 2),
          stat_keys[1]: round(team2_results[0][2], 2),
          stat_keys[2]: round(team2_results[0][3], 2)
        }
      ]
    }
    return graph_data

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
        db_queries = create_bar_ratings_graph_query(lineup_ids)
        stat_keys = ['Off Rtg', 'Def Rtg', 'Net Rtg']
    elif graph_title == 'Shooting':
        db_queries = create_bar_shooting_graph_query(lineup_ids)
        stat_keys = ['eFG%', 'TS%', '3P%']
    elif graph_title == 'Scoring':
        db_queries = create_bar_scoring_graph_query(lineup_ids)
        stat_keys = ['% Pts FTs', '% Pts Off TO', '% FGM UnAST']
    elif graph_title == 'Rebounding':
        db_queries = create_bar_rebounding_graph_query(lineup_ids)
        stat_keys = ['OREB%', 'DREB%', 'REB%']
    data_dict = db_queries_to_data(db_queries, stat_keys, graph_title)
    return jsonify(data_dict)


'''
This function creates a  sql alchemy query objects for the lineup shot chart graphs
in the lineup comparison dashboard.
It takes one argument:
lineup_id
'''
def get_shot_chart_data(player_ids):
    base_query = session.query(shots.id, shots.LOC_X, shots.LOC_Y, shots.SHOT_TYPE, shots.SHOT_MADE_FLAG)
    query = base_query.filter(shots.PLAYER_ID.in_(player_ids))
    shots_df = pd.read_sql(query.statement, query.session.bind)
    return shots_df


'''
Groups the raw shot chart data to make the chart easier
to interpret.  It takes one argument, a dataframe of raw shot data, and returns
a summary dataframe.
'''
def group_shots(shots_df): ##grouping_length=12): <- also known as scale_factor in R dashboard
    shots_df['x_plot_location'] = [round(x/10) for x in shots_df['LOC_X']]
    shots_df['y_plot_location'] = [round(y/10) for y in shots_df['LOC_Y']]
    shots_df['shot_type_numeric'] = [3 if type == '3PT Field Goal' else 2 for type in shots_df['SHOT_TYPE']]
    shots_df['efg_pct'] = shots_df['shot_type_numeric'] * shots_df['SHOT_MADE_FLAG'] / 2
    grouped_shots_df = shots_df.groupby(['x_plot_location', 'y_plot_location',\
        'shot_type_numeric'], as_index=False).agg({'id':'size', 'efg_pct':'mean'})\
        .rename(columns={'id':'total_shots'})
    return grouped_shots_df


'''
Smooths the grouped shot chart data to make the chart easier
to interpret.  It takes one argument, a dataframe of shot data grouped by location, and returns
a dataframe with smoothed eFG% values.
'''
def smooth_shots(grouped_shots_df, smooth_width, smooth_distance):
    grouped_shots_df['distance'] = '' ## field for smoothing in the future
    grouped_shots_df['shot_radians'] = '' ## field for smoothing in the future
    grouped_shots_df['min_shot_radians'] = '' ## field for smoothing in the future
    grouped_shots_df['max_shot_radians'] = '' ## field for smoothing in the future
    for index, row in grouped_shots_df.iterrows():
        x_plot_loc = grouped_shots_df.loc[index, 'x_plot_location']
        y_plot_loc = grouped_shots_df.loc[index, 'y_plot_location']
        x_for_calcs = x_plot_loc - .0000001 ## - .0000001 to deal with 0 angles
        y_for_calcs = y_plot_loc - .0000001 ## - .0000001 to deal with 0 angles
        distance = sqrt(x_for_calcs**2 + y_for_calcs**2)
        shot_radians = atan((x_for_calcs)/(y_for_calcs))
        shot_radians_adjustment = atan((smooth_width/2)/abs(distance))
        grouped_shots_df.loc[index, 'distance'] = distance
        grouped_shots_df.loc[index, 'shot_radians'] = shot_radians
        grouped_shots_df.loc[index, 'min_shot_radians'] = shot_radians - shot_radians_adjustment
        grouped_shots_df.loc[index, 'max_shot_radians'] = shot_radians + shot_radians_adjustment
    grouped_shots_df['smoothed_efg_pct'] = ''
    for index, row in grouped_shots_df.iterrows():
        shot_radians = grouped_shots_df.loc[index, 'shot_radians']
        min_shot_radians = grouped_shots_df.loc[index, 'min_shot_radians']
        max_shot_radians = grouped_shots_df.loc[index, 'max_shot_radians']
        shot_type = grouped_shots_df.loc[index, 'shot_type_numeric']
        distance = grouped_shots_df.loc[index, 'distance']
                                            ## no further than 6 feet from current spot
        near_shots_df = grouped_shots_df[(grouped_shots_df['shot_radians'] >= min_shot_radians) &\
                                            (grouped_shots_df['shot_radians'] <= max_shot_radians) &\
                                            ## not more than 3 feet closer or further from the basket
                                            (grouped_shots_df['distance'] - distance <= smooth_distance) &\
                                            ## shot type numeric should be the same
                                            (grouped_shots_df['shot_type_numeric'] == shot_type)]
        near_shots_df['efg_pct_weighted'] = near_shots_df['efg_pct']*near_shots_df['total_shots']
        efg_pct_weighted_total = near_shots_df['efg_pct_weighted'].sum()
        area_total_shots = near_shots_df['total_shots'].sum()
        grouped_shots_df.loc[index, 'smoothed_efg_pct'] = efg_pct_weighted_total/area_total_shots
    final_df = grouped_shots_df[['x_plot_location','y_plot_location','efg_pct', 'total_shots', 'smoothed_efg_pct']]\
        .rename(columns={'x_plot_location':'shotLocX',
                            'y_plot_location': 'shotLocY',
                            'efg_pct': 'efgPct',
                            'total_shots': 'totalShots',
                            'smoothed_efg_pct': 'smoothedEfgPct',
                            })
    return final_df


'''
Api route to return shot chart data for the lineup data
'''
@app.route('/nba/lineup-shots')
def lineup_shots():
    lineup_id = request.args.get('lineupId')
    player_ids = lineup_id.split(' - ')
    player_ids = [int(player_id) for player_id in player_ids]
    shots_df = get_shot_chart_data(player_ids)
    grouped_shots_df = group_shots(shots_df)
    smoothed_lineup_shots = smooth_shots(grouped_shots_df, 6, 3)
    json = smoothed_lineup_shots.to_json(orient='records')
    return json


if __name__ == "__main__":
    ##app.run(debug=True, threaded=True)
    app.run(host='0.0.0.0', port=80, threaded=True)
