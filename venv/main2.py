from flask import Flask,render_template,redirect,request,flash,url_for,g
import sqlite3 as sql
import numpy as np

app=Flask(__name__)

conn = sql.connect('iiitd.db')
conn.close()

@app.route('/')
def main1():

    return render_template("index.html")


def trips(trip_id_list):
    route_id_list = []
    # print(trip_id_list)
    for i in trip_id_list:
        trip_id = i
        con = sql.connect("iiitd.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select route_id from trips where trip_id=?', (trip_id,))
        st = cur.fetchall();
        for j in st:
            route_id_list.append(str(j["route_id"]))
    # print(route_id_list)
    return route_id_list


def stop_time(msg):
    stop_id_list=[]
    jk=[]
    for i in msg:
        jk.append(str(i["stop_id"]))
    # print(jk)
    for i in jk:
        stop_id=i
        con = sql.connect("iiitd.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select trip_id from stop_times where stop_id=?', (stop_id,))
        st = cur.fetchall();
        for j in st:
            stop_id_list.append(str(j["trip_id"]))
    kj=trips(stop_id_list)
    # print(stop_id_list)
    return kj ,stop_id_list



@app.route('/tdb', methods=['POST', 'GET'])
def tdb():
    if request.method == 'POST':
        try:
            source = str(request.form['source'])
            destination = request.form['destination']

            con = sql.connect("iiitd.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute('select stop_id from stops where stop_name=?', (source,))
            msg = cur.fetchall();
            # print("jhbdhh")
            jko=stop_time(msg)
            jk=jko[0]
            tr=jko[1]
            # print(jk)
            # print(tr)
            jk =np.array(jk)
            # print(jk)

            cur.execute('select stop_id from stops where stop_name=?', (destination,))
            msg1 = cur.fetchall();
            jko1 = stop_time(msg1)
            jk1=jko1[0]
            tr1=jko1[1]
            # print(jk1)
            # print(tr1)
            jk1=np.array(jk1)
            # print(jk1)

            a=set(jk1)
            b=set(jk)
            re=a&b
            print(re)

            #finding the trip availble
            tr=np.array(tr)
            tr=np.unique(tr)
            for j in tr:
                j=str(j)
                seq=[]
                st_id=[]
                cur.execute('select stop_id,stop_sequence from stop_times where trip_id=?', (j,))
                stop1 = cur.fetchall();
                for d in stop1:
                    seq.append(int(d['stop_id']))
                    st_id.append(int(d['stop_sequence']))
                # print(seq)
                # print(st_id)


            if len(re) > 0:
                 result = 0
            else:
                 result = 1


        except:
            result = "error in insert operation"

        finally:
            fix=[source,destination,result]
            return render_template("results.html", fix=fix)
            con.close()


if __name__=='__main__':
    app.run()