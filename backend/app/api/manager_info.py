from . import api
from .. import cur, conn
from flask import jsonify, request
from psycopg2 import extras as ex


# 这是管理员登录后出现的第一个页面,登录之后也是可以看见所有的博客信息
@api.route("/manager/home/blog", methods=['GET'])
def manager_home():
    cur.execute("Select * from log_info;")  # 对博客表做查询操作,将所有人的博客信息提取出来
    rows = cur.fetchall()
    list1 = []
    for row in rows:  # 把提取的博客信息展示
        content = {'log_id': row[0], 'model_id': row[1], 'user_id': row[2], 'title': row[3], 'create_time': row[5]}
        list1.append(content)
    return jsonify(list1), 200


# 这是管理员通过点击获取id查看博客详情的界面
@api.route("/manager/home/blog/<int:id>", methods=['GET'])
def manager_blog(id):
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
        content = {'comment_id': row[0], 'context': row[3], 'time': row[4]}
        list1.append(content)
    return jsonify({
        "msg": "查看成功",
        "user_name": user_name,
        "title": rows[0][3],
        "content": rows[0][4],
        "log_time": rows[0][5],
        "comment": list1
    }), 200


# 这是管理员查看用户信息的界面
@api.route("/manager/home/user", methods=['GET'])
def manager_user():
    # sql = "select * from user_info;"
    cur.execute("select * from user_info;")
    rows = cur.fetchall()

    list1 = []
    for row in rows:
        if row[3] is True:
            gender = '男'
        else:
            gender = '女'
        content = {"user_id": row[0], "user_name": row[1], "gender": gender, "email": row[4]}
        list1.append(content)
    return jsonify({
        "msg": "查看成功",
        "data": list1
    }), 200


# 这是查看管理员发布日志的地方
@api.route("/manager/home/log", methods=['GET'])
def manager_log():
    cur.execute("select * from message;")
    rows = cur.fetchall()
    list1 = []
    for row in rows:
        content = {'message_id': row[0], 'title': row[1], 'time': row[3]}
        list1.append(content)
    return jsonify({
        "msg": "查看成功",
        "data": list1
    }), 200


# 这是查看详细日志的接口
@api.route("/manager/home/log/<int:id>", methods=['GET'])
def manager_log_info(id):
    sql = "select * from message where message_id = %d;"
    cur.execute(r"select * from message where message_id = %s;" % id)
    rows = cur.fetchall()
    list1 = [{'message_id': rows[0][0], 'title': rows[0][1], 'content': rows[0][2], 'create_time': rows[0][3]}]
    return jsonify({
        "msg": "查看成功",
        "data": list1
    }), 200


# 这是删除该用户的博客的操作，同时会将该用户放入黑名单
@api.route("/manager/home/blog/<int:id>", methods=['DELETE'])
def manager_log_delete(id):
    sql = "select user_id from log_info where log_id = %d;"
    cur.execute(r"select user_id from log_info where log_id = %s;" % id)
    rows = cur.fetchall()

    sql = "delete from log_info where log_id = %d;"
    cur.execute(r"delete from log_info where log_id = %s;" % id)

    sql = "Insert into blacklist (user_id) values(%d);"
    cur.execute(r"Insert into blacklist (user_id) values(%s);" % rows[0][0])

    conn.commit()
    return jsonify({
        "msg": "删除日志成功并且将该用户加入黑名单"
    }), 200


# 这个是发布公告的地方
@api.route("/manager/home/log", methods=['POST'])
def manager_upload_log():
    # 从前端获取公告详情
    info = request.get_json()
    title = info['title']
    content = info['content']
    if title is None or content is None:
        return jsonify({
            "msg": "信息不全"
        }), 400

    sql = "Insert into message (title, content) values(%s,%s);"
    cur.execute(r"Insert into message (title, content) values('%s','%s');" % (title, content))
    conn.commit()

    return jsonify({
        "msg": "发布成功"
    }), 200


# 这个是管理员删除日志的地方
@api.route("/manager/home/log/<int:id>", methods=['DELETE'])
def manager_delete_log(id):
    sql = "delete from message where message_id = %d;"
    cur.execute(r"delete from message where message_id = %s;" % id)
    conn.commit()

    return jsonify({
        "msg": "删除成功"
    }), 200


# 这里是管理员设置查看名单的接口
@api.route("/manager/home/blacklist", methods=['GET'])
def manager_blacklist():
    sql = "select * from blacklist;"
    cur.execute("select * from blacklist;")

    rows = cur.fetchall()

    values = []
    for row in rows:
        values.append(row[0])

    if values is None:
        return jsonify({
            "msg": "黑名单没有成员"
        }), 400

    return jsonify({
        "msg": "查询成功",
        "blacklist": values
    }), 200


# 这里是管理取消用户黑名单的接口
@api.route("/manager/home/blacklist/<int:id>", methods=['DELETE'])
def manager_blacklist_remove(id):
    sql = "delete from blacklist where user_id = %d;"
    cur.execute(r"delete from blacklist where user_id = %s;" % id)
    conn.commit()

    return jsonify({
        "msg": "移除成功",
        "id": id
    }), 200

