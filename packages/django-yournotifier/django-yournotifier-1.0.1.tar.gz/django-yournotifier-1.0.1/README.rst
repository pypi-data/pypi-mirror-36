=====
Yournotifier
=====

Quick start
-----------

1. Install

    pip install django-yournotifier

2. Use

Create account at `YourNotifier <https://yournotifier.com>`_

Add in `settings.py`:

    NOTIFIER_APIKEY = '...'

Use:

    from yournotifier import send_notify

    send_notify(
        channel_name='name',
        text='Text message...'
    )
