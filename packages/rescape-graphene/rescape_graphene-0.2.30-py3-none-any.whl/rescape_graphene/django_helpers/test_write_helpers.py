from unittest import TestCase

from ..user.user_schema import user_fields

from .write_helpers import increment_prop_until_unique, enforce_unique_props
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class WriteHelpersTestCase(TestCase):
    client = None

    def setUp(self):
        # Prevent a circular dependency
        get_user_model().objects.update_or_create(username="cat", first_name='Simba', last_name='The Lion',
                                                  password=make_password("roar", salt='not_random'))
        get_user_model().objects.update_or_create(username="cat1", first_name='Felix', last_name='The Cat',
                                                  password=make_password("meow", salt='not_random'))

    def test_increment_prop_until_unique(self):
        user_dict = increment_prop_until_unique(get_user_model(), None, 'username',
                                    dict(username='cat', first_name='Fluffy', last_name='Mcfluffigan',
                                         password=make_password("purr", salt='not_random')))
        user, created = get_user_model().objects.update_or_create(**user_dict)
        assert user.username == 'cat2'

    def test_enforce_unique_props(self):
        user_dict = increment_prop_until_unique(get_user_model(), None, 'username',
                                    dict(username='cat', first_name='Fluffy', last_name='Mcfluffigan',
                                         password=make_password("purr", salt='not_random')))
        modifed_user_dict = enforce_unique_props(user_fields, user_dict)
        assert modifed_user_dict['username'] == 'cat2'
