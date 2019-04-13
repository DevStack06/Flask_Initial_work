from flask import Flask,render_template,redirect,request,flash,url_for,g
import sqlite3 as sql


app=Flask(__name__)

conn = sql.connect('iiitd.db')
conn.close()

@app.route('/')
def main1():

    return render_template("index.html")

@app.route('/tdb', methods=['POST', 'GET'])
def tdb():
    if request.method == 'POST':
        try:
            source = str(request.form['source'])
            destination = request.form['destination']

            con = sql.connect("iiitd.db")
            con.row_factory = sql.Row
            cur = con.cursor()

            #source stops ids
            cur.execute('select stop_id from stops where stop_name=?', (source,))
            stp1 = cur.fetchall();

            #destination stop ids
            cur.execute('select stop_id from stops where stop_name=?', (destination,))
            stp2 = cur.fetchall();
            dest_id=[]
            for l in stp2:
                dest_id.append(int(l['stop_id']))

            route1 = []
            route2 = []
            #finding the trip
            source_id=[]
            flag=1
            for i in stp1:
                i=str(i['stop_id'])
                source_id.append(int(i))
                cur.execute('select trip_id from stop_times where stop_id=?', (i,))
                trip=cur.fetchall();
                for j in trip:
                    j=str(j['trip_id'])
                    cur.execute('select stop_sequence from stop_times where stop_id=? and trip_id=?', (i, j,))
                    seq_t=cur.fetchall();
                    seq_t=seq_t[0]
                    ss=str(seq_t['stop_sequence'])

                    cur.execute('select stop_id from stop_times where stop_sequence>? and trip_id=?', (ss, j,))
                    new_st=cur.fetchall();
                    for k in new_st:
                        k=int(k['stop_id'])
                        # print(k)
                        # print(dest_id)
                        if k in dest_id:
                            flag=0
                            break
                    if flag==0:
                        break
                    cur.execute('select route_id from trips where trip_id=?', (j,))
                    route_st = cur.fetchall();
                    for n in route_st:
                        route1.append(int(n['route_id']))
                if flag==0:
                    break;


                for h in dest_id:
                    cur.execute('select trip_id from stop_times where stop_id=?', (h,))
                    trip = cur.fetchall();
                    for j in trip:
                        j = str(j['trip_id'])
                        cur.execute('select route_id from trips where trip_id=?', (j,))
                        route_st = cur.fetchall();
                        for n in route_st:
                            route2.append(int(n['route_id']))

            if flag==0:
                result=0
            else:
                a=set(route1)
                b=set(route2)
                re=a&b
                if len(re)>0:
                    result=1
                else:
                    result="No Route"



        except:
            result = "error in insert operation"

        finally:
            fix=[source,destination,result]
            return render_template("results.html", fix=fix)
            con.close()


if __name__=='__main__':
    app.run()