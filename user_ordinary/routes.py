from flask import Blueprint, render_template, request, redirect, url_for, session
import config

ordinary = Blueprint('ordinary', __name__)


@ordinary.before_request
def is_login():
    # 执行在每个请求之前的操作
    """判断是否成功登陆"""
    try:
        config.ordinary_main_temp['username'] = session["username"]
        if session["permission"] != 2:
            return redirect(url_for("home"))
        if not session["isLogin"]:
            return redirect(url_for("home"))
    except KeyError:
        return redirect(url_for("home"))


# 普通用户
@ordinary.route('/')
def ordinary_main():
    return render_template("ordinary_user_main.html", ordinary_main_temp=config.ordinary_main_temp)


@ordinary.route('/transactions')
def ordinary_transactions():
    tr_template = "<tr>" + "<td>%d</td>" + "<td>%s</td>" + "<td>%s</td>" + "</tr>"
    trs = ""
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("select * from bank_transactions,user where username=%s and bank_transactions.user_id=user.id",
                       (session['username']))
        fetchall = cursor.fetchall()
        for index, row in enumerate(fetchall):
            trs += tr_template % (fetchall[index]["money"], fetchall[index]["time"], fetchall[index]["note"])
    connection.close()
    return render_template("ordinary_user_transactions.html", ordinary_main_temp=config.ordinary_main_temp, trs=trs)


@ordinary.route('/ordinary-user-money', methods=['POST'])
def ordinary_main_submit():
    but_val = request.form.get('but')
    connection = config.get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("select * from user where username=%s", (session['username']))
            fetchone = cursor.fetchone()
            money = request.form.get('money')
            if money is not None:
                if but_val == "sava_money":
                    if float(money) % 100 == 0:
                        cursor.execute("update user set yue = %s where id = %s",
                                       (fetchone["yue"] + float(money), fetchone["id"]))
                        connection.commit()
                        cursor.execute("insert into bank_transactions(user_id,money,time) values (%s,%s,NOW())",
                                       (fetchone["id"], float(money)))
                        connection.commit()
                        config.ordinary_main_temp["hint"] = "存入成功"
                        return redirect(url_for("ordinary.ordinary_main"))
                    else:
                        config.ordinary_main_temp["hint"] = "输入不是100的整数"
                        return redirect(url_for("ordinary.ordinary_main"))
                elif but_val == "get_money":
                    if float(money) % 100 == 0 and float(money) <= fetchone["yue"]:
                        cursor.execute("update user set yue = %s where id = %s",
                                       (fetchone["yue"] - float(money), fetchone["id"]))
                        connection.commit()
                        cursor.execute("insert into bank_transactions(user_id,money,time) values (%s,%s,NOW())",
                                       (fetchone["id"], -float(money)))
                        connection.commit()
                        config.ordinary_main_temp["hint"] = "成功取出"
                        return redirect(url_for("ordinary.ordinary_main"))
                    else:
                        config.ordinary_main_temp["hint"] = "输入不是100的整数或余额不足"
                        return redirect(url_for("ordinary.ordinary_main"))
            if but_val == "query_yue":
                cursor.execute("select yue from user where id = %s", (fetchone["id"],))
                yue = cursor.fetchone()["yue"]
                config.ordinary_main_temp["hint"] = "用户 %s 您的余额为：%s" % (session["username"], str(yue))
                return redirect(url_for("ordinary.ordinary_main"))
            elif but_val == "exit":
                session["isLogin"] = None
                return redirect(url_for("home"))
    except ValueError:
        return redirect(url_for("ordinary.ordinary_main"))
