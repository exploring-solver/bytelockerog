Great! Let’s go step-by-step through the process of setting up the first stage of your **ByteLocker** Flask project. I will give you the terminal commands, as well as the basic code for the files based on the structure and setup we discussed.

### Step 1: Set Up a Virtual Environment
First, create a virtual environment to isolate your dependencies.

#### Terminal Commands:
```bash
# Create project directory
mkdir ByteLocker
cd ByteLocker

# Create and activate a virtual environment (assuming Python 3)
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Flask and Dependencies
Now, install Flask and the necessary dependencies.

#### Terminal Commands:
```bash
# Install Flask and required packages
pip install Flask Flask-SQLAlchemy Flask-Migrate

# Install other dependencies (OpenCV, Dlib)
pip install opencv-python dlib
```

### Step 3: Create Project Directory Structure
Now, let’s create the directory structure for the first stage (Attendance and Face Tracking System).

#### Terminal Commands:
```bash
# Create directories
mkdir app app/controllers app/models app/routes app/utils app/static app/templates migrations tests

# Create empty __init__.py files to make directories Python packages
touch app/__init__.py app/controllers/__init__.py app/models/__init__.py app/routes/__init__.py app/utils/__init__.py

# Create the core files
touch server.py app/config.py manage.py
```

### Step 4: Create and Populate the Files
Now, let's create the basic structure of the files with the code I previously outlined for the first stage.

#### 1. **`server.py`**:
This is the entry point of your Flask app.

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### 2. **`app/__init__.py`**:
Initialize the Flask app, database, and register blueprints (routes).

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration setup
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.routes import attendance
    app.register_blueprint(attendance.bp)

    return app
```

#### 3. **`app/config.py`**:
Define your app configuration, including the database URI.

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///byte_locker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret')
```

#### 4. **`app/routes/attendance.py`**:
Define routes for attendance marking and logging unidentified individuals.

```python
from flask import Blueprint, jsonify, request
from app.controllers.attendance_controller import mark_attendance, log_unidentified

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/mark', methods=['POST'])
def mark():
    data = request.get_json()
    result = mark_attendance(data)
    return jsonify(result)

@bp.route('/log_unidentified', methods=['POST'])
def log():
    data = request.get_json()
    result = log_unidentified(data)
    return jsonify(result)
```

#### 5. **`app/controllers/attendance_controller.py`**:
Implement basic attendance and logging functions (you will expand this later).

```python
def mark_attendance(data):
    # Placeholder function to process attendance marking
    # Logic for facial recognition here
    return {"status": "success", "message": "Attendance marked"}

def log_unidentified(data):
    # Log unidentified individuals
    return {"status": "success", "message": "Unidentified individual logged"}
```

#### 6. **`app/models/user.py`**:
Define the user model for storing user data.

```python
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    face_data = db.Column(db.LargeBinary, nullable=False)  # Facial embedding or image data
    
    def __repr__(self):
        return f'<User {self.name}>'
```

#### 7. **`app/models/attendance_log.py`**:
Define a model to store attendance logs.

```python
from app import db

class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AttendanceLog User {self.user_id} Entry {self.entry_time}>'
```

#### 8. **`app/utils/face_recognition.py`**:
Define basic utility functions for facial recognition.

```python
import cv2
import dlib

def recognize_face(image):
    # Placeholder for facial recognition logic
    return True  # Assume face recognized for now

def capture_unidentified_face(image):
    # Capture and log unidentified individual
    pass
```

### Step 5: Setting up Database Migrations
To manage the database schema, use **Flask-Migrate** for handling database migrations.

#### 1. **`manage.py`**:
This file will handle migrations and database-related commands.

```python
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app, db

app = create_app()
manager = Manager(app)

# Add the database migration command
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

#### Terminal Commands to Initialize Database and Migrations:

```bash
# Initialize migration scripts
flask db init

# Generate migration script (will generate based on models created)
flask db migrate

# Apply migration (create tables in the database)
flask db upgrade
```

### Step 6: Run the Application
Now that everything is set up, run the Flask development server.

#### Terminal Command:
```bash
# Run the Flask app
python server.py
```

You should now be able to access the application at `http://127.0.0.1:5000`.

- To **mark attendance**, you can make a POST request to `http://127.0.0.1:5000/attendance/mark` with the appropriate data.
- To **log unidentified individuals**, make a POST request to `http://127.0.0.1:5000/attendance/log_unidentified`.

### Step 7: Test the Application
Create a basic test case to ensure everything is working.

#### **`tests/test_attendance.py`**:
```python
import unittest
from app import create_app

class TestAttendance(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_mark_attendance(self):
        response = self.client.post('/attendance/mark', json={"user_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json['status'])

if __name__ == "__main__":
    unittest.main()
```

### Conclusion
This setup provides the basic structure for your **ByteLocker** project with Flask, including routes, controllers, models, and utilities for facial recognition. It is designed to be scalable as you continue developing new features like access control, logging, and monitoring.

Once this is running, you can begin integrating the facial recognition logic using **OpenCV** and expand the attendance marking functionality accordingly.

Let me know if you need any further assistance!


To kickstart your ByteLocker project, I'll help you create a scalable folder structure that aligns with each stage of your project, allowing easy addition of features as you progress through the various phases of development. We'll also include placeholders for functions, controllers, routes, and the server setup. Here's how to structure your project:

### Step 1: Folder Structure
We'll use **Flask** as your backend framework. Here's a recommended folder structure:

```bash
ByteLocker/
│
├── app/
│   ├── __init__.py                # Initialize app, database, routes
│   ├── routes/
│   │   ├── __init__.py            # Initialize routes
│   │   ├── attendance.py          # Attendance related routes
│   │   ├── access_control.py      # Access control related routes
│   │   ├── monitoring.py          # Campus-wide monitoring related routes
│   ├── controllers/
│   │   ├── __init__.py            # Initialize controllers
│   │   ├── attendance_controller.py   # Functions for attendance management
│   │   ├── access_control_controller.py   # Functions for access control
│   │   ├── monitoring_controller.py      # Functions for campus monitoring
│   ├── models/
│   │   ├── __init__.py            # Initialize models
│   │   ├── user.py                # User database model
│   │   ├── attendance_log.py      # Attendance log model
│   │   ├── access_log.py          # Access log model
│   │   ├── unidentified_log.py    # Unidentified individual log model
│   ├── utils/
│   │   ├── __init__.py            # Utility functions for the app
│   │   ├── face_recognition.py    # Facial recognition related functions
│   │   ├── logging_utils.py       # Logging functions for attendance and access control
│   ├── static/                    # Static files (CSS, images)
│   ├── templates/                 # HTML templates for the admin dashboard (if using Jinja2)
│   └── config.py                  # Configuration file for database, environment variables
│
├── migrations/                    # Database migration scripts (if using Flask-Migrate)
├── tests/                         # Unit and integration tests
│   ├── test_attendance.py         # Test cases for attendance module
│   ├── test_access_control.py     # Test cases for access control module
│   ├── test_monitoring.py         # Test cases for campus monitoring
├── requirements.txt               # Project dependencies
├── .gitignore                     # Git ignore file
├── README.md                      # Documentation for the project
├── manage.py                      # Command-line interface for running the app, migrations, etc.
└── server.py                      # Entry point to start the server
```

### Step 2: Basic File and Code Setup

Let's break down the key files with placeholder code to get you started:

#### `server.py`
This will be the entry point for your Flask application.

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### `app/__init__.py`
This file will initialize the Flask app, database, and register your routes.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints (routes)
    from app.routes import attendance, access_control, monitoring
    app.register_blueprint(attendance.bp)
    app.register_blueprint(access_control.bp)
    app.register_blueprint(monitoring.bp)
    
    return app
```

#### `app/routes/attendance.py`
This file contains the routes for the attendance system.

```python
from flask import Blueprint, jsonify, request
from app.controllers.attendance_controller import mark_attendance, log_unidentified

bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@bp.route('/mark', methods=['POST'])
def mark():
    data = request.get_json()
    result = mark_attendance(data)
    return jsonify(result)

@bp.route('/log_unidentified', methods=['POST'])
def log():
    data = request.get_json()
    result = log_unidentified(data)
    return jsonify(result)
```

#### `app/controllers/attendance_controller.py`
The controller will handle the business logic for attendance, such as facial recognition and logging.

```python
def mark_attendance(data):
    # Placeholder function to process attendance marking
    # Facial recognition logic here
    return {"status": "success", "message": "Attendance marked"}

def log_unidentified(data):
    # Log unidentified individuals
    return {"status": "success", "message": "Unidentified individual logged"}
```

#### `app/models/user.py`
This model represents the user data in the database.

```python
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    face_data = db.Column(db.LargeBinary, nullable=False)  # Facial embedding or image data
    
    def __repr__(self):
        return f'<User {self.name}>'
```

#### `app/utils/face_recognition.py`
This file will contain the utility functions for facial recognition using OpenCV, Dlib, or FaceNet.

```python
import cv2
import dlib

def recognize_face(image):
    # Placeholder for facial recognition logic
    return True  # Assume face recognized for now

def capture_unidentified_face(image):
    # Capture and log unidentified individual
    pass
```

#### `config.py`
This is where you configure your app settings such as the database URL and other environment variables.

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///byte_locker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret')
```

### Step 3: Testing
Create basic test files to ensure each component functions correctly.

#### `tests/test_attendance.py`
```python
import unittest
from app import create_app

class TestAttendance(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_mark_attendance(self):
        response = self.client.post('/attendance/mark', json={"user_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json['status'])

if __name__ == "__main__":
    unittest.main()
```

### Step 4: Dependencies
Create a `requirements.txt` file for your Python dependencies.

```
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
OpenCV-python==4.5.3
dlib==19.22
tensorflow==2.6.0
```

### Step 5: Running the Project
1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:

   ```bash
   python server.py
   ```

3. For database migrations (if needed):

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

### Conclusion
With this folder structure and basic file setup, you now have a foundation for developing ByteLocker. Each file has been designed with future expansion in mind, so as you proceed through the various stages of the project, you'll be able to add new features and extend the system with ease.