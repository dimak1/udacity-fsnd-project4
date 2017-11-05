# Full Stack Nanodegree Program - Udacity
# Project 4 - Items Catalog
# Author - Dima K
# Date - Nov 2017

from flask import Flask, jsonify, request, render_template
from flask import make_response, redirect, url_for
import psycopg2
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from setup_database import Base, User, Type

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Client secret json from Google
secret_file = json.loads(open('client_secret.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']

# Alert message used to display CRUD notifications on the page
alert = ""


def setAlert(type, msg):
    """ Set message to be displayed on upon
        success or error of CRUD operations """
    global alert
    alert = {'type': type,
             'msg': msg}


def getAlert():
    """ Get message to be displayed.
        Clear message so it won't be diplayed upon page reload """
    global alert
    alert_msg = alert
    alert = ""
    return alert_msg


@app.route("/gconnect", methods=['POST'])
def gconnect():
    """ Connect to Google for user authentication """

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print("Signed in with Google!")

    # Return logged in user name as a response
    response = make_response(json.dumps(login_session['username']), 200)

    return response


@app.route('/gdisconnect')
def gdisconnect():
    """ Disconnect from Google and revoke access token """

    access_token = login_session['access_token']

    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke access token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=' + \
        login_session['access_token']

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Check status of revoke call
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/getState')
def getState():
    """ Get a session state for app user """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return state


@app.route('/')
def home():
    return render_template("home.html", login_session=login_session)


@app.route('/dashboard')
def dashboard():
    """ Diplay Dashboard page with information about all Users """
    # Get count of all users from User table
    total_user_count = session.query(User).count()
    # Get all user's types from Type table
    user_types = session.query(Type)
    type_list = []
    type_count = []
    for t in user_types:
        # Populate list of types
        type_list.append(t.desc)
        # Get count of users for each type
        type_count.append(session.query(User).filter_by(type_id=t.id).count())

    return render_template("dashboard.html",
                           total_user_count=total_user_count,
                           type_list=type_list,
                           type_count=type_count,
                           login_session=login_session)


@app.route('/users/type/')
@app.route('/users')
def view_users():
    """ Display all users """
    users = session.query(User).all()
    return render_template("view-users.html",
                           users=users,
                           login_session=login_session,
                           alert=getAlert())


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """ Display details for a specific user """
    user = session.query(User).filter_by(id=user_id).first()
    return render_template("user-details.html",
                           user=user,
                           login_session=login_session,
                           alert=getAlert())


@app.route('/users/type/<int:user_type_id>')
def view_type_users(user_type_id):
    """ Display all users with a specific type """
    users = session.query(User).filter_by(type_id=user_type_id).all()
    return render_template("view-users.html",
                           users=users,
                           show_back_btn=True,
                           login_session=login_session)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """ GET: Display edit page for a specific user
        POST: Update user and redirect to User Details page """

    user = session.query(User).filter_by(id=user_id).first()
    user_types = session.query(Type)

    if request.method == 'GET':
        return render_template("edit-user.html",
                               user=user,
                               user_types=user_types,
                               login_session=login_session)

    elif request.method == 'POST':

        # If not signed in, set appropriate message
        # and render Edit User page
        if 'username' not in login_session:
            setAlert('warning', 'You must be signed in to edit this user')
            return render_template("edit-user.html",
                                   user=user,
                                   user_types=user_types,
                                   login_session=login_session,
                                   alert=getAlert())

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

        # Set success message and redirect to User Details page
        setAlert('success', 'Updated user information')
        return redirect(url_for('user_details',
                                user_id=user_id))


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Delete User and redirect to View Users page """

    user = session.query(User).filter_by(id=user_id).first()

    # If not signed in, set appropriate message
    # and render User Details page
    if 'username' not in login_session:
        setAlert('warning', 'You must be signed in to delete this user')
        return redirect(url_for('user_details',
                                user_id=user_id))

    session.delete(user)
    session.commit()

    setAlert('success', "Deleted user " + user.first_name +
             " " + user.last_name + " " + user.email)
    return redirect(url_for('view_users'))


@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    """ GET: Display Add User page
        POST: Add New User and redirect to newly added User Details page """

    if request.method == 'GET':
        user_types = session.query(Type)

    elif request.method == 'POST':

        user_types = session.query(Type)

        # If not signed in, set appropriate message
        # and render Add User page
        if 'username' not in login_session:
            setAlert('warning', 'You must be signed in to add new user')
            return render_template("add-user.html",
                                   user_types=user_types,
                                   login_session=login_session,
                                   alert=getAlert())

        # Get today's date as registration date
        now = datetime.datetime.now()
        register_date = "{0}-{1}-{2}".format(str(now.year),
                                             str(now.month), str(now.day))

        # Set user avatars depending on gender
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
            session.add(user)
            session.commit()

            # Get newly create user's info
            user = session.query(User).order_by(User.id.desc()).first()
            setAlert('success', 'Added new user ' +
                     user.first_name + ' ' + user.last_name)

            return redirect(url_for('user_details', user_id=user.id))

        except (Exception) as error:
            print("Error while adding new user.")
            setAlert('danger', 'Error while adding new user')
            return render_template("add-user.html",
                                   user_types=user_types,
                                   login_session=login_session,
                                   alert=getAlert())

    return render_template("add-user.html",
                           user_types=user_types,
                           login_session=login_session)

# JSON ENDPOINTS


@app.route('/users/json')
def all_users_json():
    """ Get json of all Users """
    all_users = session.query(User).all()
    return jsonify(data=[user.serialize for user in all_users])


@app.route('/users/<int:user_id>/json')
def user_json(user_id):
    """ Get json of specific User """
    user = session.query(User).filter_by(id=user_id).first()
    return jsonify(data=[user.serialize])


@app.route('/users/types/json')
def all_user_types_json():
    """ Get json of all Types """
    all_types = session.query(Type).all()
    return jsonify(data=[user_type.serialize for user_type in all_types])


@app.route('/users/type/<int:type_id>/json')
def user_type_json(type_id):
    """ Get json of a specific Type """
    user_type = session.query(Type).filter_by(id=type_id).first()
    return jsonify(data=[user_type.serialize])


if __name__ == '__main__':
    app.secret_key = 'app_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
