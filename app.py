import mariadb
from flask import Flask,request,Response
import json
import dbcreds
from flask_cors import CORS


app= Flask(__name__)
CORS(app)

@app.route('/api/post',methods=['GET','POST','PATCH','DELETE'])
def blogs():
    if request.method=='GET':
        conn=None
        cursor=None
        blogs=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM blogpost")
            blogs=cursor.fetchall()
        except Exception as error:
            print("Someting went wrong: ")
            print(error)
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(blogs!=None):
                return Response(json.dumps(blogs,default=str),mimetype="application/json",status=200)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='POST':
        conn=None
        cursor=None
        post_name=request.json.get("name")
        post_content=request.json.get("content")
        post_created=request.json.get("created")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            cursor.execute("INSERT INTO blogpost(name,content,created_at) VALUES(?,?,?)",[post_name,post_content,post_created])
            conn.commit()
            rows=cursor.rowcount
        except Exception as error:
            print("Someting went wrong: ")
            print(error)
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Post Created!",mimetype="text/html",status=201)
            else:
                return Response("Something went wrong",mimetype="text/html",status=500)

    elif request.method=='PATCH':
        conn=None
        cursor=None
        post_name=request.json.get("name")
        post_content=request.json.get("content")
        post_created=request.json.get("created")
        post_id=request.json.get("id")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            if post_name!="" and post_name!=None:
                cursor.execute("UPDATE blogpost SET name=? WHERE id=?",[post_name,post_id])
            if post_content!="" and post_content!=None:
                cursor.execute("UPDATE blogpost SET content=? WHERE id=?",[post_content,post_id])
            if post_created!="" and post_created!=None:
                cursor.execute("UPDATE blogpost SET created_at=? WHERE id=?",[post_created,post_id])
            conn.commit()
            rows=cursor.rowcount
        except Exception as error:
            print("Someting went wrong: ")
            print(error)
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Updated success!",mimetype="text/html",status=204)
            else:
                return Response("Updated failed",mimetype="text/html",status=500)

    elif request.method=='DELETE':
        conn=None
        cursor=None
        post_id=request.json.get("id")
        rows=None
        try:
            conn=mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor=conn.cursor()
            cursor.execute("DELETE FROM blogpost WHERE id=?",[post_id,])
            conn.commit()
            rows=cursor.rowcount
        except Exception as error:
            print("Someting went wrong: ")
            print(error)
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!=None):
                conn.rollback()
                conn.close()
            if(rows==1):
                return Response("Delete success!",mimetype="text/html",status=204)
            else:
                return Response("Delete failed",mimetype="text/html",status=500)