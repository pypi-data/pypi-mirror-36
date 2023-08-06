.. _customising-label:

===================
Customising
===================

Edit the template files. I do plan on doing template tags in the :ref:`future <roadmap-label>` for a better experience but this is just how it is for now.

All that you absolutely need is to load the ``wagtail_podcast/css/mediaelementplayer.css`` at the top of the page. You will need to load ``wagtail_podcast/js/jquery.min.js`` before ``wagtail_podcast/js/mediaelement-and-player.min.js`` static files in the ``wagtail_podcast/podcast_page.html`` template.

To actually render the media-player add the following:

.. code-block:: html

     <audio class="mejs__player">
        <source src="{{ page.recording.file.url }}" type="audio/mpeg">
        Your browser cannot play this type of file.
    </audio>

There is plenty of customisation available of both how the player looks and functions, see: `Media Element Player JS docs <https://github.com/mediaelement/mediaelement/tree/master/docs>`_

Do note that you can do a decent bit of customisation with the ``style`` html attribute.