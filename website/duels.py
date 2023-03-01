from datetime import datetime
from itertools import combinations
from sqlalchemy.inspection import inspect
import sqlite3
import psycopg2
from . import db
from .models import Groupz, Season, Duel, User, Round, user_duel, user_group


def create_duels_list(season, group):

    # print(group)
    groups = db.session.query(Groupz).join(
        Season).filter(Season.id == season).all()

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    duelss = db.session.query(user_duel.c.duel_id, user_duel.c.result, user_duel.c.user_id, user_duel.c.checked, User.first_name, user_group.c.groupz_id)\
        .outerjoin(user_duel)\
        .filter(user_duel.c.user_id == User.id)\
        .filter(user_duel.c.duel_id == Duel.id)\
        .filter(user_group.c.user_id == User.id)\
        .filter(user_group.c.groupz_id == Groupz.id)\
        .filter(Season.id == Duel.season_id)\
        .filter(Duel.round_id == Round.id)\
        .filter(Season.id == season)\
        .filter(Groupz.id == group)\
        .filter(Round.id == 3)\
        .order_by(User.id.desc())
        
    
    duels = []
    # d = {}
    for x, duel in enumerate(duelss):
        duels.append(duel._mapping)


    field_to_be_check = "duel_id"
    merger = ["first_name", "result", "groupz_id", "checked", "user_id"]
    merge_name = ["player", "result_", "groupy", "checking", "useride"]

    the_dict = {m: mn for m, mn in zip(merger, merge_name)}
    newdata = duels.copy()
    new_ret = [{field_to_be_check: i, **{i: [] for i in merge_name}}
               for i in set([i[field_to_be_check] for i in duels])]
    for val in new_ret:
        for k in newdata:
            if val[field_to_be_check] != k[field_to_be_check]:
                continue
            tmp = {i: k[i] for i in merger}
            for single in tmp:
                val[the_dict[single]].append({single: tmp[single]})

    return new_ret
