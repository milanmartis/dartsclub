import xlwings
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
import itertools
import sqlite3
from itertools import groupby
from .models import Groupz, Season, User
from . import db

def show_name_table(season):
    
    groups = db.session.query(Groupz).join(Season).filter(Season.id.like(season[0])).all()

    # groups = ['group-a', 'group-b', 'group-b2', 'group-c']

    return groups


def show_table(season, groupz):
    
    # print(season)
    # print(groupz)
    valz = []
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT user_group.groupz_id, user.first_name, user_duel.result, user_duel.against, 
    user_duel.points, user_duel.checked, user.id, 

    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.addons ELSE 0 END) AS c_duel,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.points ELSE 0 END) AS s_points,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.result ELSE 0 END) AS s_result,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.against ELSE 0 END) AS s_against

    FROM user_duel 
    JOIN duel ON duel.id = user_duel.duel_id 
    JOIN user ON user_duel.user_id = user.id 
    JOIN user_group ON user_group.user_id = user.id 
    JOIN season ON season.id = duel.season_id 
    WHERE season.id = ? 
    GROUP BY user_group.user_id, user_duel.user_id
    ''', (season))
    groups = cursor.fetchall()
    connection.commit()
    connection.close()
    # print(groups)
    result = {k: [*map(lambda v: v, values)]
              for k, values in groupby(sorted(groups, key=lambda x: x[0]), lambda x: x[0])
              }
    # print(result)
    for group in result.values():

        df = pd.DataFrame(group, columns=['duel_id', 'player', 'plus', 'minus', 'points', 'check', 'user_id','c_duel','s_points','s_result','s_against'])
        # df = df.replace('?', np.NaN)
        df['plusminus'] = df['s_result'] - df['s_against']
        df = df.fillna(0).groupby(by="player", as_index=False)["c_duel", "s_points", "s_result","s_against","plusminus"].sum()
        df = df.sort_values(['s_points','s_result','plusminus'], ascending=False)
        # df['dif'] = df[['plus', 'minus']].agg('/'.join, axis=1)
        df['plusminus2'] = df['s_result'].astype(str) +"/"+ df["s_against"].astype(str)
        df = df[['player', 'c_duel', 'plusminus2', 'plusminus', 's_points']]


        # print(df)
        der = df.to_string(index=False)
        der = df.values.tolist()
        valz.append([der])

    return valz



def show_table_all():
    valz = []
    season = [1]
    group = 1
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT user_group.groupz_id, user.first_name, user_duel.result, user_duel.against, 
    user_duel.points, user_duel.checked, user.id, 

    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.addons ELSE 0 END) AS c_duel,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.points ELSE 0 END) AS s_points,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.result ELSE 0 END) AS s_result,
    SUM(CASE WHEN user_duel.checked = "true" THEN user_duel.against ELSE 0 END) AS s_against

    FROM user_duel 
    JOIN duel ON duel.id = user_duel.duel_id 
    JOIN user ON user_duel.user_id = user.id 
    JOIN user_group ON user_group.user_id = user.id 
    JOIN season ON season.id = duel.season_id 
    WHERE season.id = ? 
    GROUP BY user_duel.user_id

    ''', (season))
    groups = cursor.fetchall()
    connection.commit()
    connection.close()
    # print(groups)
    result = {k: [*map(lambda v: v, values)]
              for k, values in groupby(sorted(groups, key=lambda x: x[0]), lambda x: x[0])
              }
    # print(result)
    for group in result.values():

        df = pd.DataFrame(group, columns=['duel_id', 'player', 'plus', 'minus', 'points', 'check', 'user_id','c_duel','s_points','s_result','s_against'])
        df = df.replace('?', np.NaN)
        df['plusminus'] = df['s_result'] - df['s_against']
        df = df.fillna(0).groupby(by="player", as_index=False)["c_duel", "s_points", "s_result","s_against","plusminus"].sum()
        df = df.sort_values(['s_points','s_result','plusminus'], ascending=False)
        # df['dif'] = df[['plus', 'minus']].agg('/'.join, axis=1)
        df['plusminus2'] = df['s_result'].astype(str) +"/"+ df["s_against"].astype(str)
        df = df[['player', 'c_duel', 'plusminus2', 'plusminus', 's_points']]


        # print(df)
        der = df.to_string(index=False)
        der = df.values.tolist()
        valz.append([der])

    return valz
