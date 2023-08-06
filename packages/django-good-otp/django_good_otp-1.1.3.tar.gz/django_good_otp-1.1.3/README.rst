Yet Another Implementation of OTP for Django
============================================

|CI| |CovSt| |GPA|

What This?
----------

This script is "Yet Another Implementation" of 2 factor authentication.

Why I re-invent?
----------------

First, I tried `Django
OTP <https://bitbucket.org/psagers/django-otp>`__, but 2 FA code is
required though it should be optional. Moreover, Admin Panel to edit/fix
secret key is not provided.

Then, I tried
`django-two-factor-auth <https://github.com/Bouke/django-two-factor-auth>`__,
but I found it is the wrapper of `Django
OTP <https://bitbucket.org/psagers/django-otp>`__ that requires 2FA code
to the user who doesn't have 2FA enabled.

How to use
----------

1. Install this script. There's `pip
   package <https://pypi.python.org/pypi/django_good_otp>`__ and you can
   install it by ``pip install django_good_otp``.
2. Create a Django project as usual.
3. Edit settings.py. You will need to edit INSTALLED\_APPS and
   AUTHENTICATION\_BACKENDS. For detail, refer **Edit Settings**
   section.
4. Run migration as usual.
5. Edit ``url.py`` of your root URL config to enable QR Code. For
   details, Check out **URL Routing** section.
6. To enable admin panel, you will need to write very small code. For
   details, Check out **Enable Admin Panel** section.
7. To use 2FA on Admin panel login, you will also need to write very
   simple code. For details, Check out **Enable Admin Panel** section.

Edit settings
-------------

You will need to edit configuration such settings.py. The variable to
edit is ``INSTALLED_APPS`` and ``AUTHENTICATION_BACKENDS``.

INSTALLED\_APPS
~~~~~~~~~~~~~~~

You will just need to add ``'django_otp.DjangoOTP'`` after
``'django.contrib.auth'`` i.e. it should be like this:

``settings.py``

.. code:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "django_otp.DjangoOTP"
    ]

Note that this depends on the case. i.e. If you have more apps
installed/uninstalled, your ``INSTALLED_APPS`` list might be
longer/shorter than this.

AUTHENTICATION\_BACKENDS
~~~~~~~~~~~~~~~~~~~~~~~~

To use 2 FA, you will need to replace authentication backend with the
backend this module provides. i.e. just set ``AUTHENTICATION_BACKENDS``
in ``settings.py`` to ``("django_otp.backends.OTPAuthBackend", )``. i.e.
like this:

``settings.py``

.. code:: python

    AUTHENTICATION_BACKENDS = ("django_otp.backends.OTPAuthBackend", )

URL Routing
-----------

This module supports QRCode to transfer Secret Key to your device. To
use it, you will need to add ``django_otp.urls`` with ``include``
function like this:

``urls.py``

.. code:: python

    from django.conf.urls import url, include
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^qr/', include("django_otp.urls"))
    ]

Enable Admin Panel
------------------

Admin Panel
~~~~~~~~~~~

By default, Admin Panel of the model that stores secret key is
**disabled**. To enable Admin Panel, you will need to call
``OTPAdmin.enable()`` method like this:

``urls.py``

.. code:: python

    from django.conf.urls import url, include
    from django.contrib import admin
    from django_otp.admin import OTPAdmin

    OTPAdmin.enable()

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^qr/', include("django_otp.urls"))
    ]

Using 2FA form on adminsite
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unfortunately, login template of administration site doesn't handle
custom login form. Therefore, to use 2FA-ready admin form, you will need
to replace ``admin.site`` with ``django_otp.admin.AdminSite``. i.e. like
this:

``urls.py``

.. code:: python

    from django.conf.urls import url, include
    from django.contrib import admin

    from django_otp.admin import AdminSite

    OTPAdmin.enable()

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^qr/', include("django_otp.urls"))
    ]

Other stuff
-----------

For other stuff that is not documented here, please refer the `source
code <https://github.com/hiroaki-yamamoto/django-good-otp>`__.

Contribution
------------

The code is on
`Github <https://github.com/hiroaki-yamamoto/django-good-otp>`__ and you
can create issues/PRs. Making issues is appreciated, however, **making
PRs is more appreciated**.

.. |CI| image:: https://travis-ci.org/hiroaki-yamamoto/django-good-otp.svg?branch=master
   :target: https://travis-ci.org/hiroaki-yamamoto/django-good-otp
.. |CovSt| image:: https://coveralls.io/repos/github/hiroaki-yamamoto/django-good-otp/badge.svg?branch=master
   :target: https://coveralls.io/github/hiroaki-yamamoto/django-good-otp?branch=master
.. |GPA| image:: https://codeclimate.com/github/hiroaki-yamamoto/django-good-otp/badges/gpa.svg
   :target: https://codeclimate.com/github/hiroaki-yamamoto/django-good-otp
