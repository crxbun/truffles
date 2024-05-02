from flask import render_template, request, redirect, url_for, jsonify, flash, session
from flask import session as login_session
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from truffles.models import User, Truffle, TruffleAccessories, UserTruffle, Chatroom, Messages, Participants, UserChatroom
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
        
        if not Chatroom.query.filter_by(code=code).first():
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
        
        user = User.query.filter_by(username=name).first()

        if not user:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            new_chatroom = Chatroom(code=room, user_id=user.id)
            db.session.add(new_chatroom)

            db.session.add(UserChatroom(code=room, user_id=user.id))
            db.session.commit()     
        elif not Chatroom.query.filter_by(code=code).first():
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        session["user_id"] = user.id
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or not Chatroom.query.filter_by(code=room).first():
        return redirect(url_for("home"))
    
    chatroom_messages = Messages.query.filter_by(chatroom_code=room).all()

    return render_template("room.html", code=room, messages=chatroom_messages)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if not room or not Chatroom.query.filter_by(code=room).first():
        return 
    
    sender_name = session.get("name")
    message_body = data.get("message")
    
    # Save message to the database
    new_message = Messages(chatroom_code=room, sender_id=session["user_id"], body=message_body)
    db.session.add(new_message)
    db.session.commit()
    
    # Emit the message data to all clients in the room
    message_data = {"name": sender_name, "message": message_body}
    send(message_data, to=room)
    print(f"{sender_name} said: {message_body}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    
    if not Messages.query.filter_by(chatroom_code=room).first():
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    chatroom = Chatroom.query.filter_by(code=room).first()

    if not UserChatroom.query.filter(UserChatroom.code == room, UserChatroom.user_id == session["user_id"]).first():
        db.session.add(UserChatroom(code=room, user_id=session["user_id"]))
        db.session.commit()

    if not Participants.query.filter(Participants.code == room, Participants.user_id == session["user_id"]).first():
        db.session.add(Participants(code=room, user_id=session["user_id"]))
        chatroom.participants_count += 1
        db.session.commit()


    db.session.commit()

    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if Chatroom.query.filter_by(code=room).first():
        chatroom=Chatroom.query.filter_by(code=room).first()
        chatroom.participants_count -= 1
        if chatroom.participants_count <= 0:
            db.session.delete(chatroom)
        db.session.commit()
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

@app.route("/get_messages/<code>")
def get_messages(code):
    chatroom_messages = Messages.query.filter_by(chatroom_code=code).all()
    messages_json = []
    for message in chatroom_messages:
        messages_json.append({
            'sender': message.sender.username, 
            'body': message.body,
            'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(messages=messages_json)

@app.route("/delete_message/<msg>", methods=["DELETE"])
def delete_message(msg):
    message = Messages.query.filter_by(body=msg).first()
    if not message:
        return jsonify({"error": "NOO MESSAGE"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "DELETED MESSAGE"}), 200


if __name__ == "__main__":
    socketio.run(app, debug=True)