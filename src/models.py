import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

follower_table = Table('follower', Base.metadata,
    Column('user_from_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('user_to_id', Integer, ForeignKey('user.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    followed = relationship(
        'User', secondary=follower_table,
        primaryjoin=(follower_table.c.user_from_id == id),
        secondaryjoin=(follower_table.c.user_to_id == id),
    )
    post = relationship('Post')
    comment = relationship('Comment')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media = relationship('Media')
    comment = relationship('Comment')

class Media(Base):
    __tablename__ = 'media'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type'), nullable=False)
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    comment_text = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
