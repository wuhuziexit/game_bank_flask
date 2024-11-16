import pymysql,cryptography


def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='test_bank',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# 普通用户主界面临时储存
ordinary_main_temp = {
    "hint": "",
    "username": ""
}