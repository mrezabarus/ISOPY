from flask import Flask, json, jsonify, request, make_response, render_template, session
import jwt
import datetime
from functools import wraps
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_cors import CORS, cross_origin
from sqlalchemy.sql import text 
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/reza_apps_api'
app.config['SECRET_KEY'] = 'rezabarusappskeren1'

db = SQLAlchemy(app)
CORS(app, resources={r'/*':{'origins':'*'}})

#task = db.Table('task', db.metadata, autoload=True, autoload_with=db.engine)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

#get table query
#db.session.query(task).all()
#task.query.all()
#return ''

def tokenrequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.engine.execute("SELECT * from USER where username = '%s'" %(data['username'])).first()
        except:
            return jsonify({"message":"Token is invalid"}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    username = auth.username
    
    if not auth or not auth.username or not auth.password:
        return make_response('Could not  Verify!', 401, {'WWW-Authenticate': 'Basic realm="login requiered"'})

    users = db.engine.execute("""SELECT * from USER where username = '%s'""" %(username)).first()

    if not users:
        return make_response('Could not user Verify!', 401, {'WWW-Authenticate': 'Basic realm="login requiered"'})

    if check_password_hash(users.password, auth.password):
        token = jwt.encode({'username': users.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not password Verify!', 401, {'WWW-Authenticate': 'Basic realm="login requiered"'})
    

#user function
@app.route('/user', methods=['GET'])
@tokenrequired
def get_all_user(current_user):

    if current_user.admin != '1':
        return jsonify({'message':'cannot perform that function'})

    users = db.engine.execute("SELECT * from USER")
    datauser = {}
    for user in users:
        datauser[user.id_user]={"username":user.username,"password":user.password}
    return jsonify({'user':datauser})

@app.route('/user/<id_user>', methods=['GET'])
def get_one_user(id_user):
    users = db.engine.execute("SELECT * from USER where id_user = %s" %(id_user,))
    datauser = {}
    for user in users:
        datauser[user.id_user]={"username":user.username,"password":user.password}
    return datauser

@app.route('/user', methods=['POST'])
def create_user():
    data            = request.get_json()

    hashed_password = generate_password_hash(data.get('password'), method='sha256')

    new_user        = "insert into USER (username,password, fullname, admin) values (%s,%s,%s,%s)"

    username        = data.get('username')
    #password        = request.form.get('password')
    fullname        = data.get('fullname')
    admin           = '0'

    input           = (username, hashed_password, fullname, admin)
    insert_query    = db.engine.execute(new_user,input)


    return jsonify({'message': 'new data input'})

@app.route('/user/<id_user>', methods=['PUT'])
def promote_user(id_user):
    users = db.engine.execute("SELECT * from USER where id_user = %s" %(id_user,))
    
    if not users:
        return jsonify({'message':'No Data!'})
    
    admin           = '1'
    query = "update USER set admin = %s where id_user = %s"
    update = (admin,id_user)
    update_query = db.engine.execute(query, update)
    return jsonify({'message': 'data updated'})

@app.route('/user/<id_user>', methods=['DELETE'])
def delete_user(id_user):
    query = "delete from USER where id_user = %s"
    input = (id_user)
    insert_query = db.engine.execute(query,input)
    return jsonify({'message': 'data deleted'})


#todo function
@app.route('/todo', methods=['GET'])
@tokenrequired
def get_all_todos(current_user):
    query = """
            SELECT
            a.id 
            , a.todo
            , b.username
            , b.fullname
            FROM todo a
            left join user b
            on a.id_user = b.id_user
            where a.id_user = '%s'
            """
    input = (current_user.id_user)
    todos = db.engine.execute(query,input)
    datatodos = {}
    for todo in todos:
        datatodos={"username":todo.username,"todo":todo.todo}
    return jsonify({'todo':datatodos})

@app.route('/todo/<id_todo>', methods=['GET'])
@tokenrequired
def get_one_todo(current_user, todo_id):
    return ''

@app.route('/todo',methods=['POST'])
@tokenrequired
def create_todo(current_user):
    data            = request.get_json()
    new_todo        = "insert into todo (todo,complete,id_user) values (%s,%s,%s)"

    todo        = data.get('todo')
    #password        = request.form.get('password')
    complete        = '0'
    user_id         = current_user.id_user

    input           = (todo, complete, user_id)
    insert_query    = db.engine.execute(new_todo,input)

    return jsonify({'message': 'data input'})

@app.route('/todo/<id_todo>', methods=['PUT'])
@tokenrequired
def complete_todo(current_user, todo_id):
    return ''

@app.route('/todo/<id_todo>', methods=['DELETE'])
@tokenrequired
def delete_todo(current_user,todo_id):
    return ''


if __name__ == '__main__':
    app.run(debug=True)