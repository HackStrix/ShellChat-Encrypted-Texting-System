from flask import request,Flask,app,jsonify,render_template
import pymysql
import base64

app = Flask(__name__)

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host='mysql0',
        user='sankalp',
        password = "123456",
        db='userdata',
        )

    cur = conn.cursor()
    cur.execute("select @@version")
    output = cur.fetchall()
    print(output)

    # To close the connection
    return conn,cur




@app.route('/',methods=['GET','POST'])
def init():
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        print(content_type)
        data = request.get_json()
        from_user = data["from_username"]
        to_user = data["username"]
        message = data["message"]
        print(message)
        save_new_message(to_user,from_user,message)
        return render_template("abc.html")

@app.route('/check_message',methods = ['GET'])
def check_message():
    data = request
    user = request.args.get("username")
    last_chat_id = request.args.get("last_chat_id")
    db, curr = mysqlconnect()
    curr.execute("SELECT message, from_user,chat_id FROM history where to_user='"+user+"' and chat_id > "+last_chat_id)
    r = curr.fetchall()
    db.close()
    try:
        message_list = list(zip(*r))
        print(message_list)
        return jsonify({"username":message_list[1],"message":message_list[0],"chat_id":message_list[2]})
    except:
        return jsonify({"lol":"lol"})

@app.route('/ask_key', methods = ['GET'] )
def ask_keys():
    data = request
    user_target  = data.args.get('username')
    print(user_target)
    db,curr = mysqlconnect()
    sql = "select public_n,public_e from userkeys where username = '"+user_target+"'"
    curr.execute(sql)
    r = curr.fetchone()
    db.close()
    public_n = r[0]
    public_e = r[1]
    return jsonify({"public_n":int(public_n),"public_e":public_e})


@app.route('/send_public_key', methods = ['POST'])
def save_public_key():
    data = request.get_json()
    username = data["username"]
    public_n = data["public_n"]
    public_e = data["public_e"]
    print(public_n)
    print(public_e)
    db, curr = mysqlconnect()
    sql = "insert into userkeys values ('"+username+"','"+str(public_n)+"'," +str(public_e)+")"
    curr.execute(sql)
    db.commit()
    db.close()
    return render_template("abc.html")




def save_new_message(to_user,from_user,message):
    db, curr = mysqlconnect()
    output = curr.execute("SELECT MAX(chat_id) FROM history")
    r = curr.fetchone()
    output = r[0]
    curr.execute("insert into history values ("+str(output+1)+",'"+to_user+"','"+from_user+"',\""+message+"\")")
    db.commit()
    db.close()


app.run(host="0.0.0.0",port=5000,debug=True)
