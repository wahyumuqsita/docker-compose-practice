from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuring the database
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'password')
db_host = os.getenv('DB_HOST', 'db')
db_name = os.getenv('DB_NAME', 'mydatabase')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

db.create_all()

@app.route('/message', methods=['POST'])
def create_message():
    content = request.json['content']
    message = Message(content=content)
    db.session.add(message)
    db.session.commit()
    return jsonify({'id': message.id, 'content': message.content}), 201

@app.route('/message/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify({'id': message.id, 'content': message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)