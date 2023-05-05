from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
import os
from .models import Note, User, Duel, Season, Groupz, Round, user_duel, user_group
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
from sqlalchemy import select, update
from sqlalchemy.orm import lazyload, joinedload, subqueryload
from collections import defaultdict
from itertools import groupby
import random
from random import shuffle
import mysql.connector
from . import conn
import psycopg2
import email


views = Blueprint('views', __name__)

adminz = [21, 22]
season = 1


# @views.route('/returnjson', methods=['GET'])
# def ReturnJSON():
#     if (request.method == 'GET'):
#         with sqlite3.connect('./instance/database.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM user;")
#             data = cursor.fetchall()
#             json.dumps(data)

#         with open('./data.json', 'w+') as file:
#           # First we load existing data into a dict.
#             new_data = json.load(file)
#             # convert back to json.
#             json.dump(new_data, file, indent=4)
#             # return jsonify(data)


# @views.route('/', methods=['GET', 'POST'])
# def main():

#     # user_email = session.get('user_email')
#     # user_id = session.get('user_id')
#     # user_name = session.get('user_name')

#     # dict_log = {
#     #     'id': user_id, 
#     #     'first_name': user_name, 
#     #     'email': user_email,
#     # }

#     dic = dictionary.dic

#     return render_template("main.html", dic=dic, user=current_user, adminz=adminz)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }

    # print(myduels_user[0][0])

    groups = db.session.query(Groupz).join(
        Season).filter(Season.id == season).all()
    round = db.session.query(Groupz.round_id).filter(Groupz.season_id==season).order_by(Groupz.round_id.desc()).first()

    user_group = db.session.query(Groupz).join(User.groupy).filter(
        User.id == current_user.id).filter(Groupz.season_id == Season.id).filter(Season.id == season).filter(Groupz.round_id == round[0]).first()
    
    myduels_user = db.session.query(Groupz.id).join(User.groupy).filter(Groupz.season_id == Season.id).filter(
        Season.id == season).filter(User.id.in_([current_user.id])).filter(Groupz.round_id == round[0]).all()
    
    print(myduels_user)
    
    # myduels_user = db.session.query(User.first_name, user_duel, Duel.round_id).filter(
    #     user_duel.c.user_id == User.id).filter(user_duel.c.duel_id == Duel.id).filter(User.id == current_user.id).all()

    # print(myduels_user)
    if current_user.id in adminz:
        pass
    else:
        new_ret = duels.create_user_duels_list(season, myduels_user[0][0])


    # print(myduels_user[0][0])
    players = User.query.all()
    # print(players)
    data_show_table = tabz.show_table(season, round, round[0])
    # dataAll = tabz.show_table_all()
    data_all = tabz.show_table_all()
    round = db.session.query(Round.id).filter(Season.id==season).order_by(Round.id.desc()).first()
    data_name_tabz = tabz.show_name_table(season, round[0])
    # print(data_show_table)
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

    return render_template("home.html", user_group=user_group, groups=groups, dataAll=data_all, players=players, data_name_tabz=data_name_tabz, data_show_table=data_show_table, user=current_user, adminz=adminz)


# def make_tab_list():
#     length_tab_list = len(tabz.show_name_table(season, 2))
#     return list(range(0, int(length_tab_list)))


@views.route('/delete-note', methods=['POST'])
@login_required
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


@views.route('/update-duel', methods=['POST', 'GET'])
@login_required
def update_duel():
    duelCheck = json.loads(request.data)
    data = duelCheck["duelCheck"]
    data = data.split(",")
    data = (data[0], data[1], data[2])
    print(data)

    u = update(user_duel)
    u = u.values({"checked": data[0]})
    u = u.where(user_duel.c.duel_id == int(data[1]))
    u = u.where(user_duel.c.user_id == int(data[2]))

    db.session.execute(u)
    db.session.commit()
    return jsonify({})


@views.route('/update-duel2', methods=['POST', 'GET'])
@login_required
def update_duel2():
    try:
        duelResult = json.loads(request.data)
        data = duelResult["duelResult"]
        data = data.split(",")
        # print(data)
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

        # dataz = (int(data[0]), int(data[3]), int(points), int(data[1]), int(data[2]))
        # dataz2 = (int(data[3]), int(data[0]), int(points2), int(data[4]), int(data[5]))

        if data:
            # user1 = db.session.query(user_duel).filter(user_duel.c.duel_id == int(
            #     data[1])).filter(user_duel.c.user_id == int(data[2])).first()
            # user2 = db.session.query(user_duel).filter(user_duel.c.duel_id == int(
            #     data[4])).filter(user_duel.c.user_id == int(data[5])).first()
            # print(user1)
            # print(user2)

            u = update(user_duel)
            u = u.values({"result": int(data[0]), "against": int(data[3]), "points": int(points)})
            u = u.where(user_duel.c.duel_id == int(data[1]))
            u = u.where(user_duel.c.user_id == int(data[2]))
            u2 = update(user_duel)
            u2 = u2.values({"result": int(data[3]), "against": int(data[0]), "points": int(points2)})
            u2 = u2.where(user_duel.c.duel_id == int(data[4]))
            u2 = u2.where(user_duel.c.user_id == int(data[5]))

            db.session.execute(u)
            db.session.execute(u2)
            db.session.commit()

            return jsonify({})

    except:
        print('error')



@views.route('/season/<season>/duel/<duelz>', methods=['GET', 'POST'])
@login_required
def duel_id(season, duelz):
    
    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }


    season = 1


    duel = db.session.query(User.first_name, user_duel, Duel.round_id).filter(
        user_duel.c.user_id == User.id).filter(user_duel.c.duel_id == Duel.id).filter(Duel.id == duelz).order_by(User.id.desc()).all()

    roundz = db.session.query(Round).filter(Round.season_id==season).filter(Round.open==True).order_by(Round.id.desc()).first()
    group = db.session.query(User).filter(User.id==user_duel.c.user_id).all()
    print('---------------------')
    print(roundz)
    print('------------------')


    return render_template("duel.html", group=group, roundz=roundz,  duel=duel, players=duelz, user=current_user, adminz=adminz)




@views.route('/season/<season>/round/<round>', methods=['GET', 'POST'])
@login_required
def duel_view(season, round):
    
    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }
    season_obj = Season.query.filter(Season.id==season).first()
    new_ret = duels.create_duels_list(season, round)
    print(len(new_ret))

    # group = db.session.query(Groupz).join(Season).filter(Season.id == season).filter(Groupz.round_id == round).first()
    groups = db.session.query(Groupz).join(Season).filter(Season.id == season).filter(Groupz.round_id == round).all()

    if request.method == 'POST':
        grno2 = request.form.get('grno')
        grname = request.form.get('grname')
        seasons2 = request.form.get('season')
        round2 = request.form.get('round')
        print('------------------------')
        print(grname)
        print(seasons2)
        print(round2)
        print(grno2)
        print('------------------------')
        
        # duel_view(seasons, grno)

        return redirect(url_for('views.duel_view', round=round2, group=grno2, season=seasons2))

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

    return render_template("duels_filter.html", season_obj=season_obj, round=round, groups=groups, season=season, duels=new_ret, user=current_user, adminz=adminz)




@views.route('/season', methods=['GET', 'POST'])
def season_list():

    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }

    seasons = db.session.query(Season).all()
    groupz = db.session.query(Groupz.round_id).all()
    


    if request.method == 'POST':
        season1 = request.form.get('season_id')

        print('ddd')
        return redirect(url_for('views.season_manager', season=season1))

    return render_template("season_list.html", seasons=seasons, user=current_user, adminz=adminz)


@views.route('/season/<season>', methods=['GET', 'POST'])
@login_required
def season_manager(season):

    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }

    rounds = db.session.query(Season, Round).filter(Groupz.season_id==Season.id).filter(Groupz.round_id==Round.id).filter(User.id==user_group.c.user_id).filter(user_group.c.groupz_id==Groupz.id).filter(Season.id==season).order_by(Groupz.round_id.desc()).all()
    groupz = db.session.query(Groupz.round_id).all()
    
    
    dic = dictionary.dic
    
    
    
    if request.method == "POST" and request.form.get('ide_season'):
        season = int(request.form.get('ide_season'))
        print(season)
        if season < 1:
            flash('There is a problem!', category='error')
        else:
            # pass
            create_new_season(season)
            flash('New round was created!!!', category='success')
            return redirect(url_for('views.season_manager', season=season))


    if request.form.get('round'):
        season = int(request.form.get('season'))
        round = int(request.form.get('round'))
        print(round)
        print('---------------')

        if not season:
            flash('There is a problem!', category='error')
        else:
            grno=db.session.query(Groupz.id).filter(Groupz.season_id==season).filter(Groupz.round_id==round).first()
            return redirect(url_for('views.duel_view', round=round, group=grno[0], season=season))

    return render_template("season.html", groupz=groupz, dic=dic, seasons=rounds, user=current_user, adminz=adminz)


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

    list_p = [2, 3, 1, 8, 14, 4, 7, 15, 18, 5, 6, 12,
              16, 11, 19, 23, 24, 10, 25, 26, 28, 29, 30, 31, 32]

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
    last_round = db.session.query(Round).filter(Round.season_id==season).order_by(Round.id.desc()).first()
    # next_round = last_round + 1
    new_round = Round(season_id=season, open=True)
    db.session.add(new_round)
    db.session.commit()

    for i, group in enumerate(groups):
        gr = Groupz(
            name=f'Group {i+1}', shorts=list_groups_shorts[i], season_id=season, round_id=new_round.id)
        db.session.add(gr)
        db.session.commit()

        for player in group:
            player = User.query.get(player.id)
            group_new = Groupz.query.get(gr.id)
            ## missing season and round id
            player.groupy.append(group_new)

        group = random.sample(group, len(group))

        to_duels = list(combinations(group, 2))
        couples2 = []
        for lists in to_duels:

            new_duel = Duel(notice=f'{new_round.id}. kolo', date_duel=datetime.now(), season_id=season, round_id=new_round.id)
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

