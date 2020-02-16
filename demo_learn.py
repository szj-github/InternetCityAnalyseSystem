# -*-coding：UTF-8 -*- 

# @Time : 2019/10/18 0018 19:20 

# @File : demo_learn.py 

# @Software: PyCharm

from flask import Flask
from flask_restful import Api,Resource

app = Flask(__name__)
api = Api(app)

class LoginView(Resource):
    def post(self):
        return 'hello'
api.add_resource(LoginView,'/login/',endpoint='login')
