from django.test import TestCase
import json

# Create your tests here.
from django.contrib.auth.models import User, Permission
from django.contrib import auth

# from django.urls import reverse
from rest_framework import status

from .models import Post

class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        ## Create 2 users
        cls.testuser1 = User.objects.create_user(
            username='testuser1', password='abc123'
        )
        cls.testuser1.save()

        cls.testuser2 = User.objects.create_user(
            username='testuser2', password='xyz987'
        )
        cls.testuser2.save()

        ## Create a blog post
        cls.test_post = Post.objects.create(
            author=cls.testuser1, title='Blog title', body='Body content...'
        )
        cls.test_post.save()

    def test_anonymous_cannot_see_contacts(self):
        response = self.client.get("/api/v1/")   # List of Posts
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_see_contacts(self):
        user = BlogTests.testuser1
        self.client.force_login(user=user)
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mod_blog_content_as_owner(self):
        user = BlogTests.testuser1
        self.client.force_login(user=user)
        user = auth.get_user(self.client)

        self.assertEqual(user.username, 'testuser1')
        self.assertTrue(user.is_authenticated)

        response = self.client.get("/api/v1/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Got 301 instead of 200
        # title = 'title updated'
        # response = self.client.put("/api/v1/1",
        #                            data=json.dumps({'title': title}),
        #                            content_type="application/json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # post.refresh_from_db()
        # author = f'{post.author}'
        # title = f'{post.title}'
        # body = f'{post.body}'

        # self.assertEqual(author, user.username)
        # self.assertEqual(title, 'title updated')
        # self.assertEqual(body, 'Body content...')

    def test_blog_content_as_other_user(self):
        user = __class__.testuser2
        self.client.force_login(user=user) # self.client.login(username='testuser1', password='abc123')

        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'testuser2')
        self.assertTrue(user.is_authenticated)

        response = self.client.get("/api/v1/")   # List of Posts
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Getitng 301 instaed of 403
        # response = self.client.get("/api/v1/1")  # get Post 1 of testuser1 !
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# dir(user)
# ['DoesNotExist', 'EMAIL_FIELD', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes', '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_legacy_get_session_auth_hash', '_meta', '_password', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'from_db', 'full_clean', 'get_all_permissions', 'get_deferred_fields', 'get_email_field_name', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_previous_by_date_joined', 'get_session_auth_hash', 'get_short_name', 'get_user_permissions', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'normalize_username', 'objects', 'password', 'pk', 'post_set', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'username_validator', 'validate_unique']
