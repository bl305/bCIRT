# -*- coding: utf-8 -*-
# **********************************************************************;
# Project           : bCIRT
# License           : GPL-3.0
# Program name      : assets/tests.py
# Author            : Balazs Lendvay
# Date created      : 2019.07.27
# Purpose           : Tests file for the bCIRT
# Revision History  : v1
# Date        Author      Ref    Description
# 2019.07.29  Lendvay     1      Initial file
# **********************************************************************;
# from django.shortcuts import render
# https://realpython.com/testing-in-django-part-1-best-practices-and-examples/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
# from django.test import TestCase
# Create your tests here.
# from django.test import TestCase
# from assets.models import Profile
# from django.utils import timezone
from django.urls import reverse
# from assets.forms import ProfileForm

# models test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User  # , Permission, Group
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from assets.models import Host



class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("TEST ASSSET setUpTestData")
        pass

    def setUp(self):
        print("TEST ASSET setUp")

        self.c = Client()
        self.user_readonly1 = User.objects.create_user(username="readonly1", email="readonly1@test.com", password="Password1.")
        self.user_readonly1.save()
        self.user_readonly2 = User.objects.create_user(username="readonly2", email="readonly2@test.com", password="Password1.")
        self.user_readonly2.save()
        self.user_write1 = User.objects.create_user(username="write1", email="write1@test.com", password="Password1.")
        self.user_write1.save()
        self.user_write2 = User.objects.create_user(username="write2", email="write2@test.com", password="Password1.")
        self.user_write2.save()
        self.user_review1 = User.objects.create_user(username="review1", email="rewview1@test.com", password="Password1.")
        self.user_review1.save()
        self.user_review2 = User.objects.create_user(username="review2", email="rewview2@test.com", password="Password1.")
        self.user_review2.save()
        self.assertTrue(self.user_readonly1.is_active)
        self.assertFalse(self.user_readonly1.is_staff)
        self.assertFalse(self.user_readonly1.is_superuser)
        self.assertTrue(self.user_readonly2.is_active)
        self.assertFalse(self.user_readonly2.is_staff)
        self.assertFalse(self.user_readonly2.is_superuser)
        self.assertTrue(self.user_write1.is_active)
        self.assertFalse(self.user_write1.is_staff)
        self.assertFalse(self.user_write1.is_superuser)
        self.assertTrue(self.user_write2.is_active)
        self.assertFalse(self.user_write2.is_staff)
        self.assertFalse(self.user_write2.is_superuser)
        self.assertTrue(self.user_review1.is_active)
        self.assertFalse(self.user_review1.is_staff)
        self.assertFalse(self.user_review1.is_superuser)
        self.assertTrue(self.user_review2.is_active)
        self.assertFalse(self.user_review2.is_staff)
        self.assertFalse(self.user_review2.is_superuser)
        # granting permissions
        appname = "assets"
        modelname = "host"

        add_host = "%s%s" % ('add_', modelname)
        add_host_perm = "%s.%s" % (appname, add_host)
        view_host = "%s%s" % ('view_', modelname)
        view_host_perm = "%s.%s" % (appname, view_host)
        change_host = "%s%s" % ('change_', modelname)
        change_host_perm = "%s.%s" % (appname, change_host)
        delete_host = "%s%s" % ('delete_', modelname)
        delete_host_perm = "%s.%s" % (appname, delete_host)

        content_type_host = ContentType.objects.get_for_model(Host)

        permission_view_host = Permission.objects.get(content_type=content_type_host, codename=view_host)
        permission_add_host = Permission.objects.get(content_type=content_type_host, codename=add_host)
        permission_change_host = Permission.objects.get(content_type=content_type_host, codename=change_host)
        permission_delete_host = Permission.objects.get(content_type=content_type_host, codename=delete_host)

        # creating the permission groups
        # group_name = "AssetsAll"
        # self.group = Group(name=group_name)
        # self.group.save()
        self.group_cirt_member, created = Group.objects.get_or_create(name='CIRT_MEMBER')
        self.group_cirt_reviewer, created = Group.objects.get_or_create(name='CIRT_REVIEWER')
        self.group_cirt_readonly, created = Group.objects.get_or_create(name='CIRT_READONLY')
        # Create new permission
        # permission = Permission.objects.create(codename='view_XX',
        #                                        name='Can view XX',
        #                                        content_type=content_type_host)
        self.group_cirt_member.permissions.add(permission_view_host)
        self.group_cirt_member.permissions.add(permission_add_host)
        self.group_cirt_member.permissions.add(permission_change_host)
        self.group_cirt_member.permissions.add(permission_delete_host)

        self.group_cirt_reviewer.permissions.add(permission_view_host)
        self.group_cirt_reviewer.permissions.add(permission_change_host)

        self.group_cirt_readonly.permissions.add(permission_view_host)

        self.user_readonly1.groups.add(self.group_cirt_readonly)
        self.user_readonly2.groups.add(self.group_cirt_readonly)

        self.user_write1.groups.add(self.group_cirt_member)
        self.user_write2.groups.add(self.group_cirt_member)

        self.user_review1.groups.add(self.group_cirt_reviewer)
        self.user_review2.groups.add(self.group_cirt_reviewer)

        # checking permissions
        # self.user_readonly1.user_permissions.add(permission_view_host)
        self.assertTrue(self.user_readonly1.has_perm(view_host_perm))

        # self.user_readonly2.user_permissions.add(permission_view_host)
        self.assertTrue(self.user_readonly2.has_perm(view_host_perm))

        # self.user_write1.user_permissions.add(
        #     permission_view_host,
        #     permission_change_host,
        #     permission_add_host,
        #     permission_delete_host)
        self.assertTrue(self.user_write1.has_perm(view_host_perm))
        self.assertTrue(self.user_write1.has_perm(change_host_perm))
        self.assertTrue(self.user_write1.has_perm(add_host_perm))
        self.assertTrue(self.user_write1.has_perm(delete_host_perm))

        # self.user_write2.user_permissions.add(
        #     permission_view_host,
        #     permission_change_host,
        #     permission_add_host,
        #     permission_delete_host)
        self.assertTrue(self.user_write2.has_perm(view_host_perm))
        self.assertTrue(self.user_write2.has_perm(change_host_perm))
        self.assertTrue(self.user_write2.has_perm(add_host_perm))
        self.assertTrue(self.user_write2.has_perm(delete_host_perm))

        # self.user_review1.user_permissions.add(permission_view_host)
        self.assertTrue(self.user_review1.has_perm(view_host_perm))

        # self.user_review2.user_permissions.add(permission_view_host)
        self.assertTrue(self.user_review2.has_perm(view_host_perm))

        # x=self.user_readonly1.get_all_permissions()
        # for xx in x:
        #     print(xx)
        #clear cache when testing perms
        # if hasattr(user, '_perm_cache'):
        #     delattr(user, '_perm_cache')

        pass

    def tearDown(self):
        print("TEST ASSET Teardown")
        self.user_readonly1.delete()
        self.user_readonly2.delete()
        self.user_write1.delete()
        self.user_write2.delete()
        self.user_review1.delete()
        self.user_review2.delete()

        self.group_cirt_member.delete()
        self.group_cirt_readonly.delete()
        self.group_cirt_reviewer.delete()
        # self.group.delete()

    # def test_create_user(self):
    #     print("TEST (Create user)")
    #     User = get_user_model()
    #     user = User.objects.create_user(username="bcirt", email='bcirt@bcirt.com', password='Password1.')
    #     user.save()
    #     self.assertEqual(user.email, 'bcirt@bcirt.com')
    #     self.assertTrue(user.is_active)
    #     self.assertFalse(user.is_staff)
    #     self.assertFalse(user.is_superuser)

        # try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            # self.assertIsNone(user.username)
            # pass
        # except AttributeError:
        #     pass
        # with self.assertRaises(TypeError):
        #     User.objects.create_user()
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(email='')
        # with self.assertRaises(ValueError):
        #     User.objects.create_user(username='bcirt', email='', password="AlmaFa1.")

    # def test_create_superuser(self):
    #     print("TEST (Create superuser)")
    #     User = get_user_model()
    #     admin_user = User.objects.create_superuser(username='admintest', email='admin@bcirt.com', password='Password1.')
    #     user.save()
    #     self.assertEqual(admin_user.email, 'admin@bcirt.com')
    #     self.assertTrue(admin_user.is_active)
    #     self.assertTrue(admin_user.is_staff)
    #     self.assertTrue(admin_user.is_superuser)


        # self.c.login(username='admin', password='Password1.')
        # response = self.c.get(reverse('assets:host_list'))
        # self.assertEqual(response.status_code, 200, u'user should have access')

        # try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            # self.assertIsNone(admin_user.username)
            # pass
        # except AttributeError:
        #     pass
        # with self.assertRaises(ValueError):
        #     User.objects.create_superuser(
        #         username='admin', email='admin@bcirt.com', password='AlmaFa1.', is_superuser=False)

    def test_user_can_access(self):
        print("TEST ASSET User can access")
        #     self.user.groups.add(self.group)
        #     self.user.save()
        self.c.login(username='readonly1', password='Password1.')

        response = self.c.get(reverse('assets:host_list'))
        # login = self.client.login(username='admin', password='Password1.')
        # self.assertTrue(login)
        # response = self.c.post('/accounts/login/', {'username': 'test', 'password': 'Password1.'})
        self.assertEqual(response.status_code, 200, u'user should have access')
    #
    # def create_profile(self, username="Username"):
    #     return Profile.objects.create(username=username, created_at=timezone.now())
    #
    # def test_profile_creation(self):
    #     w = self.create_profile()
    #     self.assertTrue(isinstance(w, Profile))
    #     self.assertEqual("Username", w.username)

    # def test_profile_lists_view(self):
        # User = get_user_model()
        # self.client.login(username='temporary', password='Password1.')
        # print(User.objects.all())
        # self.user.user_permissions.add('assets.view_ProfileListView')
        # self.assertTrue(self.user.has_module_perms('assets'))
        # w = self.create_profile()
        # url = reverse("assets.views.profilelistview")
        # url = reverse('assets:prof_list')
        # resp = self.client.get(url)
        # print(resp)
        # self.assertEqual(resp.status_code, 200)
        # self.assertIn(w.title, resp.content)

    # def test_profile_list_view(self):
    #     w = self.create_profile()
    #     url = reverse("assets:prof_list")
    #     resp = self.client.get(url)
    #
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn(w.title, resp.content)

# class MyTestTemplateClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass
#
#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass
#
#     def tearDown(self):
#         print("tearDown: Clean up run after every test method.")
#         pass
#
#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

    # def test_first_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('first_name').max_length
    #     self.assertEquals(max_length, 100)
    #
    # def test_object_name_is_last_name_comma_first_name(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = f'{author.last_name}, {author.first_name}'
    #     self.assertEquals(expected_object_name, str(author))
    #
    # def test_get_absolute_url(self):
    #     author = Author.objects.get(id=1)
    #     This will also fail if the urlconf is not defined.
        # self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
