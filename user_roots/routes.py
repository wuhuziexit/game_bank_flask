from flask import Blueprint, render_template, request, redirect, url_for, session
import config

root = Blueprint('root', __name__)


@root.before_request
def is_login():
    # 执行在每个请求之前的操作
    """判断是否成功登陆"""
    try:
        config.ordinary_main_temp['username'] = session["username"]
        if session["permission"] != 1:
            return redirect(url_for("home"))
        if not session["isLogin"]:
            return redirect(url_for("home"))
    except KeyError:
        return redirect(url_for("home"))


@root.route('/main', methods=['GET'])
def main():
    """
    1.超级用户的主界面
    2.判断是否成功登陆，防止用户跳过登陆直接通过url转入该界面
        判断用户权限
    3.连接数据库将数据库的数据以表格形式呈现
    :return:
    """
    table = "<table>%s</table>"
    trs = ""
    tr_template = "<tr>" + "<td>%d</td>" + "<td>%s</td>" + "<td>%s</td>" + "<td>%s</td>" + "<td>%s</td> " + "<td>%s</td> " + "</tr>"
    tr_buts_template = ("<button name=\"update_but\" value=\"%d\">修改</button><button name=\"delete_but\" "
                        "value=\"%d\">删除</button>")
    query_username = request.args.get("query_username") if request.args.get("query_username") is not None else ""
    fetchall = user_query(query_username)
    for index, row in enumerate(fetchall):
        trs += tr_template % (fetchall[index]["id"], fetchall[index]["username"], fetchall[index]["password"],
                              "超级用户" if fetchall[index]["permission"] == 1 else "普通用户",
                              fetchall[index]["yue"],
                              tr_buts_template % (fetchall[index]["id"], fetchall[index]["id"]))
    return render_template('main.html', trs=trs, username=session['username'])


@root.route('/adduser')
def adduser():
    return render_template('administrator_adduser.html')


@root.route('/adduser-submit', methods=['POST'])
def adduser_submit():
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE username=%s', (request.form.get('username')))
        fetchone = cursor.fetchone()
        if fetchone is not None:
            return redirect(url_for('adduser'))
        cursor.execute("INSERT INTO user (username, password,permission,yue) VALUES (%s,%s,%s,%s)",
                       (request.form.get('username'), request.form.get('password'), request.form.get('permission'),
                        request.form.get('yue')))
        connection.commit()
        cursor.close()
    connection.close()
    return redirect(url_for('root.main'))


# 修改页面的路由
@root.route('/user-update')
def user_update():
    update_id = request.args.get('update_id')
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE id=%s', (update_id))
        fetchone = cursor.fetchone()
        if fetchone is not None:
            if fetchone["permission"] == 1:
                return render_template("administrator_update.html", id=update_id, username=fetchone["username"],
                                       password=fetchone["password"], yue=fetchone["yue"],
                                       root_user="selected")
            else:
                return render_template("administrator_update.html", id=update_id, username=fetchone["username"],
                                       password=fetchone["password"], yue=fetchone["yue"],
                                       dc_user="selected")


# 修改页面的逻辑代码
@root.route('/user-update—submit', methods=['POST'])
def user_update_submit():
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('update user set username = %s,password = %s,yue=%s,permission=%s where id=%s', (
            request.form['username'], request.form['password'], request.form['yue'], request.form['permission'],
            request.form.get('id')))
        connection.commit()
    connection.close()
    return redirect(url_for("root.main"))


@root.route('/user-update-delete-query', methods=['get'])
def user_update_delete_query():
    """
    1.获取修改和删除的用户id
    2.判断是修改还是删除用户，添加对应的逻辑代码
    3.如果都不是修改或删除，则判断是否为查询
    :return:
    """
    update_id = request.args.get("update_but")
    delete_id = request.args.get("delete_but")
    query_username = request.args.get("query_username")
    if update_id is not None:
        return redirect(url_for("root.user_update", update_id=update_id))
    if delete_id is not None:
        connection = config.get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM user WHERE id=%s', (delete_id))
            connection.commit()
        connection.close()
    if query_username is not None:
        return redirect(url_for("root.main", query_username=query_username))
    return redirect(url_for("root.main"))


@root.route('/exit-login')
def user_exit_login():
    session["isLogin"] = None
    return redirect(url_for("home"))


def user_query(username=""):
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        execute = cursor.execute("select * from user where username like %s", ("%" + str(username) + "%"))
        return cursor.fetchall()
