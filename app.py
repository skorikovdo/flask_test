from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/user/create', methods=['POST'])
def create_user():
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
        return jsonify([{'id': user.id, 'name': user.name}
                        for user in User.query.all()])
    return Response(status=404)


@app.route('/api/user/<int:user_id>', methods=['GET'])
def show_user(user_id):
    from model import User
    if request.method == 'GET':
        return jsonify([{'id': user.id, 'name': user.name}
                        for user in User.query
                                        .filter(User.id == user_id).all()])
    return Response(status=404)


@app.route('/api/followers/create', methods=['POST'])
def followers_create():
    """
    Follow: User X now follows user Y
    If User X now follows user Y is True ->
    Unfollow: User X no longer follows user Y
    Выводим
    """
    from model import User
    if request.method == 'POST':
        form = request.get_json(force=True)
        user = User.query.filter(User.id == form['follower_id']).one()
        foll = User.query.filter(User.id == form['followed_id']).one()
        if foll in user.followed.all():
            user.followed.remove(foll)
            db.session.commit()
        else:
            user.followed.append(foll)
            db.session.commit()
        return Response(status=200, response='ok')
    return Response(status=404)


@app.route('/api/followers/list', methods=['GET'])
def followers_list():
    from model import User
    if request.method == 'GET':
        user_to_followers = {}
        for user in User.query.all():
            if user.followed.all():
                user_to_followers[user.name] = [user.name for user in user.followed.all()]
        return jsonify(user_to_followers)
    return Response(status=404)


@app.route('/api/message/create', methods=['POST'])
def create_message():
    from model import Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        message = Message(user_id=form['user_id'],
                          message_text=form['message_text'])
        db.session.add(message)
        db.session.commit()
    return Response(status=404)


@app.route('/api/message/post', methods=['POST'])
def user_post():
    """
    Post(X,Y): Post message X as user Y
    """
    from model import Message
    if request.method == 'POST':
        form = request.get_json(force=True)
        post_id = {}
        for message in Message.query.all():
            if int(form['id']) == message.user.id:
                for message_user in Message.query.filter(Message.user_id == form['id'])\
                                            .order_by(Message.date_time.desc()).all():
                    post_id[message_user.id] = dict(message_text=message_user.message_text,
                                                    user_id=message_user.user.id,
                                                    user=message_user.user.name)
                return jsonify(post_id)
    return Response(status=404)


@app.route('/api/message/list', methods=['POST'])
def message_list():
    from model import Message, User
    if request.method == 'POST':
        form = request.get_json(force=True)
        user = User.query.filter(User.id == form['id']).one()
        message_id = {}
        followed_id_list = [followed.id for followed in user.followed.all()]
        for followed_message in db.session.query(Message.date_time, User.name, Message.message_text, User, Message.id).join(User) \
                .filter(User.id.in_(followed_id_list)).order_by(Message.date_time.desc()).all():
            message_id[followed_message.id] = dict(message_date_time=followed_message.date_time,
                                                   message_text=followed_message.message_text,
                                                   autor_id=followed_message.name)
        return jsonify(message_id)
    return Response(status=404)


if __name__ == '__main__':
    from model import *
    db.create_all()
    app.run()
