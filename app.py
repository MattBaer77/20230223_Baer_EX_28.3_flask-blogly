"""Blogly application."""
import os
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from helpers import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.route('/')
def root():
    """Shows a list of all users"""

    return redirect('/users')

# USER ROUTES

@app.route('/users')
def users():
    """Shows a list of all users"""

    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Shows a form to add a user"""

    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def add_user_post():
    """Accepts form input, Adds a user to the database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    replace_user_values_empty_with_null(new_user)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Dispalys details of one user"""

    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user.id).all()

    return render_template("user-detail.html", user=user, user_posts=user_posts)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    """Deletes a user"""

    user = User.query.filter_by(id = user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows a form to edit a user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_post(user_id):

    user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    replace_user_values_empty_with_null(user)

    # db.session.add(user)
    db.session.commit()

    return redirect('/users')

# POST ROUTES

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """displays the content of a post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post-detail.html", post=post)

@app.route('/users/<int:user_id>/posts/add')
def post_add(user_id):
    """shows a form to add a post for a particular user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("add-post.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/add', methods=["POST"])
def post_add_submit(user_id):
    """handles form submission and creates a post for a particular user"""

    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post_submit(post_id):
    """accepts post_id and deletes coorisponding post"""

    post = Post.query.get(post_id)

    db.session.delete(post)

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_details_form(post_id):
    """displays the content of a post"""

    post = Post.query.get(post_id)

    tags = Tag.query.all()

    return render_template("edit-post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_details_submit(post_id):
    """accepts post_id and edits coorisponding post"""

    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)

    db.session.commit()

    return render_template("post-detail.html", post=post)

# TAG ROUTES

@app.route('/tags')
def list_tags():
    """displays a list of tags"""
    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """displays tag details"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-detail.html', tag=tag)

@app.route('/tags/new')
def add_tag():
    """displays form to add new tag"""

    return render_template("add-tag.html")

@app.route('/tags/new', methods=["POST"])
def post_add_tag():
    """displays form to add new tag"""

    name = request.form["name"]

    new_tag = Tag(name=name)

    db.session.add(new_tag)

    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """displays form to edit existing tag by id"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit-tag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def post_edit_tag(tag_id):
    """posts changes to a tag by id"""

    tag = Tag.query.get_or_404(tag_id)

    name = request.form["name"]

    tag.name = name

    db.session.add(tag)

    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def post_delete_tag(tag_id):
    """deletes tag by id"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)

    db.session.commit()

    return redirect('/tags')