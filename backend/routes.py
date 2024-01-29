import re  # Import the regular expression module
from flask import jsonify, request
from app import app, db, User, Project, Task, Review, Rating
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_current_user, unset_jwt_cookies
from datetime import datetime
from sqlalchemy.exc import IntegrityError



CORS(app)

bcrypt = Bcrypt(app)


app.config['JWT_SECRET_KEY'] = 'adasdassgvgtAdsffdFFdbnmR'
jwt = JWTManager(app)


# User registration

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if all fields are filled
    if not username or not email or not password:
        return jsonify({'message': 'Please fill all fields!'}), 400

    # Validate username uniqueness
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({'message': 'Username already taken!'}), 400

    # Validate email format
    email_pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'message': 'Invalid email format!'}), 400

    # Validate email uniqueness
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'message': 'Email already in use!'}), 400

    # Validate password strength
    if len(password) < 8 or not any(c.islower() for c in password) \
            or not any(c.isupper() for c in password) \
            or not any(c.isdigit() for c in password) \
            or not any(c in '!@#$%^&*()-_+=<>,.?/:;{}[]|' for c in password):
        return jsonify({
            'message': 'Password must be at least 8 characters long and include '
                       'at least one uppercase letter, one lowercase letter, '
                       'one digit, and one special character!'
        }), 400

    # Hash and store the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
    )

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 200


# user login

@app.route('/login_user', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'user_id': user.id})
        return jsonify({'access_token': access_token, 'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid Credentials!'}), 401

# creating a project
@app.route('/createproject', methods=['POST'])
@jwt_required()
def create_project():
    current_user = get_jwt_identity()

    if not current_user or 'user_id' not in current_user:
        return jsonify({'message': 'Create an account'}), 403

    user_id = current_user['user_id']

    # Check if the user exists in your database or handle it according to your authentication mechanism
    user_exists = User.query.get(user_id)

    if not user_exists:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    title = data.get('title')
    objective = data.get('objective')
    category = data.get('category')

    new_project = Project(
        title=title,
        objective=objective,
        category=category,
        user_id=user_id
    )

    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'New Project created successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
