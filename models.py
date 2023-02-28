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
                    nullable=True,
                    unique=True)
    
    img_url = db.Column(db.String(),
                    nullable=True,
                    unique=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    # 'cascade="all, delete-orphan"' CAN be deleted here without effecting the behavior of the app

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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), # "ondelete='CASCADE'" CANNOT be deleted here - if it is, that reproduces the orginal issue.
                    nullable=False)

    post_tags = db.relationship('PostTag', backref ='post_tagged', cascade='all, delete-orphan')
    # 'cascade="all, delete-orphan"' CANNOT be deleted here without effecting the behavior of the app - DELETING a post which has a tag ceases to function if this is removed.

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
    
class PostTag(db.Model):
    """Post Tag"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id", ondelete='CASCADE'), # "ondelete='CASCADE" CAN be deleted here. As long as the cascade=all, delete-orphan remains everything continues to work
                    primary_key=True,
                    nullable=True)

    tag_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id", ondelete='CASCADE'), # "ondelete='CASCADE" CAN be deleted here. As long as the cascade=all, delete-orphan remains everything continues to work
                    primary_key=True,
                    nullable=True)

# MIKAEL - Code is exhibiting two completely different behaviors - for the relationship between Post and Users - your solution works, however it does not work when implemented on the solution between Post and PostTag - instead cascade='all, delete-orphan' MUST be included. I am at a loss for why only differing solutions seem to work in these two very similar cases.

# Hedging my bets and just doing both seems to be failsafe... at least in this case. Trying to find a solution that produces consistant behavior when using these tools so I am not just guessing.