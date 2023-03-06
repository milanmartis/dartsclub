from flask import Blueprint, render_template, request, flash, redirect, url_for, session, app, jsonify
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
import bcrypt
import uuid
import jwt
import datetime
from functools import wraps
# def redirect_dest(fallback):
#     dest = request.args.get('next')
#     try:
#         dest_url = url_for(dest)
#     except:
#         return redirect(fallback)
#     return redirect(dest_url)


# @auth.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = datetime.timedelta(minutes=20)
#     session.modified = True



# @auth.after_request
# def add_header(response):
#     response.headers["Cache-Control"] = "no-store, max-age=0"
#     return response
   
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       token = session.get('token')
       user_id = session.get('user_id')
       if not token:
           return redirect(url_for("auth.login", user=None))
           
        #    return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, 'jiuhihuhiuhgftfuyi564dfsff5ss5f421s5', algorithms=["HS256"])
           current_user = User.query.filter_by(id=user_id).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator



@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST' and request.form.get('email'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if check_password_hash(user.password, password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)
            flash('Logged in successfuly!', category='success')


            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, 'jiuhihuhiuhgftfuyi564dfsff5ss5f421s5', "HS256")
            session['token'] = token
            session['user_id'] = user.id
            # return jsonify({'token' : token})
 
            # return make_response('could not verify',  401, {'Authentication': '"login required"'})
            return redirect(url_for("views.home", user=current_user, token=token))
        else:
            flash('Sorry, but you could not log in.', category='error')
            # return redirect('/login')
            # return render_template("auth.login")
        
        print(current_user)


    return render_template("users/login.html", user=current_user)


@auth.route('/logout')
@token_required

def logout(current_user):
    # current_user.is_anonymous=True
    # current_user.is_authenticated=False
    # current_user.is_anonymous=True
    # session["user_email"] = None
    # session["user_id"] = None
    # session["user_name"] = None
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    session.clear()
    logout_user()
    print(current_user)
    # if session.get('was_once_logged_in'):
    #     del session['was_once_logged_in']
    # # return redirect(url_for('auth.login'))
    # next = request.args.get('next')
    return redirect(url_for('auth.login'))


@auth.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', None)
        first_name = request.form.get('first_name', None)
        password1 = request.form.get('password1', None)
        password2 = request.form.get('password2', None)
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 chars", category="error")
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 chars", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match", category="error")
        elif len(password1) < 7:
            flash("Passwords must be at least 7 chars", category="error")
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)

            flash("Account created", category="success")
            return redirect(url_for('auth.login'))
            # add user to database
    return render_template("users/sign_up.html", user=current_user)


@auth.route('/account', methods=['GET', 'POST'])
@token_required

def user_details(current_user):

    
    if request.method == 'POST':

        useride = request.form.get('useride')
        # email = request.form.get('email')
        first_name = request.form.get('first_name_update')

        password_old = request.form.get('password_old')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.get(useride)
        # print(user)
        if user == '':
           flash('This user doesn\'t exist.', category='error')
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 chars", category="error")
        else:
            if password1 !='':
                if not check_password_hash(user.password, password_old):
                    flash('Old password is not correct!', category='error')
                elif password1 != password2:
                    flash("New passwords don\'t match", category="error")
                elif password_old == password2:
                    flash("New password must be different", category="error")
                elif len(password1) < 7:
                    flash("New passwords must be at least 7 chars", category="error")
                else:
                    user.password = generate_password_hash(password1, method='sha256')
                    user.first_name = first_name
                    session["user_name"] = first_name

                    db.session.commit()
                    login_user(user, remember=True)

                    flash("Account updated!", category="success")
                    return redirect(url_for('auth.user_details'))
            else:
                user.first_name = first_name
                session["user_name"] = first_name
                db.session.commit()
                login_user(user, remember=True)

                flash("Account updated!", category="success")
                return redirect(url_for('auth.user_details'))

    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }
        
    return render_template("users/account.html", user=current_user)



@auth.route('/my-stats', methods=['GET', 'POST'])
@login_required
def user_stats():
        


        return render_template("users/my-stats.html", user=current_user)
