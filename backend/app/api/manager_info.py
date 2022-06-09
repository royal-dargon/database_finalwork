from . import api
from .. import cur, conn
from flask import jsonify, request
from psycopg2 import extras as ex


# 这是管理员登录后出现的第一个页面,登录之后也是可以看见所有的博客信息
@api.route("/manager/home/blog", methods=['GET'])
def manager_home():
    pass


# 这是管理员通过点击获取id查看博客详情的界面
@api.route("/manager/home/blog/<int:id>", methods=['GET'])
def manager_blog(id):
    pass


# 这是管理员查看用户信息的界面
@api.route("/manager/home/user", methods=['GET'])
def manager_user():
    pass


# 这是管理员查看用户详细信息的接口
@api.route("/manager/home/user/<int:id>", methods=['GET'])
def manager_user_info(id):
    pass


# 这是管理员发布日志的地方
@api.route("/manager/home/log", methods=['GET'])
def manager_log():
    pass


# 这是查看详细日志的接口
@api.route("/manager/home/log/<int:id>", methods=['GET'])
def manager_log_info(id):
    pass