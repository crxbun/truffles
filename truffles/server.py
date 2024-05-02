from flask import render_template, request, redirect, url_for, jsonify, flash, session
from flask import session as login_session
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from truffles.models import User, Truffle, TruffleAccessories, UserTruffle, Chatroom, Messages, Participants
from truffles import app, db 
from werkzeug.security import generate_password_hash, check_password_hash
from string import ascii_uppercase

socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@app.route('/viewTruffles/')
def viewTruffles():
    username = session.get('name')
    user = User.query.filter_by(username=username).first()
    # Check if the user exists
    if user:
        # Get the user ID
        user_id = user.id
        
        # Query the UserTruffle table to get the truffle IDs associated with the user ID
        truffle_ids = [user_truffle.truffleID for user_truffle in UserTruffle.query.filter_by(userID=user_id).all()]
        
        # Render the template with the truffle IDs
        return render_template('viewTruffles.html', user_id=user_id, truffle_ids=truffle_ids)
    else:
        # Render an error message if the user does not exist
        return render_template('error.html', message='User not found')

if __name__ == "__main__":
    socketio.run(app, debug=True)