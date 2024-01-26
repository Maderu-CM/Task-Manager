from app import db, User, Project, Task, Review, Rating, Review, app
from faker import Faker
import random
import bcrypt

fake = Faker()

def create_fake_users(count=10):
    with app.app_context():
        for _ in range(count):
            password = fake.password()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(
                username=fake.user_name(),
                email=fake.email(),  
                password=hashed_password
            )
            db.session.add(user)
        db.session.commit()





def create_fake_projects(count=5):
    with app.app_context():
        categories = ["IT", "AGRICULTURE", "DAM CONSTRUCTION", "SOLAR DESIGN", "NETWORK DESIGN"]
        users = User.query.all() 

        for _ in range(count):
            title = fake.word()
            objective = fake.text()
            category = random.choice(categories)
            user = random.choice(users)

            project = Project(
                title=title,
                objective=objective,
                category=category,
                user_id=user.id,
                
            )

            db.session.add(project)

        db.session.commit()


def create_fake_tasks(count=15):
    with app.app_context():
        users = User.query.all()
        projects = Project.query.all()

        existing_titles = set()  # Keep track of existing titles to ensure uniqueness

        for _ in range(count):
            user = random.choice(users)
            project = random.choice(projects)

            # Generate a unique title
            title = fake.word()
            while title in existing_titles:
                title = fake.word()
            existing_titles.add(title)

            description = fake.text()
            priority = random.choice(["HIGH", "LOW", "MEDIUM"])
            start_date = fake.date_this_decade()
            due_date = fake.date_between(start_date, '+7d') 
            status = random.choice(["PENDING", "COMPLETED"])

            task = Task(
                user_id=user.id,
                project_id=project.id,
                title=title,
                description=description,
                priority=priority,
                start_date=start_date,
                due_date=due_date,
                status=status
            )

            db.session.add(task)

        db.session.commit()


def create_fake_reviews(count=15):
    with app.app_context():
        users = User.query.all()
        projects = Project.query.all()
        
        for _ in range(count):
            user = random.choice(users)
            project = random.choice(projects)
            
            comment = fake.text()  
            
            review = Review(
                user_id=user.id,
                project_id=project.id,
                comment=comment,
            )
            db.session.add(review)
        
        db.session.commit()


def create_fake_ratings(count=10):
    with app.app_context():
        users = User.query.all()
        
        for _ in range(count):
            user = random.choice(users)
            
            feedback = fake.text() 
            rating = random.randint(1, 5)  
            
            rating_instance = Rating(
                user_id=user.id,
                rating=rating,
                feedback=feedback,
            )
            db.session.add(rating_instance)
        
        db.session.commit()
        

if __name__ == "__main__":
    with app.app_context():
        create_fake_users()
        create_fake_projects()
        create_fake_tasks()
        create_fake_reviews()
        create_fake_ratings()
       
    print("Seeding completed successfully.")
