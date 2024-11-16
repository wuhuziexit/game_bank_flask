from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import config
# 导入蓝图
from user_roots.routes import root
from user_ordinary.routes import ordinary

app = Flask(__name__)
app.secret_key = 'my_flask_key'

# 注册蓝图
app.register_blueprint(root, url_prefix='/root')
app.register_blueprint(ordinary, url_prefix='/ordinary')


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """
    1.获取前端数据
    2.获取数据库数据
    3.对比 成功 ==》main.html  不成功 ==》login.html
    4.看是否为超级用户，是则 ==》 main.html 否则
    :return:
    """
    username = request.form.get('username')
    password = request.form.get('password')
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE username=%s AND password=%s', (username, password))
        fetchone = cursor.fetchone()
        connection.close()
        if fetchone is not None:
            session['permission'] = fetchone["permission"]
            session['username'] = fetchone["username"]
            session['isLogin'] = True
            if fetchone["permission"] == 1:
                return redirect(url_for("root.main"))
            elif fetchone["permission"] == 2:
                config.ordinary_main_temp["username"] = fetchone["username"]
                return redirect(url_for('ordinary.ordinary_main'))

        else:
            return render_template('login.html', hint="用户名或密码错误")


# 注册跳转路由
@app.route('/registration')
def registration():
    return render_template('registration.html')


# 注册逻辑代码
@app.route('/registration-submit', methods=['POST'])
def registration_submit():
    """
    1.获取前端数据，用户名、密码1、密码2
    2.比对密码1和2，不一致则重新渲染注册页面
    3.对比数据库，查看是否存在相同用户名
    4.创建新用户
    :return:
    """
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password != password2:
        return render_template('registration.html', hint="密码不一致，请重新输入", username=username)
    connection = config.get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE username=%s', (username))
        fetchone = cursor.fetchone()
        print(fetchone)
        if fetchone is not None:
            return render_template('registration.html', hint="用户已存在")
        cursor.execute("INSERT INTO user (username, password,permission) VALUES (%s, %s,%s)", (username, password, 2))
        connection.commit()
        cursor.close()
        connection.close()
        print("用户添加成功")
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()
