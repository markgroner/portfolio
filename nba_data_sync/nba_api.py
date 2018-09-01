import requests
import pandas as pd
import json
from config import nba_headers


def nba_get_request(api_route, params):
    base_url = 'http://stats.nba.com/stats/'
    url = f'{base_url}{api_route}'
    print(nba_headers)
    response = requests.get(url, params=params, headers=nba_headers)
    print(f'    CONNECTING TO - {url}')
    print(f'    RESPONSE URL - {response.url}')
    print(f'    RESPONSE STATUS - {response.status_code}')
    json_data = response.json()
    return json_data


def nba_json_to_df(json_data):
    if 'resultSets' in json_data.keys():
        result_set_json = json_data['resultSets']
    elif 'resultSet' in json_data.keys():
        result_set_json = json_data['resultSet']
    main_result_json = result_set_json[0]
    main_headers = main_result_json['headers']
    main_rowset_data = main_result_json['rowSet']
    main_response_df = pd.DataFrame(data=main_rowset_data, columns=main_headers)
    if len(result_set_json) == 2:
        secondary_result_json = result_set_json[1]
        secondary_headers = secondary_result_json['headers']
        secondary_rowset_data = secondary_result_json['rowSet']
        secondary_response_df = pd.DataFrame(data=secondary_rowset_data,
                                            columns=secondary_headers)
        return main_response_df, secondary_response_df
    else:
        return main_response_df


def add_season_column(nba_df, season_string):
    nba_df['SEASON'] = season_string
    nba_df_columns = nba_df.columns.values.tolist()
    nba_df_columns.insert(2, 'SEASON')
    nba_df_columns = nba_df_columns[:-1]
    nba_df = nba_df[nba_df_columns]
    return nba_df



teams_route = 'leaguedashteamstats'
teams_params = {'Conference': '',
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
                'Season': '2017-18',
                'SeasonSegment': '',
                'SeasonType': 'Regular Season',
                'ShotClockRange': '',
                'StarterBench': '',
                'TeamID': 0,
                'VsConference': '',
                'VsDivision': ''
                }

## teams_json = nba_get_request(teams_route, teams_params)
## teams_df = nba_json_to_df(nba_json)
## print(teams_df)
## print(teams_df.columns)

cavs_2017_18_team_id = 1610612739
rosters_route = 'commonteamroster'
rosters_params = {'LeagueID': '00',
                    'Season': '2017-18',
                    'TeamID': cavs_2017_18_team_id
                    }

## roster_df, coaches_df = get_nba_com_dataframe(rosters_route, rosters_params)
## print(roster_df)
## print(coaches_df)


kyrie_player_id = 202681
cavs_2017_18_team_id = 1610612739
shots_route = 'shotchartdetail'
shots_params = {'PlayerID': kyrie_player_id,
                'PlayerPosition': '',
                'Season': '2017-18',
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
                'TeamID': 0,
                'VsConference': '',
                'VsDivision': ''
                }

'''
player_shots_df, league_average_shots_df = get_nba_com_dataframe(shots_route, shots_params)
print(player_shots_df)
print(league_average_shots_df)
'''


players_route = 'leaguedashplayerstats'
players_params = {'College': '',
                    'Conference': '',
                    'Country': '',
                    'DateFrom': '',
                    'DateTo': '',
                    'Division': '',
                    'DraftPick': '',
                    'DraftYear': '',
                    'GameScope': '',
                    'GameSegment': '',
                    'Height': '',
                    'LastNGames': 0,
                    'LeagueID': '00',
                    'Location': '',
                    'MeasureType': 'Base',
                    'Month': 0,
                    'OpponentTeamID': 0,
                    'Outcome': '',
                    'PORound': 0,
                    'PaceAdjust': 'N',
                    'PerMode': 'Totals',
                    'Period': 0,
                    'PlayerExperience': '',
                    'PlayerPosition': '',
                    'PlusMinus': 'N',
                    'Rank': 'N',
                    'Season': '2017-18',
                    'SeasonSegment': '',
                    'SeasonType': 'Regular Season',
                    'ShotClockRange': '',
                    'StarterBench': '',
                    'TeamID': 0,
                    'VsConference': '',
                    'VsDivision': '',
                    'Weight': ''
                    }


## players_df = get_nba_com_dataframe(players_route, players_params)
## print(players_df)
