import flask
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User, bcrypt
from routes import routes
import os

app = Flask(__name__)
# Enable CORS for all routes and all origins
CORS(app)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'
app.config['JWT_SECRET_KEY'] = 'jwt_secret'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Set to a number of seconds if you want tokens to expire

# Connect SQLAlchemy db, bcrypt, jwt to the app
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Create the database
with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")
    # Check if admin already exists before adding
    admin = User.query.filter_by(email="admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            role="admin"
        )
        admin.set_password("admin1234")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")

# Register routes from routes.py
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True, port=5006)