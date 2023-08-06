**************************
Internationalisation
**************************

Languages
=============

Currently only these languages are fully supported:

    #. English (Daniel F. Meyer)
    #. Afrikaans (Daniel F. Meyer)


It would be super awesome if you translate it to your locale language and make a pull request so that everybody can enjoy your translations. You'll also get credit on this page.

To translate the app is super easy thanks to gettext and Django's builtin stuff. This will translate the user interface and admin interface.

.. code-block:: shell

    $ cd wagtail_podcast
    $ django-admin makemessages -l <your_locale>


Open the ``wagtail_podcast/locale/<your_locale>LC_MESSAGES/django.po`` file in your favourite text editor. Provide your translations and then run ``django-admin compilemessages``. The translations should now automatically activate on server restart.

The language will default to what is set in ``settings.py`` ;however, if a specific Wagtail user changes it then it will be what they set as their language or what langauge you serve the page in to the client. See the Django and Wagtail internationalisation documentation on this.

Caveats
=================

#. You will need to manually add your language locale to the PodcastParentPage model and then ``manage.py makemigrations`` and ``manage.py migrate`` and then restart your server. If you don't do this the dropdown won't be available on the admin page and iTunes and other services will have discoverability issues.

#. I have not internationalised the urls yet; however, its not important as there is no url route that has anything except /<YYYY>/<MM> routing in it which is nice. This will need to be done when adding seasons.