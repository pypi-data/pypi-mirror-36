Introduction
===========================================

This is a very basic podcast app that integrates with Wagtail. It allows a person to upload a mp3 and then play it on the website. It generates a rss/xml feed that you can submit to Itunes, Google and/or Blubrry.

This app is simple, and not feature rich. It does the basics and thats it. I will probably add more features and options to it as time permits, but only if requests are made.

It is also not production ready as there are **no tests currently written** for it. I did put this up on a site and they have been using it extensively and haven't had any reported issues. That said, *apps without tests should always be treated sceptically.*

I hope to write tests in a month or so when I get a bit of free time. I also hope to add a bunch of features in the near future.

Please report any errors you encounter. I will try resolve them quickly and then add tests for them. Please visit: `wagtail_podcast <https://gitlab.com/dfmeyer/wagtail_podcast>`_ .  Documentation is at readthedocs.io: `wagtail_podcast documentation <https://wagtail-podcast.readthedocs.io/en/latest/>`_

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