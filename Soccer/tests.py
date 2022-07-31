# See European Soccer Game Analysis from https://www.projectpro.io/article/sql-database-projects-for-data-analysis-to-practice/565
# Kaggle data set: https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/data

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

# What country is each leage in?
#table = pd.read_sql("SELECT League.name, Country.name FROM League JOIN Country ON League.country_id = Country.id", conn)
#print(table)

# Get the Home Player 1's.
#table = pd.read_sql("SELECT Match.match_api_id, Player.player_name FROM Match JOIN Player ON Match.home_player_1 = Player.player_api_id", conn)
#print(table)

# For a given team (takes the short name as a parameter), plot the average goals per game the team gets over time (by year).
def team_score(team_name):
    table = pd.read_sql("""
        WITH goals AS
        (
            SELECT 
                Team.team_short_name,
                Match.season,
                SUM(Match.home_team_goal) AS Season_Home_Goals,
                SUM(Match.away_team_goal) AS Season_Away_Goals,
                COUNT(Match.home_team_goal) AS Season_Home_Games,
                COUNT(Match.away_team_goal) AS Season_Away_Games
            FROM Team JOIN Match ON Team.team_api_id = Match.home_team_api_id
            WHERE team_short_name = "{0}"
            GROUP BY Team.team_short_name, Match.season
        ),
        goal_calcs AS
        (
            SELECT 
                team_short_name,
                season,
                Season_Home_Games+Season_Away_Games AS Season_Games,
                Season_Home_Goals+Season_Away_Goals AS Season_Goals
            FROM goals
        )
        SELECT 
            team_short_name,
            season,
            Season_Games,
            Season_Goals,
            CAST (Season_Goals AS FLOAT) / CAST (Season_Games AS FLOAT) AS Goals_Per_Game
        FROM goal_calcs
    ;""".format(team_name), conn)
    return table
def team_score_plot(team_name_short):
    table = team_score(team_name_short)
    fig = plt.figure(figsize=(8,6))
    ax = plt.axes()
    seasons = table["season"].to_list()
    years = [int(seasons[i].split("/")[0]) for i in range(len(seasons))]
    ax.plot(seasons, table["Goals_Per_Game"])
    plt.title("Team {0}: Average Goals per Game".format(team_name_short))
    plt.xticks(rotation = 15)
    plt.xlabel("Season")
    plt.ylabel("Goals per Game")
    plt.show()
#team_score_plot("ABE")

####################### For a given player, find out what team(s) they played on, the player number (1-11), and whether the team was home or away.
def player_teams_subquery(player_name, home_away, player_position):
    return """
        SELECT '{2}' AS 'Player Number', '{1}' AS 'Home or Away', Team.team_long_name AS 'Team Name'
        FROM Player JOIN Match JOIN Team ON Player.player_api_id = Match.{1}_player_{2} AND Match.{1}_team_api_id = Team.team_api_id
        WHERE Player.player_name = '{0}'
    """.format(player_name, home_away, player_position)
  
def player_teams(player_name):
    query = "\nUNION\n".join(
        [player_teams_subquery(player_name,"home",i) for i in range(1,12)] +
        [player_teams_subquery(player_name,"away",i) for i in range(1,12)]
    ) +";"
    print(pd.read_sql(query, conn))

def all_player_teams():
    players = pd.read_sql("SELECT * FROM Player;",conn)["player_name"].to_list()
    for i in range(len(players)):
        print(players[i])
        player_teams(players[i])
        print("\n")
#all_player_teams()

####################### Just the count of how many teams a player has been on. Eventually do this for all players.
def player_teams_subquery_abb(player_name, home_away, player_position):
    return """
        SELECT Match.{1}_team_api_id AS 'TeamNumber'
        FROM Player JOIN Match ON Player.player_api_id = Match.{1}_player_{2}
        WHERE Player.player_name = '{0}'
    """.format(player_name, home_away, player_position)
  
def player_teams_abb(player_name):
    sub_query = "\nUNION\n".join(
        [player_teams_subquery_abb(player_name,"home",i) for i in range(1,12)] +
        [player_teams_subquery_abb(player_name,"away",i) for i in range(1,12)]
    )
    full_query = """
        WITH Teams AS ({0})
        SELECT COUNT(TeamNumber) FROM Teams
    ;""".format(sub_query)
    print(pd.read_sql(full_query, conn))
#player_teams_abb("Aaron Hunt")

def all_player_teams_abb():
    players = pd.read_sql("SELECT * FROM Player;",conn)["player_name"].to_list()
    for i in range(len(players)):
        print(players[i])
        player_teams_abb(players[i])
        print("\n")
all_player_teams_abb()

# To-do
# - Display the count as a simple number (i.e. no pandas table).
# - Join it with all players
# - Visualize the data

#################################################################################
# List of teams by 3 letter abbreviation

#table = pd.read_sql("SELECT * FROM Team;", conn)
#print(table["team_short_name"].to_list())
#['GEN', 'BAC', 'ZUL', 'LOK', 'CEB', 'AND', 'GEN', 'MON', 'DEN', 'STL', 'MEC', 'CLB', 'ROS', 'KOR', 'TUB', 'MOU', 'WES', 'CHA', 'STT', 'LIE', 'EUP', 'O-H', 'WAA', 'OOS', 'MOP', 'MUN', 'NEW', 'ARS', 'WBA', 'SUN', 'LIV', 'WHU', 'WIG', 'AVL', 'MCI', 'EVE', 'BLB', 'MID', 'TOT', 'BOL', 'STK', 'HUL', 'FUL', 'CHE', 'POR', 'BIR', 'WOL', 'BUR', 'BLA', 'SWA', 'QPR', 'NOR', 'SOU', 'REA', 'CRY', 'CAR', 'LEI', 'BOU', 'WAT', 'AUX', 'NAN', 'BOR', 'CAE', 'LEH', 'NIC', 'LEM', 'LOR', 'LYO', 'TOU', 'MON', 'PSG', 'NAN', 'LIL', 'REN', 'MAR', 'SOC', 'GRE', 'VAL', 'ETI', 'LEN', 'MON', 'BOU', 'ARL', 'BRE', 'AJA', 'ETG', 'DIJ', 'REI', 'BAS', 'TRO', 'GUI', 'MET', 'ANG', 'GAJ', 'BMU', 'HAM', 'LEV', 'DOR', 'S04', 'HAN', 'WOL', 'FCK', 'EFR', 'HBE', 'BIE', 'WBR', 'COT', 'HOF', 'GLA', 'STU', 'KAR', 'BOC', 'FRE', 'NUR', 'MAI', 'KAI', 'STP', 'AUG', 'FDU', 'GRF', 'BRA', 'PAD', 'ING', 'DAR', 'ATA', 'SIE', 'CAG', 'LAZ', 'CAT', 'GEN', 'CHI', 'REG', 'FIO', 'JUV', 'ACM', 'BOL', 'ROM', 'NAP', 'SAM', 'INT', 'TOR', 'LEC', 'UDI', 'PAL', 'BAR', 'LIV', 'PAR', 'CES', 'BRE', 'NOV', 'PES', 'VER', 'SAS', 'EMP', 'FRO', 'CAP', 'VIT', 'GRO', 'ROD', 'TWE', 'WII', 'AJA', 'NEC', 'GRA', 'UTR', 'PSV', 'HER', 'FEY', 'SPA', 'HAA', 'VOL', 'HEE', 'ALK', 'NAC', 'RKC', 'VEN', 'EXC', 'ZWO', 'CAM', 'GAE', 'DOR', 'WIS', 'POB', 'GOR', 'CHO', 'LEG', 'PWA', 'SLA', 'LGD', 'LOD', 'ODR', 'POZ', 'BEL', 'ARK', 'BIA', 'PIG', 'CKR', 'KKI', 'ZAG', 'WID', 'POD', 'POG', 'ZAW', 'LEC', 'TBN', 'POR', 'BEL', 'SCP', 'TRO', 'GUI', 'SET', 'FER', 'BRA', 'AMA', 'ACA', 'RA', 'BEN', 'LEI', 'NAC', 'NAV', 'MAR', 'ULE', 'OLH', 'POR', 'B-M', 'FEI', 'GV', 'MOR', 'EST', 'ARO', 'PEN', 'BOA', 'MAD', 'TON', 'FAL', 'RAN', 'HEA', 'MOT', 'KIL', 'HIB', 'ABE', 'INV', 'CEL', 'MIR', 'HAM', 'DUU', 'JOH', 'DUN', 'DUF', 'ROS', 'PAR', 'VAL', 'MAL', 'OSA', 'VIL', 'COR', 'REA', 'NUM', 'BAR', 'SAN', 'SEV', 'SPG', 'GET', 'BET', 'HUE', 'ESP', 'VAL', 'BIL', 'ALM', 'AMA', 'MAL', 'XER', 'ZAR', 'TEN', 'HER', 'LEV', 'SOC', 'GRA', 'RAY', 'CEL', 'ELC', 'EIB', 'COR', 'LAS', 'GRA', 'BEL', 'YB', 'BAS', 'AAR', 'SIO', 'LUZ', 'VAD', 'XAM', 'ZUR', 'GAL', 'THU', 'SER', 'LAU', 'LUG']