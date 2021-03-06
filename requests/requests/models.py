from requests import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    clients = db.relationship('Clients', backref='user', lazy=True)
    requests = db.relationship('Requests', backref='user', lazy=True)
    

    def __repr__(self):
        return f"User('{self.email}','{self.username}')"


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requests = db.relationship('Requests', backref='client', lazy=True)

    def __repr__(self):
        return f"{self.name}"

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_priority = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    target_date = db.Column(db.Text, nullable= False)
    files = db.Column(db.String(200), nullable=True)
    product_area = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    def __repr__(self):
        return f"Requests('{self.title}', '{self.date_posted}')"

