from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Adicione esta linha para habilitar CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/batepapo'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    media_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

def encrypt_aes(key, plaintext):
    key = key.ljust(32)[:32].encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_aes(key, encrypted):
    key = key.ljust(32)[:32].encode('utf-8')
    encrypted = base64.b64decode(encrypted.encode('utf-8'))
    iv = encrypted[:16]
    ciphertext = encrypted[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    key = data['key']
    message = data['message']
    media_type = data.get('media_type', None)

    encrypted_message = encrypt_aes(key, message)
    new_message = Message(user_id=data['user_id'], message=encrypted_message, media_type=media_type)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'status': 'success'})

@app.route('/get_messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    messages = Message.query.filter_by(user_id=user_id).all()
    key = request.args.get('key')

    decrypted_messages = []
    for msg in messages:
        decrypted_msg = decrypt_aes(key, msg.message)
        decrypted_messages.append({'message': decrypted_msg, 'media_type': msg.media_type})

    return jsonify(decrypted_messages)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
