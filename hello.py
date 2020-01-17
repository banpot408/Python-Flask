import datetime
import pyodbc
import OpenOPC
import time
import pywintypes

from flask import Flask, render_template

pywintypes.datetime = pywintypes.TimeType






app = Flask(__name__)

@app.route('/')
def hello_world():
    opc=OpenOPC.client()
    opc.servers()
    opc.connect('Matrikon.OPC.Simulation.1')
    value = opc.read(tags,group='Group0',update=1)
    return render_template('index.html', data = value)
#
# @app.route('/login')
# def login():
#     return render_template('login.html')

# tags =['Random.Int1','Random.Real4','Random.Int2','Random.Real8']
tags =['Random.Int1']


def db_exec():
    con_string = "Driver=ODBC Driver 17 for SQL Server;server=BANPOT-P;database=flask_db;trusted_connection=yes"
    sql = '''select * from Person where id = 1'''
    # sql = """
    #     create table Person(
    #         id int identity(1,1) primary key,
    #         username char(10),
    #         fullname char(100),
    #         gender char(1),
    #         weight real,
    #         hight real
    #     )
    # """

    with pyodbc.connect(con_string) as con:
        for row in con.execute(sql):
            username = row[2]
            print(username)
        count_all = con.execute(sql).rowcount
        print(count_all)

if __name__ == "__main__":
    # db_exec()

    app.run(debug=True)
