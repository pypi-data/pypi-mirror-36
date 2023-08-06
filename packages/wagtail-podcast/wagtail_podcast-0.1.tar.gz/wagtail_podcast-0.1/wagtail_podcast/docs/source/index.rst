Welcome to Wagtail Podcast's documentation!
===========================================

This is a very basic podcast app that integrates with Wagtail. It allows a person to upload a mp3 and then play it on the website. It generates a rss/xml feed that you can submit to Itunes, Google and/or Blubrry.

This app is simple, and not feature rich. It does the basics and thats it. I will probably add more features and options to it as time permits, but only if requests are made.

It is also not production ready as there are **no tests currently written** for it. I did put this up on a site and they have been using it extensively and haven't had any reported issues. That said, *apps without tests should always be treated sceptically.*

I hope to write tests in a month or so when I get a bit of free time. I also hope to add a bunch of features in the near future. See: :ref:`roadmap-label`

Please report any errors you encounter. I will try resolve them quickly and then add tests for them as things come up so it doesn't reoccur. Please visit `wagtail_podcast git <https://gitlab.com/dfmeyer/wagtail_podcast>`_ to make pull requests or log issues etc. Documentation is at readthedocs.io: `wagtail_podcast documentation <https://wagtail-podcast.readthedocs.io/en/latest/>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   podcast-options
   customising
   internationalisation
   api
   roadmap
   changelog


Thanks
====================

This app wouldn't be possible without the following great projects and people:

   #. `Wagtail CMS <https://wagtail.io/>`_
   #. `Django Web Framework   <https://www.djangoproject.com/>`_
   #. `Mutagen <https://github.com/quodlibet/mutagen>`_
   #. `Media Element JS <http://www.mediaelementjs.com/>`_
   #. `Bootstrap <http://getbootstrap.com/>`_
   #. `Django Social Share <https://github.com/fcurella/django-social-share>`_
   #. `Font Awesome <https://fontawesome.com/>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
