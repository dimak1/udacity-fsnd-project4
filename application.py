from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2
import datetime
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


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):

    user = session.query(User).filter_by(id=user_id).first()

    if request.method == 'GET':
        user_types = session.query(Type)
        return render_template("edit-user.html", user=user, user_types=user_types)

    elif request.method == 'POST':

        user.first_name = request.form["firstNameInput"]
        user.last_name = request.form["lastNameInput"]
        user.email = request.form["emailInput"]
        user.phone = request.form["phoneInput"]
        user.address = request.form["addressInput"]
        user.city = request.form["cityInput"]
        user.state = request.form["stateInput"]
        user.country = request.form["countryInput"]
        user.post = request.form["postInput"]
        user.type_id = int(request.form["userTypeSelect"])

        session.add(user)
        session.commit()

        return redirect(url_for('user_details', user_id=user_id))


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = session.query(User).filter_by(id=user_id).first()
    session.delete(user)
    session.commit()

    return render_template("delete-user.html", user=user, show_back_btn=True)


@app.route('/users/add', methods=['GET', 'POST'])
def add_user():

    if request.method == 'GET':
        user_types = session.query(Type)

    elif request.method == 'POST':
        now = datetime.datetime.now()
        register_date = "{0}-{1}-{2}".format(str(now.year),
                                             str(now.month), str(now.day))

        if request.form["gender"].upper() == "M":
            profile_avatar = "/static/avatar_male.png"
        else:
            profile_avatar = "/static/avatar_female.png"

        user = User(request.form["firstNameInput"],
                    request.form["lastNameInput"],
                    request.form["emailInput"],
                    request.form["gender"].upper(),
                    request.form["datepicker"],
                    request.form["phoneInput"],
                    request.form["addressInput"],
                    request.form["cityInput"],
                    request.form["stateInput"],
                    request.form["countryInput"],
                    request.form["postInput"],
                    register_date,
                    request.form["userTypeSelect"],
                    profile_avatar  # picture
                    )

        try:
            # Add user to database
            print("Updating user")
            session.add(user)
            session.commit()
            print("New user added")
            # new_user_id = session.query(User).filter(user).filter(id)
            # email=request.form["emailInput"], phone=request.form["phoneInput"])

            user = session.query(User).order_by(User.id.desc()).first()

            return redirect(url_for('user_details', user_id=user.id))

        except (Exception) as error:
            print("Error while adding new user: ")
            msg = "Failed to add new user."
            result = "danger"
            return redirect(url_for('view_users'))

    return render_template("add-user.html", user_types=user_types)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
