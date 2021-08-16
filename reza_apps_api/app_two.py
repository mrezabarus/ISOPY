from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/articulate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

@app.route("/", methods=['GET'])
def hello():
    #return jsonify({"data":"Hello gaes"})
    users = db.session.execute('SELECT * from data_user order by id desc limit 10').all()
    # =================================Cara Satu================================= #
    # payload = []
    # content = {}
    # for result in users:
    #     content = {'id': result[0], 'username': result[1], 'password': result[2]}
    #     payload.append(content)
    #     content = {}
    # return jsonify(payload)

    # =================================Cara Dua================================= #
    datauser = {}
    for user in users:
        datauser[user.id_user]={"user_name":user.user_name,"password":user.password}
    return jsonify({'user':datauser})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
