import datetime
import unittest
from app import app
from app.models import User, Post, Follow, FollowHelpers
from mongoengine import *

class UserModelTest(unittest.TestCase):
  def setUp(self):
    connect('test1', host='mongodb://pmarquette:plm080192.@ds141633.mlab.com:41633/stories-flask-test')

  def tearDown(self):
    User.drop_collection()
    Post.drop_collection()
    Follow.drop_collection()

  def test_password_hashing(self):
    new_user = User(email='test@yahoo.com', username='Sam8080')
    new_user.set_password('thisisatest')
    self.assertFalse(new_user.check_password('thisiswrong'))
    self.assertTrue(new_user.check_password('thisisatest'))

  def test_follow(self):
    user1 = User(email='test@yahoo.com', username='Sam8080')
    user2 = User(email='test2@yahoo.com', username='Jane8080')
    user1.save()
    user2.save()
    self.assertEqual(FollowHelpers.return_following(user1), [])
    self.assertEqual(FollowHelpers.return_following(user2), [])

    # user1 (Sam8080) follows user2 (Jane8080)
    Follow(user1, user2).save()
    self.assertTrue(FollowHelpers.is_following(user1, user2))
    self.assertEqual(len(FollowHelpers.return_following(user1)), 1)
    self.assertEqual((FollowHelpers.return_following(user1))[0].following_fkey.username, 'Jane8080')
    self.assertEqual(len(FollowHelpers.return_followers(user2)), 1)
    self.assertEqual((FollowHelpers.return_followers(user2))[0].follower_fkey.username, 'Sam8080')

    FollowHelpers.unfollow(user1, user2)
    self.assertFalse(FollowHelpers.is_following(user1, user2))
    self.assertEqual(len(FollowHelpers.return_following(user1)), 0)
    self.assertEqual(len(FollowHelpers.return_followers(user2)), 0)

  def test_posts(self):
    user1 = User(email='test3@uh.edu', username='Jackie700')
    user2 = User(email='test4@uh.edu', username='Arthur700')
    user1.save()
    user2.save()

    post1 = Post(body='post from jackie', user_fkey = user1, timestamp = datetime.datetime.now())
    post2 = Post(body='post from arthur', user_fkey = user2, timestamp = datetime.datetime.now())
    post3 = Post(body='post 2 from jackie', user_fkey = user1, timestamp = datetime.datetime.now())
    post1.save()
    post2.save()
    post3.save()
    
    # user1 = Jackie, user2 = Arthur
    Follow(user1, user2).save()
    Follow(user2, user1).save()
    self.assertEqual(len(FollowHelpers.return_following_posts(user1)), 1)
    self.assertEqual((FollowHelpers.return_following_posts(user1))[0].body, 'post from arthur') # Jackie is following arthur's posts
    self.assertEqual(len(FollowHelpers.return_following_posts(user2)), 2)

if __name__ == '__main__':
  unittest.main(verbosity=2)