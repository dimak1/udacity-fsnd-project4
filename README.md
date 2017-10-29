# Items Catalogue

Forth project from Udacity's [Full-Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### About

For this project I built a User Membership Management App to view, add, edit and delete users from database (CRUD operations).

Each user has basic information along with a type of membership.

There are two databases:
- User (to hold all users)
- Type (to hold all user types)

##### User table

| id `PK` | first_name | last_name | email | gender | dob | phone | address | city | state | country | post | register_date | type_id `FK` | picture |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Don | Arnold | don.arnold@example.com | M | 1970-03-05 | (973)-130-6982 | 3741 Spring St | Eugene | New York | US | 12594 | 2013-05-13 | 1 | picture_url |

##### Type table

| id `PK` | type |
| --- | --- |
| 1 | new |
