import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)

    def __init__(self, type):
        self.type = type

    @property
    def serialize(self):
        # return book data in serializable format
        return {
            'id': self.id,
            'type': self.type
        }

# class to store user info


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    dob = Column(String(10), nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(String(100), nullable=False)
    register_date = Column(String(10), nullable=False)
    type_id = Column(Integer, ForeignKey('types.id'))
    picture = Column(String(100))

    type = relationship(Type)

    # address_id = Column(Integer, ForeignKey("user_details.details_id"))
    # details_id = Column(Integer, ForeignKey("user_address.address_id"))

    def __init__(self, first_name, last_name, email, gender, dob,
                 phone, address, country, register_date, type_id, picture):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.dob = dob
        self.phone = phone
        self.address = address["street"] + ", " + address["city"] + ", " + \
            address["state"] + ", " + str(address["postcode"]) + \
            ", " + country
        self.register_date = register_date
        self.type_id = type_id
        self.picture = picture

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
            'register_date': self.register_date,
            'type_id': self.type_id,
            'picture': self.picture
        }


engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
