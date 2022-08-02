# See European Soccer Game Analysis from https://www.projectpro.io/article/sql-database-projects-for-data-analysis-to-practice/565
# Kaggle data set: https://www.kaggle.com/code/dimarudov/data-analysis-using-sql/data

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

####################### For a given team (takes the short name as a parameter), plot the average goals per game the team gets over time (by year).

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

####################### Just the count of how many teams a player has been on.

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
    return pd.read_sql(full_query, conn)

def all_player_teams_abb():
    players = pd.read_sql("SELECT * FROM Player;",conn)["player_name"].to_list()
    for i in range(len(players)):
        num_teams = player_teams_abb(players[i])["COUNT(TeamNumber)"][0]
        print(players[i] + ": " + str(num_teams) + " team(s).")
#all_player_teams_abb()

####################### Same as above, but for all players at once. Produce a histogram of the number of teams that players are on.

def player_teams_subquery_all(home_away, player_position):
    return """
        SELECT Player.player_name, Match.{0}_team_api_id AS 'TeamNumber'
        FROM Player JOIN Match ON Player.player_api_id = Match.{0}_player_{1}
    """.format(home_away, player_position)
  
def player_teams_all():
    sub_query = "\nUNION\n".join(
        [player_teams_subquery_all("home",i) for i in range(1,12)] +
        [player_teams_subquery_all("away",i) for i in range(1,12)]
    )
    full_query = """
        WITH Teams AS ({0})
        SELECT player_name, COUNT(TeamNumber) AS num_teams FROM Teams
        GROUP BY player_name
    ;""".format(sub_query)
    return pd.read_sql(full_query, conn)

def all_player_teams_all():
    table = player_teams_all()
    table = table.sort_values(by=['num_teams'], ignore_index=True)
    max_number_teams = table["num_teams"][10847]
    num_teams = table["num_teams"]
    plt.title("Number of teams by players")
    plt.hist(num_teams, width=0.75, bins=np.arange(1,max_number_teams+1)-0.375)
    plt.ylabel("Number of Players")
    plt.xlabel("Number of Teams")
    plt.xticks(np.arange(1,max_number_teams+1))
    plt.show()
    
all_player_teams_all()

