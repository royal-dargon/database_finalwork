from . import api
from .. import cur, conn
from flask import jsonify, request
from psycopg2 import extras as ex
from ..model import UserInfo,ManagerInfo, LogInfo


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
    # print(rows)
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
    cur.execute(r"select id, pwd from user_info where uname = '%s';" % user.username)
    rows = cur.fetchall()
    for row in rows:
        if row[1] == user.pwd:
            return jsonify({
                "msg": "登入成功",
                "id": rows[0][0]
            }), 200
    return jsonify({
        "msg": "登入信息有误"
    }), 400


# 这是管理员登录的接口
@api.route("/mlogin", methods=["POST"])
def manager_login():
    manager = ManagerInfo()
    manager.managername = request.form.get('username')
    manager.pwd = request.form.get('password')
    if manager.managername is None or manager.pwd is None:
        return jsonify({
            "msg": "信息不能填写为空"
        }), 400
    sql = "select pwd from manager where mname = %s;"
    cur.execute(r"select id, pwd from manager where mname = '%s';" % manager.managername)
    rows = cur.fetchall()
    for row in rows:
        if row[1] == manager.pwd:
            return jsonify({
                "msg": "登入成功",
                "id": rows[0][0]
            }), 200
    return jsonify({
        "msg": "登入信息有误"
    }), 400


# 这是管理员注册的接口
@api.route("/mregister", methods=["POST"])
def manager_register():
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
    cur.execute("select mname from manager;")
    # conn.commit()
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        if row[0] == username:
            return jsonify({
                "msg": "本昵称已经被使用"
            }), 400

    g = True
    if gender == '男':
        g = True
    else:
        g = False
    values = []
    values.append((username, password, g, email))
    sql = "Insert into manager (mname, pwd, gender, email) values %s;"
    # cur.execute("Insert into manager (mname, pwd, gender, email) values (%s, %s, %d, %s);", values)
    ex.execute_values(cur, sql, values)
    conn.commit()
    # print(values)
    return jsonify({
        "msg": "注册成功"
    }), 200


# 这是展示的主界面，登录进去后，首先展示的便是所有人发布的博客信息
@api.route("/home/log", methods=["GET"])
def home_info():
    cur.execute("Select * from log_info;")  # 对博客表做查询操作,将所有人的博客信息提取出来
    rows = cur.fetchall()
    list1 = []
    for row in rows:  # 把提取的博客信息展示
        content = {'log_id': row[0], 'model_id': row[1], 'user_id': row[2], 'title': row[3], 'create_time': row[5]}
        list1.append(content)

    return jsonify(list1), 200


# 这里是通过点击id对博客的详细内容进行查看，同时也是展示了其相关的评论
@api.route("/home/log/<int:id>", methods=["GET"])
def log_info(id):
    # 先从前端获取博客id号
    log_id = id
    cur.execute(r"select * from log_info where log_id = %s;" % log_id)
    rows = cur.fetchall()
    user_id = rows[0][2]
    cur.execute(r"select uname from user_info where id = %s;" % user_id)
    rows3 = cur.fetchall()
    user_name = rows3[0][0]
    cur.execute(r"select * from comment_info where log_id = %s;" % log_id)
    rows2 = cur.fetchall()
    list1 = []
    for row in rows2:
        content = {'comment_id': row[0],  'context': row[3], 'time': row[4]}
        list1.append(content)
    return jsonify({
        "msg": "查看成功",
        "user_name": user_name,
        "title": rows[0][3],
        "content": rows[0][4],
        "log_time": rows[0][5],
        "comment": list1
    }), 200


# 这里是在博客内容下发布评论
@api.route("/home/log/<int:id>/comment", methods=["POST"])
def post_comment(id):
    # 从前端获取评论内容,博客号,和用户号
    context = request.form.get("comment")
    user_id = request.form.get("user_id")
    print(user_id, context)
    log_id = id

    if context is None or user_id is None:
        return ({
            "msg": "存在字段为空"
        }), 400

    sql = "Insert into comment_info (log_id,user_id,context) values(%d, %d, %s);"
    cur.execute(r"Insert into comment_info (log_id,user_id,context) values(%s, %s, '%s');" % (log_id, user_id, context))

    conn.commit()

    return ({
        "msg": "评论成功"
    }), 200


# 这里是用户发布博客
@api.route("/home/post_log/<int:id>", methods=["POST"])
def post_log(id):
    blog = LogInfo()
    blog.user_id = id
    blog.title = request.form.get('title')
    blog.content = request.form.get('content')
    # blog.model_id = request.form.get('model_id')
    # 现阶段是默认这个数值为1， 后期可以根据选择进行更改
    blog.model_id = 1
    if blog.model_id is None or blog.user_id is None or blog.title == '' or blog.content == '':
        return jsonify({
            "msg": "有数据为空"
        }), 400
    cur.execute(r"insert into log_info (model_id, user_id, title, content) values(%s, %s, '%s', '%s');" % (blog.model_id,blog.user_id, blog.title, blog.content))
    conn.commit()
    return jsonify({
        "msg": "发表成功"
    }), 200


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
def my_photo():
    pass


# 这里是对相册进行添加的操作
@api.route("/home/my_photo/put", methods=["POST"])
def put_photos():
    pass


# 这里是对相册进行删除的操作
@api.route("/home/my_photo/delete/<int:id>")
def del_photo(id):
    pass

