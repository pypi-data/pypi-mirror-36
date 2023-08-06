=====
Django Classic User Accounts
=====


Detailed documentation is in the "docs" directory.

Quick 
-----------

1. Add "ClassicUserAccounts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ClassicUserAccounts',
    ]

2. `AUTH_USER_MODEL = 'ClassicUserAccounts.User'` add this line in your project settings.py file.

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage user profile (you'll need the Admin app enabled).
