# Item Catalog

Forth project from Udacity's [Full-Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### About

For this project I built a __User Management App__ with following features:
 - View, Add, Edit or Delete Users (CRUD operations)
 - Dashboard
 - Google authentication
 - Generate random User data via [API](https://randomuser.me/)

> Note: __Google Account__ is required to Sign In to the app to _Add_, _Edit_ or _Delete_ Users. All other features available without sign in.

Each `User` has basic information along with its `Type` (New, Promotion, Pay-As-You-Go, Subscribed, Inactive, Cancelled).

There are two tables:
- `User` (to hold all Users)
- `Type` (to hold all Types of Users)

##### User table

| id `PK` | first_name | last_name | email | gender | dob | phone | address | city | state | country | post | register_date | type_id `FK` | picture |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Don | Arnold | don.arnold@example.com | M | 1970-03-05 | (973)-130-6982 | 3741 Spring St | Eugene | New York | US | 12594 | 2013-05-13 | 1 | picture_url |

##### Type table

| id `PK` | type |
| --- | --- |
| 1 | new |

### How to setup

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html).

Clone this repo into `user-app` folder:

```
$ git clone https://github.com/dimak1/udacity-fsnd-project4.git user-app
```

### How to run

Start virtual machine and log in to it:

```
$ cd user-app
$ vagrant up
$ vagrant ssh
```

Once logged in, populate database and run the app:
```
$ python3 populate_database.py
$ python3 application.py
```

Go to application at http://localhost:5000/

### Screenshots

![Home Page](https://github.com/dimak1/udacity-fsnd-project4/tree/master/static/screenshots/home-page.png)

![View Users Page](https://github.com/dimak1/udacity-fsnd-project4/tree/master/static/screenshots/view-users.png)
