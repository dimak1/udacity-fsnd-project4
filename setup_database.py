import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class Type(Base):
    """ Type object to represent a User's type/category """

    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    desc = Column(String(20), nullable=False)

    def __init__(self, desc):
        self.desc = desc

    @property
    def serialize(self):
        return {
            'id': self.id,
            'desc': self.desc
        }


class User(Base):
    """ User object to encapsulate Users's information """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    dob = Column(String(10), nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(String(70), nullable=False)
    city = Column(String(20), nullable=False)
    state = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)
    post = Column(String(8), nullable=False)
    register_date = Column(String(10), nullable=False)
    type_id = Column(Integer, ForeignKey('types.id'))
    picture = Column(String(100))
    admin_id = Column(String(50), nullable=False)

    type = relationship(Type)

    def __init__(self, first_name, last_name, email, gender, dob,
                 phone, address, city, state, country, post,
                 register_date, type_id, picture, admin_id):

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.dob = dob
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.post = post
        self.register_date = register_date
        self.type_id = type_id
        self.picture = picture
        self.admin_id = admin_id

    @property
    def serialize(self):
        # return book data in serializable format
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'gender': self.gender,
            'dob': self.dob,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'post': self.post,
            'register_date': self.register_date,
            'type_id': self.type_id,
            'picture': self.picture
        }


engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
