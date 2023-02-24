from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
# app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add semple user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TestLastName", img_url="TestURL")

        db.session.add(user)
        db.session.commit()

        post = Post(title="TestTitle", content="TestContent", user_id=user.id)

        db.session.add(post)
        db.session.commit()

        print('USERS-')

        print(user)
        print(user.id)

        print('POSTS-')

        print(post)
        print(post.id)

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        # db.session.rollback()

    # TESTS - USER ROUTES

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            # Maybe add more?

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)

    def test_add_user_post(self):
        with app.test_client() as client:
            d = {
                "first_name":"TestAddFirst",
                "last_name":"TestAddLast",
                "img_url":"TestAddURL"
            }

            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestAddFirst", html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/delete" method="POST" style="display: inline;"><button class="btn btn-danger">Delete</button></form>', html)

    # v THIS TEST FAILS DUE TO ISSUES WITH CASCADING DELETE

    def test_user_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Users', html)
            self.assertNotIn('TestFirstName', html)

    # ^ THIS TEST FAILS DUE TO ISSUES WITH CASCADING DELETE

    def test_edit_user_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/edit" method="POST">', html)

    def test_edit_user_post(self):
        with app.test_client() as client:

            d = {
                "first_name":"TestEditFirst",
                "last_name":"TestEditLast",
                "img_url":"TestEditURL"
            }

            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("TestEditFirst", html)
            self.assertNotIn("TestAddFirst", html)

    # TESTS - POST ROUTES

    def test_post_details(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/posts/{self.post_id}/delete" method="POST" style="display: inline;"><button class="btn btn-danger">Delete</button></form>', html)

    def test_post_add(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/posts/add" method="POST">', html)

    def test_post_add_submit(self):
        with app.test_client() as client:

            d = {

                "title":"TestAddTitle",
                "content":"TestAddContent"

            }

            resp = client.post(f"/users/{self.user_id}/posts/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'TestAddTitle', html)

    def test_delete_post_submit(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'TestTitle', html)

    def edit_post_details_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/posts/{self.post_id}/edit" method="POST">', html)

    def edit_post_details_submit(self):
        with app.test_client() as client:

            d = {

                "title":"TestEditTitle",
                "content":"TestEditContent"

            }

            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'TestEditTitle', html)