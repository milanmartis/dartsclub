from website import create_app
import os
from website import db

app = create_app()

# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)),host='127.0.0.1',debug=True)
