from flask import Flask , render_template , redirect , url_for , request
from flask_socketio import join_room, leave_room, send, SocketIO , emit
from flask_pymongo import PyMongo
import datetime


x = datetime.datetime.now()
print(x)

app = Flask(__name__) 


app.config["MONGO_URI"] = "mongodb://localhost:27017/chat-data"

mongo = PyMongo(app)

app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

@app.route("/" , methods=["POST","GET"])
def home():
  if request.method == "POST":
     username = request.form["name"]
     roomid = request.form["room"]
     return render_template("chat.html" , user = username , room = roomid)
  
  return render_template("home.html")


@socketio.on('join_room')
def handle_new_joiners(data):
  
   print(f" {data['username']} have joined {data['room']} ")
   socketio.emit('join_room_announcement', data)



@socketio.on('send_message')
def handle_send_messages(data):
   mongo.db.user.insert_one({"user":data['username'] , "msg": data["message"] ,"room":data["room"], "date":x})
   socketio.emit('recevied' , data )


@app.route("/users" , methods=["POST" , "GET"])
def users():
   if request.method == "POST":
      rm = request.form["room"]
      users=list(mongo.db.user.find({"room":rm}))
      
      for i in users:
         print(i["user"])
         print(i["msg"])

      return render_template("get_users.html", users = users)
   
   return render_template("user.html")

  



if __name__ == '__main__':
    socketio.run(app, debug=True)
