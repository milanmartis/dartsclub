from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import os
from .models import Note, User, Duel, Season, Groupz
from . import db
import json
from . import tabz
from datetime import datetime
from itertools import combinations
from sqlalchemy.inspection import inspect
import sqlite3
from flask import jsonify
import numbers



views = Blueprint('views', __name__)

adminz = 21

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # if request.method == 'POST':
    #    note = request.form.get('note')

    #    if len(note) < 1:
    #        flash('Note is too short!', category='error')
    #    else:
    #        new_note = Note(data=note, user_id=current_user.id)
    #        db.session.add(new_note)
    #        db.session.commit()
    #        flash('Note added!', category='success')

    if request.method == 'POST':
        duel = request.form.get('duel')

        if len(duel) < 1:
            flash('Duel is too short!', category='error')
        else:
            new_duel = Duel(date_duel=datetime.now())
            db.session.add(new_duel)
            db.session.commit()
            flash('Duel added!!!!!!!', category='success')

    duels = Duel.query.all()
    players = User.query.all()
    data123 = tabz.show_table()
    # data_all = tabz.show_table_all()
    data_name_tabz = tabz.show_name_table()
    fooor = make_tab_list()
    return render_template("home.html", duels=duels, fooor=fooor, players=players, data_name_tabz=data_name_tabz, data123=data123, user=current_user)

def make_tab_list():
    length_tab_list = len(tabz.show_name_table())
    return list(range(0, int(length_tab_list)))


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
def delete_duel():
    duel = json.loads(request.data)
    duelId = duel['duelId']
    duel = Duel.query.get(duelId)
    if duel:
        db.session.delete(duel)
        db.session.commit()

    return jsonify({})


@views.route('/update-duel', methods=['POST'])
def update_duel():
    duelCheck = json.loads(request.data)
    data = duelCheck["duelCheck"]
    data = data.split(",")
    data = (data[0], data[1], data[2])
    print(data)
    conn = sqlite3.connect('instance/database.db')
    cur = conn.cursor()
    cur.execute("UPDATE user_duel SET checked = ? WHERE duel_id = ? AND user_id = ?", data)
    conn.commit()
    conn.close()
    # if data[0] == 'true':
    #     flash('Duel checked!', category='success') 
    # else:
    #     flash('Duel unchecked!', category='success') 


    return jsonify({})

@views.route('/update-duel2', methods=['POST'])
def update_duel2():
    try:
        duelResult = json.loads(request.data)
        data = duelResult["duelResult"]
        data = data.split(",")
        connection = sqlite3.connect('instance/database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT user_duel.result, user_duel.user_id FROM user_duel WHERE user_duel.duel_id = ? and user_duel.user_id != ?", (data[1], data[2]))
        opponent = cursor.fetchall()
        connection.commit()
        connection.close()   
        opponent_result = opponent[0][0]
        opponent_id = opponent[0][1]

        # calculating points
        if int(data[0]) == 6 and int(opponent_result)<=4:
            points = 3
        elif int(data[0]) == 6 and int(opponent_result)==5:
            points = 2
        elif int(data[0]) == 5 and int(opponent_result)==6:
            points = 1
        elif int(data[0]) <= 4 and int(opponent_result)==6:
            points = 0
        elif int(data[0]) == 4 and int(opponent_result)==0:
            points = 2
        else:
            points = 0

        if int(opponent_result) == 6 and int(data[0])<=4:
            points2 = 3
        elif int(opponent_result) == 6 and int(data[0])==5:
            points2 = 2
        elif int(opponent_result) == 5 and int(data[0])==6:
            points2 = 1
        elif int(opponent_result) <= 4 and int(data[0])==6:
            points2 = 0
        elif int(opponent_result) == 4 and int(data[0])==0:
            points2 = 2
        else:
            points2 = 0


        # print(f"{opponent} - {data[0]}")

        data = (data[0], points, data[1], data[2])
        data2 = (opponent_result, points2, data[1], opponent_id)
        if data:
            # flash('Duel updated!', category='success') 
            # print(data)
            conn = sqlite3.connect('instance/database.db')
            cur = conn.cursor()
            cur.execute(f"UPDATE user_duel SET result = ?, against = {opponent_result}, points = ?, checked='false' WHERE duel_id = ? AND user_id = ?", data)
            cur = conn.cursor()
            cur.execute(f"UPDATE user_duel SET result = ?, against = {data[0]}, points = ?, checked='false' WHERE duel_id = ? AND user_id = ?", data2)
            conn.commit()
            conn.close()
            return jsonify({})
            # fetch the user, perform the updates and commit
        # return jsonify(success=1)
    except:
        print('error')
        # flash('Duel was not updated!', category='error')



@views.route('/season/duel/<duelz>', methods=['GET', 'POST'])  # /landingpage/A
def duel_id(duelz):
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
    cursor.execute(f"SELECT user.id, user.first_name, user_duel.result, duel.date_duel, user.id, user_duel.checked, user_duel.duel_id FROM user JOIN Duel ON duel.id = user_duel.duel_id JOIN user_duel ON user.id = user_duel.user_id AND user_duel.duel_id = {duelz}")
    duel = cursor.fetchall()
    connection.commit()
    connection.close()   

    return render_template("duel.html", duel=duel, players=duelz, user=current_user, adminz=adminz)



@views.route('/season/<season>', methods=['GET', 'POST'])
@login_required
def duel_manager(season):

    duels = Duel.query.join(User.play).filter(Season.id == season).order_by(Duel.id.asc()).all()
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_duel.duel_id, user.id, user_duel.result, user_duel.user_id, user_duel.checked, user.first_name FROM user JOIN Duel ON duel.id = user_duel.duel_id JOIN user_duel ON user.id = user_duel.user_id WHERE duel.season_id=? GROUP BY duel.id, user.id",season)
    duel = cursor.fetchall()
    connection.commit()
    connection.close()  
    # duels = Duel.query.join(User.play).filter(User.id == current_user.id).filter(Season.id == season).order_by(Duel.id.desc()).all()

    if request.method == "POST":

        duelz_players=[]
        flash('Lets play!!!', category='success')

        duelz = request.form.get("duelz")
        duelz_players = request.form.get("duelz_players")

        # duel_players = db.session.query(User)\
        #          .join(User.seasony)\
        #          .filter(Duel.id.like(duelz))\
        #          .first()

        return redirect(url_for('views.duel_id', duelz=duelz, duelz_players=duelz_players))


    return render_template("duels.html", duel=duel, duels=duels, user=current_user, adminz=adminz)



@views.route('/season', methods=['GET', 'POST'])
@login_required
def season_manager():


    seasons = Season.query.all()

    if request.method == 'POST':
        season = int(request.form.get('ide_season'))

        if season < 1:
            flash('There is a problem!', category='error')
        else:
            # create_new_season(season)
            # flash('Season was created!!!', category='success')
            return redirect(url_for('views.duel_manager', season=season))

    return render_template("season.html", seasons=seasons, user=current_user)


def create_new_season(season):

    my_list_of_ids = [16,17,18,19,20]
    players = User.query.filter(User.id.in_(my_list_of_ids)).all()

    players = db.session.query(User)\
                 .join(User.seasony)\
                 .filter(Season.id.like(season))\
                 .order_by(User.id.asc())\
                 .all()

    def divide_to_groups(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
    n = 5
    groups = list(divide_to_groups(players, n))
  
    for i, group in enumerate(groups):
        gr = Groupz(name=f'Group {i+1}', season_id=season)
        db.session.add(gr)
        db.session.commit()


        for player in group:
            player = User.query.get(player.id)
            group_new = Groupz.query.get(gr.id)
            player.groupy.append(group_new)

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

