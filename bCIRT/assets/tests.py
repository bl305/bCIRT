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


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        # create permissions group
        # group_name = "AssetsAll"
        # self.group = Group(name=group_name)
        # self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="Password1.")
        print(self.user)
        self.user.save()
        pass

    def tearDown(self):
        self.user.delete()
        # self.group.delete()

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="bcirt", email='bcirt@bcirt.com', password='AlmaFa1.')
        self.assertEqual(user.email, 'bcirt@bcirt.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
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

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username='admin', email='admin@bcirt.com', password='AlmaFa1.')
        self.assertEqual(admin_user.email, 'admin@bcirt.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
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
        #     self.user.groups.add(self.group)
        #     self.user.save()
        self.c.login(username='admin', password='Almafa1.')
        response = self.c.get(reverse('assets:host_list'))
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
