from flask import Flask, jsonify, request, render_template
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from setup_database import Base, User, Type

app = Flask(__name__)

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    user = "hey, user"
    return render_template("home.html")


@app.route('/dashboard')
def dashboard():
    # Get count of all users from User table
    total_user_count = session.query(User).count()
    # Get all user's types from Type table
    user_types = session.query(Type)
    type_list = []
    type_count = []
    for t in user_types:
        # Populate list of types
        type_list.append(t.type)
        # Get count of users for each type
        type_count.append(session.query(User).filter_by(type_id=t.id).count())

    return render_template("dashboard.html", total_user_count=total_user_count, type_list=type_list, type_count=type_count)


@app.route('/users/type/')
@app.route('/users')
def view_users():
    # Join User and Type tables to get user_type name for each user
    all_users = session.query(User).join(Type).all()
    # filter(User.type_id == Type.id).all()
    # user_types = session.query(Type).all()
    # for t in all_users:
    # print(t.type)
    return render_template("view-users.html", users=all_users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = session.query(User).filter_by(id=user_id).join(Type).first()
    return render_template("user-details.html", user=user)


@app.route('/users/type/<int:user_type_id>')
def view_type_users(user_type_id):
    users = session.query(User).filter_by(type_id=user_type_id).all()
    return render_template("view-users.html", users=users, show_back_btn=True)


@app.route('/users/add')
def add_user():
    return render_template("add-user.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
