"""Seed file to make sample data for pets db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name='Whiskey', last_name="Bandit", img_url="https://upload.wikimedia.org/wikipedia/commons/4/49/Jonathan_G_Meath_portrays_Santa_Claus.jpg")
bowser = User(first_name='Bowser', last_name="Bonger", img_url="https://upload.wikimedia.org/wikipedia/commons/4/49/Jonathan_G_Meath_portrays_Santa_Claus.jpg")
spike = User(first_name='Spike', last_name="Willow", img_url= None)
lee = User(first_name='Lee', last_name="Bird", img_url= None)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(lee)

# Commit--otherwise, this never gets saved!
db.session.commit()

# If table isn't empty, empty it
Post.query.delete()

# Add posts
whiskey_post = Post(title='The Dude', content='As it turns out, the dude does in fact abide. He is abiding right now... Just look at him!', user_id=1)
whiskey_post2 = Post(title='The moon: not real.', content='It is actually just a projetion by the government.', user_id=1)
whiskey_post3 = Post(title='Birds: not real.', content='Much like bigfoot, nobody has ever actually seen a bird.', user_id=1)

bowser_post = Post(title='Whiskey lost it', content='Whiskey Bandit is very strange and silly. He is right about the moon though...', user_id=2)

spike_post = Post(content='Surrounded by idiots', user_id=3)

db.session.add_all([whiskey_post, whiskey_post2, whiskey_post3, bowser_post, spike_post])

db.session.commit()