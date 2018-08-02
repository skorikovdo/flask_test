from flask import Flask, request, Response, jsonify, make_response
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
        user = User(name=form['name'])
        db.session.add(user)
        db.session.commit()
        return Response(response='Ok', status=200)
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
    """
    Follow: User X now follows user Y
    If User X now follows user Y is True -> Unfollow: User X no longer follows user Y
    Выводим
    """
    from model import User, followers
    if request.method == 'POST':
        form = request.get_json(force=True)
        user = User.query.filter(User.id == form['follower_id']).one()
        foll = User.query.filter(User.id == form['followed_id']).one()
        if foll in user.followed.all():
            user.followed.remove(foll)
            db.session.commit ()
        else:
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


@app.route('/api/message/create', methods=['POST'])
def create_message():
    from model import Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        message = Message(user_id=form['user_id'], message_text=form['message_text'])
        db.session.add(message)
        db.session.commit()
    return Response(status=200)


@app.route('/api/message/post', methods=['POST'])
def user_post():
    """
    Post(X,Y): Post message X as user Y
    """
    from model import User, Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        id={}
        for i in Message.query.all():
            print(i.id, i.user.id)
            if int(form['id']) == i.user.id:
                for m in Message.query.filter(Message.user_id == form['id']).order_by(Message.date_time.desc()).all():
                    id[m.id] = {'message_text': m.message_text, 'user_id': m.user.id, 'user': m.user.name}
                    print(id)
                return jsonify(id)
    return Response(status=404)




@app.route('/api/message/timeline', methods=['POST'])
def timeline():
    from model import Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        user = User.query.filter(User.id == form['id']).one()
        id = {}
        n = 1
        id = {}
        for i in user.followed.all ():
            message_timeline = db.session.query (User.name, Message.message_text, Message.date_time).filter (
                User.id == Message.user_id, User.id == i.id).order_by (
                Message.date_time.desc ()).one ()
            if message_timeline:
                id[user.name + str(n)] = {'user_name': message_timeline[0], 'message': message_timeline[1], 'datetime': message_timeline[2]}
                n += 1
        return jsonify(id)
    return Response(status=404)


if __name__ == '__main__':
    from model import *
    db.create_all ()
    app.run ()
