# imports
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
 
# initializing Flask app
app2 = Flask(__name__)
 
# Google Cloud SQL (change this accordingly)
PASSWORD ="3(%`hhUq]#;GjQL["
PUBLIC_IP_ADDRESS ="35.189.222.107"
DBNAME ="darts"
PROJECT_ID ="gasparik-1578814675994"
INSTANCE_NAME ="dartsdbase0001"
 
# configuration
app2.config["SECRET_KEY"] = "yoursecretkey"
app2.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 
# db = SQLAlchemy(app2)

# try:    
#     q="CREATE TABLE IF NOT EXISTS `student` (\
#   `id` int(2) NOT NULL AUTO_INCREMENT,\
#   `name` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '',\
#   `class` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT '',\
#   `mark` int(3) NOT NULL DEFAULT '0',\
#   `sex` varchar(6) CHARACTER SET utf8 NOT NULL DEFAULT 'male',\
#       UNIQUE KEY `id` (`id`)\
#     ) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"
#     db.execute(q)
# except:
#         print('error')

db2 = SQLAlchemy(app2)
 
# User ORM for SQLAlchemy
class Users(db2.Model):
    id = db2.Column(db2.Integer, primary_key = True, nullable = False)
    name = db2.Column(db2.String(50), nullable = False)
    email = db2.Column(db2.String(50), nullable = False, unique = True)
 
@app2.route('/add', methods =['POST'])
def add():
    # getting name and email
    name = request.form.get('name')
    email = request.form.get('email')
 
    # checking if user already exists
    user = Users.query.filter_by(email = email).first()
 
    if not user:
        try:
            # creating Users object
            user = Users(
                name = name,
                email = email
            )
            # adding the fields to users table
            db.session.add(user)
            db.session.commit()
            # response
            responseObject = {
                'status' : 'success',
                'message': 'Successfully registered.'
            }
 
            return make_response(responseObject, 200)
        except:
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occurred !!'
            }
 
            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'User already exists !!'
        }
 
        return make_response(responseObject, 403)
 
@app2.route('/view')
def view():
    # fetches all the users
    users = Users.query.all()
    # response list consisting user details
    response = list()
 
    for user in users:
        response.append({
            "name" : user.name,
            "email": user.email
        })
 
    return make_response({
        'status' : 'success',
        'message': response
    }, 200)
 
 
if __name__ == "__main__":
    # serving the app directly
    app.run()