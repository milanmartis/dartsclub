from flask import Blueprint, render_template, request, flash, redirect, url_for, session, app
from .models import User, Season
from . import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, IntegerField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, StopValidation
auth = Blueprint('auth', __name__)
import datetime
from flask import url_for, current_app
from flask_mail import Message
from website import mail
   


@auth.route('/login', methods=['GET', 'POST'])
def login():


    
    if request.method == 'POST' and request.form.get('email'):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        
        if user.confirm==False:
            flash('Váš účet nie je aktivovaný. Potvrďte konfirmačný e-mail!', category='error')
        else:
            if user and bcrypt.check_password_hash(user.password, password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()

                login_user(user, remember=True)
                next_page = request.args.get('next')

                flash('Logged in successfuly!', category='success')


                # return redirect(url_for("views.home"))
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Sorry, but you could not log in.', category='error')

            
            print(current_user)


    return render_template("users/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))


@auth.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', None)
        first_name = request.form.get('first_name', None)
        password1 = request.form.get('password1', None)
        password2 = request.form.get('password2', None)
        # season_id = request.form.get('season_id', None)
        
        # season = Season.query.filter_by(id=season).first()
        user = User.query.filter_by(email=email).first()
        nickname = User.query.filter(User.first_name.ilike(first_name)).first()
        if user:
            flash('Email already exist.', category='error')
        elif nickname:
            flash("User name already exist.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 chars", category="error")
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 chars", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match", category="error")
        elif len(password1) < 7:
            flash("Passwords must be at least 7 chars", category="error")
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')

            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            # new_user.seasony.append(season)

            db.session.commit()
            send_confirm_email(new_user)

            # login_user(new_user, remember=True)

            flash("Account created. Check your email to confirm account.", category="success")
            return redirect(url_for('auth.login'))
            # add user to database
    return render_template("users/sign_up.html", user=current_user)



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Reset password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. Try another one.')
            


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()], render_kw={"placeholder": "Password"}, default = "")
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password"}, default = "")

    submit = SubmitField('Save new password')



@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password.', category="success")
        return redirect(url_for('auth.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form, user=current_user)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The used token has expired.', category="warning")
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been changed! You can login.', category="success")
        return redirect(url_for('auth.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)



# @users.route("/confirm_email", methods=['GET', 'POST'])
# def confirm_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('users/reset_request.html', title='Reset Password', form=form, teamz=RightColumn.main_menu(), next_match=RightColumn.next_match(), score_table=RightColumn.score_table())


@auth.route("/confirm_email/<token>", methods=['GET', 'POST'])
def confirm_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_confirm_token(token)
    if user is None:
        flash('The used token has expired.', category="warning")
        return redirect(url_for('auth.register'))
    else:
        user.confirm = True

        db.session.commit()
        flash('Your email has been successfully verified! Welcome to the club. You can login.', category="success")
        return redirect(url_for('auth.login'))
    # return render_template('users/confirm_email.html', title='Confirm Register Email', form=form, teamz=RightColumn.main_menu(), next_match=RightColumn.next_match(), score_table=RightColumn.score_table())



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=('Darts Club', 'info@dartsclub.sk'),
                  recipients=[user.email])
    msg.html = f'''<center><h1>To reset your password, click on the following button</h1>
<br>
<br>
<a style="
    border-radius: 14px !important;
    background-color: #00EE00;
    border: 2px solid #00EE00;
    color: #030303;
    font-weight: 610;
    font-size: 120%;
    text-decoration:none;
    cursor:pointer;
    padding: 8px 12px 8px 12px;
    margin: 12px;
    width:300px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;" 
    href="{current_app.url_for('auth.reset_token', token=token, _external=True)}">RESET PASSWORD</a>
<br>
<br>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
<br>
<br>
  <source srcset="{ current_app.url_for('static', filename='img/logo-dark.png', _external=True) }" media="(prefers-color-scheme: dark)">
  <img width="120" src="{ current_app.url_for('static', filename='img/logo-light.png', _external=True) }">
<h5>©4NOLIMIT. POWERED BY APPDESIGN.SK</h5>
</center>
'''
    mail.send(msg)


def send_confirm_email(user):
    token = user.get_confirm_token()
    msg = Message('Confirm your register email',
                  sender=('Darts Club', 'info@dartsclub.sk'),
                  recipients=[user.email])
    msg.body = f'''<center><h1>To confirm your email, click on the following link</h1>
<br>
<br>
<a style="
    border-radius: 14px !important;
    background-color: #00EE00;
    border: 2px solid #00EE00;
    color: #030303;
    font-weight: 610;
    font-size: 120%;
    text-decoration:none;
    cursor:pointer;
    padding: 8px 12px 8px 12px;
    margin: 12px;
    width:300px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;" 
    href="{url_for('auth.confirm_token', token=token, _external=True)}">CONFIRM ACCOUNT</a>
<br>
<br>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
<br>
<br>
  <source srcset="{ current_app.url_for('static', filename='img/logo-dark.png', _external=True) }" media="(prefers-color-scheme: dark)">
  <img width="120" src="{ current_app.url_for('static', filename='img/logo-light.png', _external=True) }">
<h5>©4NOLIMIT. POWERED BY APPDESIGN.SK</h5>
</center>
'''
    mail.send(msg)



def environment():
    """
    This is not how you want to handle environments in a real project,
    but for the sake of simplicity I'll create this function.

    Look at using environment variables or dotfiles for these.
    """
    return {
        "billing": {
            "stripe": {
                "token": "****",
                "product": "****",
            }
        }

    }






















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
        nickname = User.query.filter(User.first_name.like(first_name)).filter(User.first_name.notlike(current_user.first_name)).first()

        print(current_user.first_name)
        if user == '':
           flash('This user doesn\'t exist.', category='error')
        elif len(first_name) < 2:
            flash("First Name must be greater than 1 chars", category="error")
        elif nickname:
            flash("User name already exist.", category="error")
        else:
            if password1 !='':
                if not bcrypt.check_password_hash(user.password, password_old):
                    flash('Old password is not correct!', category='error')
                elif password1 != password2:
                    flash("New passwords don\'t match", category="error")
                elif password_old == password2:
                    flash("New password must be different", category="error")
                elif len(password1) < 7:
                    flash("New passwords must be at least 7 chars", category="error")
                else:
                    user.password = bcrypt.generate_password_hash(password1).decode('utf-8')
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
