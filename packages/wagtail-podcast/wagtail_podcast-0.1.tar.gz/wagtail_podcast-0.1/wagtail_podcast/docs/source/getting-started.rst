***************************
Getting Started
***************************

Installation
===================

To install run ``pip install wagtail_podcast``

It should automatically install mutagen; however, if it doesn't then you will need to install it manually with: ``pip install mutagen``

Remember to add ``wagtail_podcast`` to your installed apps in settings.py i.e.

    .. code-block:: Python

        INSTALLED_APPS = [
            ...
            'wagtail_podcast',
        ]

Requirements:

    .. code-block:: Python

        python3
        mutagen
        wagtail
        django
        django-social-share

I'm not quite sure how far back this app works; however, it should work going back quite far. It's currently tested on Python3 with Wagtail >2 and Django >2 on openSUSE. It should work on all platforms and shouldn't break anytime soon. Let me know if you have a combo that doesn't work and I'll see what I can do to support it.

*Please see the* :ref:`caveats-label` *below*

Usage
===================================

To use the app just add a Podcast Root Page to your page hierarchy and fill in the details as necessary.

Try use a very high resolution image for the default image as that is the image used for your Podcast on Itunes/Google/etc. I also recommend high resolution images for the podcasts themselves. Don't worry about the high resolution, Itunes will cache it their side, and ``wagtail_podcast`` reduces image sizes when serving for you.

Look at the Podcast Root Page url and append ``podcast/`` to the end. Submit this URL to Itunes/Google/Blubrry. You will then get a podcast page on their platforms. Copy the url of your page to the relevent urls in the podcast root page and then the sidebar widget will be rendered.

To add a podcast just add a child page to the parent page and fill in the details. See :ref:`podcast-options-label` for more information.


Analytics
======================

90% of your users and listeners will consume your podcast through an app. Putting in analytics will create code bloat and probably not be meaningfully useful to you. If you need some analytics I highly recommend using Google Analytics as that will give you a good indication of web listeners, but for apps just use the analytics Google/Itunes/Blubrry provide through their platforms.


Customising
==========================

Honestly I give a really basic thing. No menus, no title bar, just some bootstrap cards, pagination, and a side bar, all of which is responsive. I highly recommend you edit the templates. I do plan on creating template tags at a later stage that should make customising much easier in the future. This is a rough, ugly framework just to get you on your feet. Go nuts! I recommend cheaking out the beautiful themes (based on Bootstrap) made by `Creative Tim <https://www.creative-tim.com/>`_

For more about customising see: :ref:`customising-label`

.. _caveats-label:

Caveats
============

#.  I haven't implemented categories at all so that is rather broken. You need to go into wagtail_podcast/templates/wagtail_podcast/feed.xml
    and change it to something more appropriate

    .. code-block:: XML

        <itunes:category text="{{ page.category }}">
            <itunes:category text="Christianity"/>
        </itunes:category>

#. There is currently no handling of ogg files though I plan on doing auto conversion to them at some point. All major browsers support mp3 these days.

#. This is made only for audio podcasts though I may support video podcasts at a later stage since that doesn't require much changing.

#. Seasons are currently not supported. This is really high on my list, but I haven't figured out a really great way to do it. The page hierarchy is already going to be a bit of a mess.

#. This currently only supports one podcast per wagtail site. It should be relatively easy to make it support multiple; however, I'll only do it if there is demand for the feature.


