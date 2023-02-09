from datetime import datetime
from itertools import combinations
from sqlalchemy.inspection import inspect
import sqlite3
from . import db
from .models import Groupz, Season


def create_duels_list(season, group):

    # print(group)
    groups = db.session.query(Groupz).join(Season).filter(Season.id.like(season)).all()

    
    def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

    connection = sqlite3.connect('instance/database.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute('''
    SELECT user_duel.duel_id, user_duel.result, user_duel.user_id, user_duel.checked, user.first_name, user_group.groupz_id 
    FROM duel 
    JOIN user_duel ON duel.id = user_duel.duel_id 
    JOIN user ON user.id = user_duel.user_id 
    JOIN user_group ON user.id = user_group.user_id 
    JOIN groupz ON groupz.id=user_group.groupz_id 
    JOIN round ON round.id = groupz.round_id
    WHERE duel.season_id=? AND groupz.id=? AND duel.id > 100
    GROUP BY duel.id, user.id
    ''', (season,group))

    duels = cursor.fetchall()

    print('------------------------------')
    print(duels)
    print('------------------------------')


    connection.commit()
    connection.close()

    # duels = {key:np.hstack([d1[key],d2[key]]) for key in d1.keys()}
    # dd = defaultdict(list)

    field_to_be_check = "duel_id"
    merger = ["first_name", "result", "groupz_id", "checked", "user_id"]
    merge_name = ["player", "result_", "groupy", "checking", "useride"]

    # merger and merge_name must be one to one.
    the_dict = {m: mn for m, mn in zip(merger, merge_name)}
    # {"city":"cities", "ads":"my_ads"}  merge_name
    newdata = duels.copy()
    # create new_ret as result
    new_ret = [{field_to_be_check: i, **{i: [] for i in merge_name}}
            for i in set([i[field_to_be_check] for i in duels])]
    # print(new_ret, "this is new_ret")
    for val in new_ret:
        for k in newdata:
            if val[field_to_be_check] != k[field_to_be_check]:
                continue
            tmp = {i: k[i] for i in merger}
            for single in tmp:
                # if {single:tmp[single]} not in val[the_dict[single]]:
                val[the_dict[single]].append({single: tmp[single]})
    
        
    return new_ret