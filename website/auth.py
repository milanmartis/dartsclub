from flask import Blueprint, render_template, request, flash, redirect, url_for, session, app
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)
import bcrypt
import datetime


# def redirect_dest(fallback):
#     dest = request.args.get('next')
#     try:
#         dest_url = url_for(dest)
#     except:
#         return redirect(fallback)
#     return redirect(dest_url)


@auth.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    session.modified = True



@auth.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response
   

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            flash('You are already registered.', category='success')
            return redirect(url_for("views.home"))

    
    # user_email = session.get('user_email')
    # user_id = session.get('user_id')
    # user_name = session.get('user_name')

    # dict_log = {
    #     'id': user_id, 
    #     'first_name': user_name, 
    #     'email': user_email,
    # }

    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db.session.rollback()
        user = User.query.filter_by(email=email).first()

        if check_password_hash(user.password, password):
            # session["user_email"] = user.email
            # session["user_id"] = user.id
            # session["user_name"] = user.first_name
            user.authenticated = True
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash('Logged in successfuly!', category='success')

            # next = request.args.get('next')
            # return redirect(next) if next else redirect(url_for('views.home'))

    # return render_template('users/login.html', user=current_user)

            return redirect(url_for("views.home"))
        else:
            flash('Sorry, but you could not log in.', category='error')
            # return redirect('/login')
            # return render_template("auth.login")


    return render_template("users/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
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
    # print(user)
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
@login_required
def user_details():

    
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
