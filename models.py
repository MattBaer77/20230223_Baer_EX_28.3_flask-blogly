"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)



class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(20),
                    nullable=True,
                    unique=False)

    last_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    
    img_url = db.Column(db.String(),
                    nullable=True,
                    unique=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """Post Model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String(100),
                    nullable=True,
                    unique=False,
                    default='Untitled Post')

    content = db.Column(db.Text,
                    nullable=False,
                    unique=False)

    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                    nullable=False)

    post_tags = db.relationship('PostTag', backref ='post_tagged')
    tags = db.relationship('Tag', secondary='post_tags', backref ='posts')

class Tag(db.Model):
    """Tag"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.String(100),
                    nullable=False,
                    unique=True)

    # posts = db.relationship('Post', secondary='post_tags', backref ='tags')

    
class PostTag(db.Model):
    """Post Tag"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    primary_key=True,
                    nullable=False)

    tag_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id"),
                    primary_key=True,
                    nullable=False)

    __table_args__ = (db.UniqueConstraint('post_id', 'tag_id'),)

    # __table_args__ = (UniqueConstraint('post_id', 'tag_id', name="post_tag_combination"))