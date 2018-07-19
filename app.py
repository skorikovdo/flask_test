from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask (__name__)
app.config.from_object (Config)

db = SQLAlchemy (app)


@app.route ('/')
def hello_world ():
    return 'Hello World!'


@app.route('/api/user/create', methods=['POST'])
def create_user ():
    from model import User
    if request.method == 'POST':
        form = request.get_json(force=True)
        print(form["name"])
        user = User(name=form['name'])
        db.session.add(user)
        db.session.commit()
        return Response(status=200)
    return Response(status=404)


@app.route('/api/user/list', methods=['GET'])
def user_list():
    from model import User
    if request.method == 'GET':
        return jsonify([{'id': User.id, 'name': User.name}
                        for User in User.query.all()])
    return Response(status=404)


@app.route('/api/user/<int:user_id>', methods=['GET'])
def show_user(user_id):
    from model import User
    if request.method == 'GET':
        return jsonify([{'id': User.id, 'name': User.name}
                        for User in User.query.filter(User.id == user_id).all()])
    return Response(status=404)


@app.route('/api/followers/create', methods=['POST'])
def followers_create():
    from model import User, followers
    if request.method == 'POST':
        form = request.get_json(force=True)
        user = User.query.filter(User.id == form['follower_id']).one()
        foll = User.query.filter(User.id == form['followed_id']).one()
        user.followed.append(foll)
        db.session.commit()
        return Response(status=200, response='ok')
    return Response(status=404)


@app.route('/api/followers/list', methods=['GET'])
def followers_list():
    from model import User, followers
    if request.method == 'GET':
        user_to_followers = {}
        for i in User.query.all():
            if i.followers.all() != []:
                user_to_followers[i.name] = [m.name for m in i.followers.all()]
        return jsonify(user_to_followers)
    return Response(status=404)


@app.route('/api/followers/<int:followers_id>', methods=['GET'])
def show_followers(followers_id):
    from model import User, followers
    if request.method == 'GET':
        return jsonify([{}])


@app.route('/api/message/create', methods=['POST'])
def create_message():
    from model import Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        message = Message(user_id=form['user_id'], message_text=form['message_text'])
        db.session.add(message)
        db.session.commit()
    return Response(status=200)


@app.route('/api/message/list', methods=['GET'])
def user_notification():
    from model import User, Message
    if request.method == 'GET':
        pass



if __name__ == '__main__':
    from model import *

    db.create_all ()
    app.run ()
