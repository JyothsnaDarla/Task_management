from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # Pending/In Progress/Completed
    priority = db.Column(db.Integer, default=1, nullable=False)  # 1=Low, 2=Medium, 3=High
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 🔑 Add this foreign key to link tasks to users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship (optional, lets you do current_user.tasks)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def due_badge(self):
        if not self.due_date:
            return 'No due date'
        return self.due_date.strftime('%d %b %Y')
