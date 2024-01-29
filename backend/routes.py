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


#creating a task

@app.route('/create_task', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()

    if not current_user or 'user_id' not in current_user:
        return jsonify({'message': 'Create an account'}), 403

    user_id = current_user['user_id']

    # Check if the user exists in your database 
    user_exists = User.query.get(user_id)

    if not user_exists:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    start_date_str = data.get('start_date')
    due_date_str = data.get('due_date')
    status = data.get('status')
    project_id = data.get('project_id')  

    # Check if the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({'message': 'Project not found or does not belong to the user'}), 404

    # Convert start_date and due_date to datetime objects and then format them
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use yyyy-mm-dd'}), 400

    # Create the new task with formatted dates
    new_task = Task(
        title=title,
        user_id=user_id,
        project_id=project_id,
        description=description,
        priority=priority,
        start_date=start_date,
        due_date=due_date,
        status="Pending"
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'New Task created successfully'}), 200

#project review


@app.route('/project_review/<int:project_id>', methods=['POST'])
@jwt_required()
def project_review(project_id):
    current_user = get_jwt_identity()

    if not current_user or 'user_id' not in current_user:
        return jsonify({'message': 'Create an account'}), 403

    user_id = current_user['user_id']

    # Check if the user exists in your database
    user_exists = User.query.get(user_id)

    if not user_exists:
        return jsonify({'message': 'User not found'}), 404

    # Check if the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=user_id).first()

    if not project:
        return jsonify({'message': 'Can only be reviewed by the Project Administrator.'}), 404

    data = request.get_json()
    comment = data.get('comment')

    # Create a new review
    new_review = Review(user_id=user_id, project_id=project_id, comment=comment)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully'}), 200

#user giving a  rating and feedback
@app.route('/feedback', methods=['POST'])
@jwt_required()
def user_feedback():
    current_user = get_jwt_identity()

    if not current_user or 'user_id' not in current_user:
        return jsonify({'message': 'Create an account'}), 403

    user_id = current_user['user_id']

    data = request.get_json()
    rating = data.get('rating')
    feedback_text = data.get('feedback')

    # Check if the user exists in your database
    user_exists = User.query.get(user_id)

    if not user_exists:
        return jsonify({'message': 'User not found'}), 404

    # Create a new feedback
    new_feedback = Rating(user_id=user_id, rating=rating, feedback=feedback_text)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Thank you for your feedback!'}), 200

if __name__ == '__main__':
    app.run(debug=True)