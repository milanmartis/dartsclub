from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import os
from .models import Note, User, Duel, Season, Groupz, Round
from . import db
import json
from . import tabz, duels, dictionary, mysql
from datetime import datetime
from itertools import combinations
from sqlalchemy.inspection import inspect
import sqlite3
from flask import jsonify
import numbers
from sqlalchemy.inspection import inspect
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload, subqueryload
from collections import defaultdict
from itertools import groupby
import random
from random import shuffle
import mysql.connector


views = Blueprint('views', __name__)

adminz = [21, 22]
season = [1]


@views.route('/', methods=['GET', 'POST'])
def main():


    dic = dictionary.dic

    return render_template("main.html", dic=dic, user=current_user, adminz=adminz)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    # print(myduels_user[0][0])

    groups = db.session.query(Groupz).join(
        Season).filter(Season.id.like(season[0])).all()

    # print(user_group)
    user_group = db.session.query(Groupz).join(User.groupy).filter(
        User.id.like(current_user.id)).filter(Season.id.like(season[0])).filter(Groupz.round_id == 2).first()
    myduels_user = db.session.query(Groupz.id).join(User.groupy).filter(
        Season.id.like(season[0])).filter(User.id.in_([current_user.id])).filter(Groupz.round_id.like(2)).all()


    print(myduels_user)
    if current_user.id in adminz:
        # user_group = 7
        new_ret = duels.create_duels_list(season[0], 'visitor')
        shearch_table = 111
    else:
        new_ret = duels.create_duels_list(season[0], myduels_user[0][0])
        shearch_table = myduels_user[0][0]


    players = User.query.all()
    data_show_table = tabz.show_table(season, shearch_table)
    # dataAll = tabz.show_table_all()
    data_all = tabz.show_table_all()
    data_name_tabz = tabz.show_name_table(season)
    # print(data_name_tabz)
    # fooor = make_tab_list()

    if request.method == "POST" and request.form.get("duelz"):

        duelz_players = []
        # flash('Lets play!!!', category='success')

        duelz = request.form.get("duelz")
        duelz_players = request.form.get("duelz_players")

        # duel_players = db.session.query(User)\
        #          .join(User.seasony)\
        #          .filter(Duel.id.like(duelz))\
        #          .first()

        return redirect(url_for('views.duel_id', season=season, duelz=duelz, duelz_players=duelz_players))

    return render_template("home.html", user_group=user_group, groups=groups, dataAll=data_all, duels=new_ret, players=players, data_name_tabz=data_name_tabz, data_show_table=data_show_table, user=current_user, adminz=adminz)


# def make_tab_list():
#     length_tab_list = len(tabz.show_name_table(season, 2))
#     return list(range(0, int(length_tab_list)))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-duel', methods=['POST'])
@login_required
def delete_duel():
    duel = json.loads(request.data)
    duelId = duel['duelId']
    duel = Duel.query.get(duelId)
    if duel:
        db.session.delete(duel)
        db.session.commit()

    return jsonify({})


@views.route('/update-duel', methods=['POST'])
@login_required
def update_duel():
    duelCheck = json.loads(request.data)
    data = duelCheck["duelCheck"]
    data = data.split(",")
    data = (data[0], data[1], data[2])
    # print(data)
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_duel SET checked = ? WHERE duel_id = ? AND user_id = ?", data)
    conn.commit()
    conn.close()
    # if data[0] == 'true':
    #     flash('Duel checked!', category='success')
    # else:
    #     flash('Duel unchecked!', category='success')

    return jsonify({})


@views.route('/update-duel2', methods=['POST'])
@login_required
def update_duel2():
    try:
        duelResult = json.loads(request.data)
        data = duelResult["duelResult"]
        data = data.split(",")

        # calculating points
        if int(data[0]) == 6 and int(data[3]) <= 4:
            points = 2
        elif int(data[0]) == 6 and int(data[3]) == 5:
            points = 2
        elif int(data[0]) == 5 and int(data[3]) == 6:
            points = 1
        elif int(data[0]) <= 4 and int(data[3]) == 6:
            points = 0
        elif int(data[0]) == 4 and int(data[3]) == 0:
            points = 2
        elif int(data[0]) == 0 and int(data[3]) == 0:
            points = 0
        else:
            points = 0

        if int(data[3]) == 6 and int(data[0]) <= 4:
            points2 = 2
        elif int(data[3]) == 6 and int(data[0]) == 5:
            points2 = 2
        elif int(data[3]) == 5 and int(data[0]) == 6:
            points2 = 1
        elif int(data[3]) <= 4 and int(data[0]) == 6:
            points2 = 0
        elif int(data[3]) == 4 and int(data[0]) == 0:
            points2 = 2
        elif int(data[3]) == 0 and int(data[0]) == 0:
            points2 = 0
        else:
            points2 = 0

        dataz = (int(data[0]), int(data[3]), int(
            points), int(data[1]), int(data[2]))
        dataz2 = (int(data[3]), int(data[0]), int(
            points2), int(data[4]), int(data[5]))
        # print(dataz)
        # print(dataz2)

        if data:

            conn = sqlite3.connect('instance/database.db')
            cur1 = conn.cursor()
            cur1.execute(
                "UPDATE user_duel SET result = ?, against = ?, points = ? WHERE duel_id = ? AND user_id = ?", (dataz))
            cur2 = conn.cursor()
            cur2.execute(
                "UPDATE user_duel SET result = ?, against = ?, points = ? WHERE duel_id = ? AND user_id = ?", (dataz2))
            conn.commit()
            conn.close()
            return jsonify({})
            # fetch the user, perform the updates and commit
        # return jsonify(success=1)
    except:
        print('error')
        # flash('Duel was not updated!', category='error')


# /landingpage/A
@views.route('/season/<season>/duel/<duelz>', methods=['GET', 'POST'])
@login_required
def duel_id(season, duelz):

    season = 1

    # duel = Duel.query.join(User.play).filter(User.id == current_user.id).filter(Duel.id == duelz).first()
    # if request.method == 'POST':
    #     user_duel_id = request.form.get('user_duel_id')
    #     user_duel_result = request.form.get('user_duel_result')

    #     if user_duel_id=='':
    #         flash('Something wrong!', category='error')
    #     else:

    #         # course_id = db.session.query(Duel.id).filter(Duel.play.in_(user_duel)).all()
    #         conn = sqlite3.connect('instance/database.db')
    #         cur = conn.cursor()
    #         data = (user_duel_result, duelz, user_duel_id)
    #         # print(data)
    #         cur.execute("UPDATE user_duel SET result = ? WHERE duel_id = ? AND user_id = ?", data)
    #         conn.commit()
    #         conn.close()

    # flash('Duel updated!!!', category='success')

    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    cursor.execute(
        f'''
        SELECT user.id, user.first_name, user_duel.result, duel.date_duel, user.id, user_duel.checked, user_duel.duel_id, user_group.groupz_id  
        FROM user 
        JOIN user_duel ON user.id = user_duel.user_id
        JOIN duel ON duel.id = user_duel.duel_id 
        JOIN user_group ON user_group.user_id = user_duel.user_id 
        WHERE user_duel.duel_id = {duelz}
        GROUP BY user_duel.duel_id, user.id
  
        '''
    )
    duel = cursor.fetchall()
    connection.commit()
    connection.close()

    print(duel)


    groups = db.session.query(Groupz).join(
        Season).filter(Season.id.like(season)).filter(Groupz.round_id.like(2)).all()

    return render_template("duel.html", groups=groups, duel=duel, players=duelz, user=current_user, adminz=adminz)


# /landingpage/A
@views.route('/season/<season>/group/<group>', methods=['GET', 'POST'])
@login_required
def duel_view(season, group):


    new_ret = duels.create_duels_list(season, group)
    # print(new_ret)

    group = db.session.query(Groupz).join(Season).filter(
        Season.id.like(season)).filter(Groupz.id.like(group)).first()
    groups = db.session.query(Groupz).join(
        Season).filter(Season.id.like(season)).filter(Groupz.round_id.like(2)).all()

    if request.method == 'POST' and request.form.get('grno'):
        grno = request.form.get('grno')
        grname = request.form.get('grname')
        seasons = request.form.get('seasons')
        # duel_view(seasons, grno)

        return redirect(url_for('views.duel_view', groups=groups, group=grno, grno=grno, grname=grname, season=seasons, user=current_user, adminz=adminz))

    if request.method == "POST" and request.form.get("duelz"):

        duelz_players = []
        # flash('Lets play!!!', category='success')

        duelz = request.form.get("duelz")
        duelz_players = request.form.get("duelz_players")

        # duel_players = db.session.query(User)\
        #          .join(User.seasony)\
        #          .filter(Duel.id.like(duelz))\
        #          .first()

        return redirect(url_for('views.duel_id', season=season, duelz=duelz, duelz_players=duelz_players))

    return render_template("duels_filter.html", group=group, groups=groups, season=season, duels=new_ret, user=current_user, adminz=adminz)


@views.route('/season/<season>', methods=['GET', 'POST'])
@login_required
def duel_manager(season):

    groups = db.session.query(Groupz).join(
        Season).filter(Season.id.like(season)).all()
    group = db.session.query(Groupz.id).join(
        Season).filter(Season.id.like(season)).first()

    # print("-------------------------------")
    # print(group)
    # print("-------------------------------")

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
    WHERE duel.season_id=? AND groupz.id=?
    GROUP BY duel.id, user.id
    ''', (season, group[0]))

    duels = cursor.fetchall()

    # print(duels)

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
    # duel_view(season,group)

    # CHOOSE GROUP
    # if request.data:
    #     groupList = json.loads(request.data)
    #     data = groupList["groupList"]
    #     data = data.split(",")
    if request.method == 'POST' and request.form.get('grno'):
        grno = request.form.get('grno')
        grname = request.form.get('grname')
        seasons = request.form.get('seasons')
        # duel_view(seasons, grno)

        return redirect(url_for('views.duel_view', groups=groups, group=grno, grno=grno, grname=grname, season=seasons, user=current_user, adminz=adminz))
        # return render_template("duels_filter.html", duels=new_ret, season=season, groups=groups, user=current_user, adminz=adminz)

    if request.method == "POST" and request.form.get("duelz"):

        duelz_players = []
        # flash('Lets play!!!', category='success')

        duelz = request.form.get("duelz")
        duelz_players = request.form.get("duelz_players")

        # duel_players = db.session.query(User)\
        #          .join(User.seasony)\
        #          .filter(Duel.id.like(duelz))\
        #          .first()

        return redirect(url_for('views.duel_id', group=group, season=season, duelz=duelz, duelz_players=duelz_players))

    # CHOOS DUEL

    return render_template("duels_filter.html", duels=new_ret, season=season, groups=groups, user=current_user, adminz=adminz)


@views.route('/season', methods=['GET', 'POST'])
# @login_required
def season_manager():


    # mdb = mysql.connect_tcp_socket()

    # database=mysql.connector.connect(host='35.240.52.3',user='root',passwd='Babkapesko.1',database='darts', )
    # cursor=database.cursor()
    # query="select * from posts"
    # cursor.execute(query)
    # database.commit()
    

    # print(mdb_results)

    seasons = Season.query.all()
    dic = dictionary.dic

    # pokus = db.session.query(Duel).join(User).all()

    if request.method == 'POST' and request.form.get('ide_season'):
        season = int(request.form.get('ide_season'))

        if season < 1:
            flash('There is a problem!', category='error')
        else:
            create_new_season(season)
            flash('Season was not created!!!', category='success')
            # return redirect(url_for('views.duel_manager', season=season))

    if request.method == 'POST' and request.form.get('season'):
        season = int(request.form.get('season'))

        if season < 1:
            flash('There is a problem!', category='error')
        else:
            return redirect(url_for('views.duel_view', group=8, season=season))

    return render_template("season.html", dic=dic, seasons=seasons, user=current_user, adminz=adminz)


def create_new_season(season):

    # my_list_of_ids = [16, 17, 18, 19, 20]
    # players = User.query.filter(User.id.in_(my_list_of_ids)).all()

    # players = db.session.query(User)\
    #     .join(User.seasony)\
    #     .filter(Season.id.like(season))\
    #     .order_by(User.groupy.order.asc())\
    #     .all()

    # connection = sqlite3.connect('instance/database.db')
    # cursor = connection.cursor()
    # cursor.execute('''
    # SELECT user.id FROM user
    # JOIN user_season ON user.id = user_season.user_id
    # WHERE user_season.season_id = '1' ORDER BY user_season.orderz ASC
    # ''')
    # players = cursor.fetchall()
    # connection.commit()
    # connection.close()

    list_p = [2, 3, 1, 8, 14, 4, 7, 15, 18, 9, 5, 6, 12, 16, 13, 11, 19, 23, 24, 20, 10, 17, 25, 26, 27]

    players = db.session.query(User)\
        .filter(User.id.in_(list_p))\
        .order_by(User.orderz.asc())\
        .group_by(User.id)\
        .all()

    # print(players)
    # players = tabz.show_table_all()

    def divide_to_groups(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    n = 5
    groups = list(divide_to_groups(players, n))
    # print(groups)

    list_groups_shorts = ['A', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']

    for i, group in enumerate(groups):
        gr = Groupz(
            name=f'Group {i+1}', shorts=list_groups_shorts[i], season_id=season, round_id=2)
        db.session.add(gr)
        db.session.commit()

        for player in group:
            player = User.query.get(player.id)
            group_new = Groupz.query.get(gr.id)
            player.groupy.append(group_new)

        group = random.sample(group, len(group))

        to_duels = list(combinations(group, 2))
        couples2 = []
        for lists in to_duels:

            new_duel = Duel(date_duel=datetime.now(), season_id=season)
            db.session.add(new_duel)
            db.session.commit()

            couples = []
            for combo in lists:
                couples.append(new_duel.id)
                couples.append(combo.id)

            couples2.append(couples)

            for co_player in lists:
                duel = Duel.query.get(new_duel.id)
                player = User.query.get(co_player.id)
                player.play.append(duel)
                db.session.commit()
                # player2.play.append(duel2)

    db.session.commit()


# from website import db
# from website.models import User, Duel, OpenHour
# db.create_all()
# from website.models import User, Duel, OpenHour
# from datetime import datetime
# duel = Duel(date_duel=datetime(2012, 3, 3, 10, 10, 10))

# openhour = OpenHour(oh_from=datetime(2012, 3, 3, 10, 10, 10), oh_to=datetime(2012, 3, 3, 10, 10, 10), duel=duel)
# db.session.add_all([duel,openhour])
# db.session.commit()

# players = User.query.all()

#     season = Season.query.get(1)

#     for player in players:
#         player = User.query.get(player.id)
#         season = Season.query.get(season.id)
#         player.seasony.append(season)

#     db.session.commit()
