import datetime
import pyodbc
import OpenOPC
import time
import pywintypes
import time, threading, random, webbrowser
from flask import Flask, render_template, request, redirect, url_for

pywintypes.datetime = pywintypes.TimeType
app = Flask(__name__)
conn = pyodbc.connect("Driver=ODBC Driver 17 for SQL Server;server=BANPOT-P;database=flask_db;trusted_connection=yes")


@app.route('/adduser')
def add_user():
    return render_template('adduser.html')

@app.route('/selectuser')
def selectuser():
    return render_template('search.html')





@app.route('/')
def show_user():
    value = 80
    sql = "select * from Person"
    with conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        c = []
        for b in rows:
            d = (b[0], b[1], b[2], b[3], round(b[4],2), round(b[5],2))
            c.append(d)
    return render_template('index.html', datas = c)





@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    if request.method == "GET":
        # sql_insert = "insert into Person (username,fullname,gender,weight,hight) values(?,?,?,?,?)"
        sql_delete = "delete from  Person where id =  ?"
        with conn:
            cur = conn.cursor()
            cur.execute(sql_delete, id_data)
            conn.commit()
            print('commit ok')
        return redirect(url_for('show_user'))





@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        db_execuser = request.form['username']
        db_fullname = request.form['fullname']
        db_gender = request.form['gender']
        db_weight = request.form['weight']
        db_hight = request.form['hight']
        sql_insert = "insert into Person (username,fullname,gender,weight,hight) values(?,?,?,?,?)"
        with conn:
            cur = conn.cursor()
            cur.execute(sql_insert, (db_execuser, db_fullname, db_gender, db_weight, db_hight))
            conn.commit()
            print('commit ok')
        return redirect(url_for('show_user'))


@app.route('/select_user', methods=['POST'])
def select_user():
    db_select_user_execuser = '%' + request.form['username'] + '%'
    db_select_user_fullname = '%' + request.form['fullname'] + '%'
    db_select_user_gender   = '%' +  request.form['gender'] + '%'
    db_select_user_weight = request.form['weight']
    db_select_user_hight = request.form['hight']
    sql = "select * from Person where username  like ?"
    print(sql)
    with conn:
        cur = conn.cursor()
        cur.execute(sql, db_select_user_execuser)
        rows = cur.fetchall()
        c = []
        for b in rows:
            d = (b[0], b[1], b[2], b[3], round(b[4],2), round(b[5],2))
            c.append(d)
        print('commit ok select_user()')
        print(c)
    return render_template('search_result.html', datas = c)



@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        id_update = request.form['id']
        db_execuser = request.form['username']
        db_fullname = request.form['fullname']
        db_gender = request.form['gender']
        db_weight = request.form['weight']
        db_hight = request.form['hight']
        sql_insert = "update  Person set username = ?, fullname = ?, gender = ?, weight = ?, hight = ? where id = ?"
        with conn:
            cur = conn.cursor()
            cur.execute(sql_insert, db_execuser, db_fullname, db_gender, db_weight, db_hight, id_update)
            conn.commit()
            print('commit ok')
        return redirect(url_for('show_user'))

if __name__ == "__main__":
    port = 5000
    url = "http://127.0.0.1:{}".format(port)
    wb = webbrowser.get(None)  # instead of None, can be "firefox" etc
    threading.Timer(1.25, lambda: wb.open(url) ).start()
    app.run(port=port, debug=True)
