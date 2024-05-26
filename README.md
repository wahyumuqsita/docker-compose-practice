# Docker Compose Learning Task

This task will guide you through creating a Dockerized Python API server that interacts with a MySQL database. You'll learn how to build a Docker image, use Docker Compose to manage multi-container applications, and handle secrets for database credentials.

## Project Setup

### Step 1: Create a Python API Server

Create a file named `app.py` with the following content:

```python
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
```

### Step 2: Create a Dockerfile

Create a file named `Dockerfile` with the following content:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask sqlalchemy pymysql flask_sqlalchemy

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Step 3: Create a Docker Compose File

Create a file named `docker-compose.yml` with the following content:

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
      MYSQL_DATABASE: mydatabase
      MYSQL_USER_FILE: /run/secrets/db_user
      MYSQL_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_root_password
      - db_user
      - db_password

  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_NAME: mydatabase
      DB_USER_FILE: /run/secrets/db_user
      DB_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_user
      - db_password
    depends_on:
      - db

volumes:
  db_data:

secrets:
  db_root_password:
    file: ./secrets/db_root_password.txt
  db_user:
    file: ./secrets/db_user.txt
  db_password:
    file: ./secrets/db_password.txt
```

### Step 4: Create Secret Files

Create a directory named `secrets` in your project directory and add the following files with their respective content:

**secrets/db_root_password.txt:**
```
your_root_password
```

**secrets/db_user.txt:**
```
your_db_user
```

**secrets/db_password.txt:**
```
your_db_password
```

Replace `your_root_password`, `your_db_user`, and `your_db_password` with appropriate values.

## Running the Project

1. Open a terminal and navigate to the project directory.
2. Build and push your image to docker hub
   ```sh
   docker build simple-python-api-server:0.0.2 .
   ```
3. ssh to your server and copy/create the docker-compose.yaml file in your server.
4. Build and start the Docker containers:
   ```sh
   docker-compose up -d
   ```
5. Ensure both containers (API server and MySQL database) are running and can communicate over the same network.

## Testing the API

Use tools like `curl` or Postman to interact with the API:

### POST a message
```sh
curl -X POST -H "Content-Type: application/json" -d '{"content": "Hello, World!"}' http://localhost:5000/message
```

### GET a message
```sh
curl http://localhost:5000/message/1
```

Replace `1` with the ID of the message you want to retrieve.

## Conclusion

This task helps you learn how to:
- Build a Docker image for a Python application.
- Use Docker Compose to manage multi-container applications.
- Manage secrets for database credentials.
- Interact with a MySQL database from a Python application.

Happy learning!
