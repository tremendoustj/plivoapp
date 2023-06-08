from flask import request, jsonify
from . import app
from .database import session
from .models import Message

@app.route('/', methods=['GET'])
def get_home():
    return "OK"

@app.route('/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    messages = session.query(Message).filter_by(account_id=account_id).all()
    result = []
    for message in messages:
        result.append({
            'account_id': message.account_id,
            'message_id': message.id,
            'sender_number': message.sender_number,
            'receiver_number': message.receiver_number
        })
    return jsonify(result)

@app.route('/create', methods=['POST'])
def create_message():
    data = request.json
    message = Message(
        id=data['message_id'],
        account_id=data['account_id'],
        sender_number=data['sender_number'],
        receiver_number=data['receiver_number']
    )
    session.add(message)
    session.commit()
    return jsonify({'message': 'Message created successfully'})

@app.route('/search', methods=['GET'])
def search_messages():
    message_id = request.args.get('message_id')
    sender_number = request.args.get('sender_number')
    receiver_number = request.args.get('receiver_number')

    query = session.query(Message)
    if message_id:
        message_ids = message_id.split(',')
        query = query.filter(Message.id.in_(message_ids))
    elif sender_number:
        sender_numbers = sender_number.split(',')
        query = query.filter(Message.sender_number.in_(sender_numbers))
    elif receiver_number:
        receiver_numbers = receiver_number.split(',')
        query = query.filter(Message.receiver_number.in_(receiver_numbers))

    messages = query.all()
    result = []
    for message in messages:
        result.append({
            'account_id': message.account_id,
            'message_id': message.id,
            'sender_number': message.sender_number,
            'receiver_number': message.receiver_number
        })
    return jsonify(result)
