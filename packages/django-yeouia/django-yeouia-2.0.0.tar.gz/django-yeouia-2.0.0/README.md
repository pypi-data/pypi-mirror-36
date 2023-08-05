# Yummy Email Or Username Insensitive Auth model backend for Django

[![Build Status](https://travis-ci.org/nim65s/django-YummyEmailOrUsernameInsensitiveAuth.svg?branch=master)](https://travis-ci.org/nim65s/django-YummyEmailOrUsernameInsensitiveAuth)
[![Coverage Status](https://coveralls.io/repos/github/nim65s/django-EmailOrUsernameAuth/badge.svg?branch=master)](https://coveralls.io/github/nim65s/django-EmailOrUsernameAuth?branch=master)

## Instructions

* `pip install django-yeouia`
* Add `AUTHENTICATION_BACKENDS = ['yeouia.backends.YummyEmailOrUsernameInsensitiveAuth']` to your `settings.py`
* Enjoy

## Requirements

Tested for

* Python 3.4, 3.5, 3.6, 3.7
* Django 2.0, 2.1

May work otherwise, but you should run tests :P

## Case Insensitive ?

Django's default auth username is *not* case insensitive.
(See [#2273](https://code.djangoproject.com/ticket/2273) and [#25617](https://code.djangoproject.com/ticket/25617))

But… Who cares ?

This backend tries:

1. username, case sensitive
2. username, case insensitive
3. email, case insensitive

And follows [#20760](https://code.djangoproject.com/ticket/20760).
