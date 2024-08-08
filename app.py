import json
import sqlite3
from flask import Flask
from flask import request
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

app.config['CORS_HEADERS'] = 'Content-Type'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def query_db(query, args=(), one=False):
    cur = get_db_connection().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


@app.route('/')
def index():
    answers = query_db('SELECT * FROM answers')
    return json.dumps(answers)


@app.route('/create/', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.get_json()
        id = str(uuid4())
        user_id = data['id']
        will_be = data['willBe']
        name = data['name']
        companion_name = data['companionName']
        drinks = ', '.join(data['drinks'])
        custom_drink = data['customDrink']
        rouse = data['sayTost']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO answers (id, user_id, will_be, name, companion_name, drinks, custom_drink, rouse) VALUES (?,?,?,?,?,?,?,?)',
            (id, user_id, will_be, name, companion_name, drinks, custom_drink, rouse))
        conn.commit()
        conn.close()
        return 'success'
    return 'fail'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
