import xlwings
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
import itertools
import sqlite3
from itertools import groupby


def show_name_table():
    groups = ['group-a', 'group-b', 'group-b2', 'group-c']
    return groups


def show_table():
    valz = []
    season = 1
    group = 1
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_group.groupz_id, user.first_name, user_duel.result, user_duel.against, user_duel.points, user_duel.checked, user.id FROM user_duel JOIN duel ON duel.id = user_duel.duel_id JOIN user ON user_duel.user_id = user.id JOIN user_group ON user_group.user_id = user.id JOIN season ON season.id = duel.season_id WHERE season.id = 1")
    groups = cursor.fetchall()
    connection.commit()
    connection.close()
    # print(groups)
    result = {k: [*map(lambda v: v, values)]
              for k, values in groupby(sorted(groups, key=lambda x: x[0]), lambda x: x[0])
              }
    # print(result)
    for group in result.values():

        df = pd.DataFrame(group, columns=['duel_id', 'player', 'plus', 'minus', 'points', 'check', 'user_id'])
        df = df.replace('?', np.NaN)
        df['plusminus'] = df['plus'] - df['minus']
        df = df.groupby(by="player", as_index=False)["points", "plus","minus","plusminus"].sum()
        df = df.sort_values(['points','plus','plusminus'], ascending=False)
        # df['dif'] = df[['plus', 'minus']].agg('/'.join, axis=1)
        df['plusminus2'] = df['plus'].astype(str) +"/"+ df["minus"].astype(str)
        df = df[['player', 'points', 'plusminus2', 'plusminus']]


        # print(df)
        der = df.to_string(index=False)
        der = df.values.tolist()
        valz.append([der])

    return valz
