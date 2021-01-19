from os import access
from werkzeug import useragents
from app.model.user import User

from app import response, app, db
from flask import request

from flask_jwt_extended import *
import datetime

# def buatAdmin():
#     try:
#         nip = request.form.get('nip')
#         nama = request.form.get('nama')
#         password = request.form.get('password')
#         level = 1

#         users = User(nip=nip, nama=nama, password=password, level=level)
#         users.setPassword(password)
        
#         db.session.add(users)
#         db.session.commit()

#         return response.success('','Sukses Menambahkan Data User')
#     except Exception as e:
#         print(e)

def login():
    try:
        nip = request.form.get('nip')
        password = request.form.get('password')

        user = User.query.filter_by(nip=nip).first()

        if not user:
            return response.badRequest([],"nip tidak terdaftar")

        if not user.checkPassword(password):
            return response.badRequest([],'kombinasi password salah')

        data = singleObject(user)
        expires = datetime.timedelta(days=1)
        expires_refresh = datetime.timedelta(days=3)
        access_token = create_access_token(data,fresh=True,expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            'data':data,
            'access_token': access_token,
            'refresh_token':refresh_token,
        },'Success!')
    except Exception as e:
        print(e)

def singleObject(data):
    data = {
        'id': data.id,
        'nip': data.nip,
        'nama': data.nama
    }

    return data
