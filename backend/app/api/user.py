from . import api
from .. import cur, conn
from flask import jsonify, request
from psycopg2 import extras as ex
from ..model import UserInfo


# 这是注册用户的接口
@api.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    gender = request.form.get('gender')
    email = request.form.get('email')
    if username is None or password is None or password2 is None or gender is None or email is None:
        return jsonify({
            "msg": "注册时不允许有填写内容为空!"
        }), 400
    if password != password2:
        return jsonify({
            "msg": "注册时两次密码输入不一致"
        }), 400
    cur.execute("select uname from user_info;")
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        if row[0] == username:
            return jsonify({
                "msg": "本昵称已经被使用"
            }), 400
    mark = 1
    g = True
    if gender == '男':
        g = True
    else:
        g = False
    values = []
    values.append((username, password, g, email, mark))
    sql = "Insert into user_info (uname, pwd, gender, email, mark) values %s;"
    # cur.execute("Insert into user_info (uname, pwd, gender, email, mark) values (%s, %s, %d, %s, %d);", values)
    ex.execute_values(cur, sql, values)
    conn.commit()
    # print(values)
    return jsonify({
        "msg": "注册成功"
    }), 200


# 这是登录的接口
@api.route("/login", methods=["POST"])
def login():
    user = UserInfo()
    user.username = request.form.get('username')
    user.pwd = request.form.get('password')
    if user.username is None or user.pwd is None:
        return jsonify({
            "msg": "信息不能填写为空"
        }), 400
    sql = "select pwd from user_info where uname = %s;"


# 这是管理员登录的接口
@api.route("/mlogin", methods=["POST"])
def manager_login():
    pass


# 这是管理员注册的接口
@api.route("/mregister", methods=["POST"])
def manager_register():
    pass


# 这是展示的主界面，登录进去后，首先展示的便是所有人发布的博客信息
@api.route("/home/log", methods=["GET"])
def home_info():
    pass


# 这里是通过点击id对博客的详细内容进行查看，同时也是展示了其相关的评论
@api.route("/home/log/<int:id>", methods=["GET"])
def log_info(id):
    pass


# 这里是在博客内容下发布评论
@api.route("/home/log/<int:id>/comment", methods=["GET"])
def post_comment():
    pass


# 这里是用户发布博客
@api.route("/home/post_log", methods=["POST"])
def post_log():
    pass


# 这里是查看自己的模板
@api.route("/home/my_model/<int:id>", methods=["GET"])
def my_model(id):
    pass


# 这里是查看所有的模板信息
@api.route("/home/model", methods=["GET"])
def all_model():
    pass


# 这里是对自己想要的模板进行添加
@api.route("/home/model/<int:id>")
def get_model():
    pass


# 这里是查看自己的相册
@api.route("/home/my_photo")
def get_photo():
    pass


# 这里是用过点击照片查看详情
@api.route("/home/my_photo/get/<int:id>")
def my_photo()
    pass


# 这里是对相册进行添加的操作
@api.route("/home/my_photo/put", methods=["POST"])
def put_photos():
    pass


# 这里是对相册进行删除的操作
@api.route("/home/my_photo/delete/<int:id>")
def del_photo(id):
    pass

