Setup
=====

Installation
------------
.. include:: ../../README.rst
  :start-after: installation
  :end-before: end-installation


Authentication
--------------

Unofficial method
^^^^^^^^^^^^^^^^^
**important notes:**

    - **This method is for educational purposes only and its use is at your own risk.** See `disclaimer <https://meapi.readthedocs.io/en/latest/index.html#disclaimer>`_
    - In this method you are going to verify as a user of the app and get a token with access to all the actions that the app provides.
    - After verification, if you are connected to another device, you will be disconnected automatically.
    - For app users there is an Rate-limit of about ``350`` searches per day.

**Verification:**

- Run this code:

.. code-block:: python

    from meapi import Me
    me = Me(phone_number=1234567890) # Enter your phone number

- If you have not verified this number before, you will see the following prompt in the terminal:

::

    To get access token you need to authorize yourself:
    * WhatsApp (Recommended): https://wa.me/972543229534?text=Connectme
    * Telegram: http://t.me/Meofficialbot?start=__iw__XXXXXXXXXX // Your phone number instead of the 'XXXXX'

    ** Enter your verification code (6 digits):

- Go into `WhatsApp <https://wa.me/972543229534?text=Connectme>`_ (+972543229534) and send any message to this number.
- You can also verify by Me Telegram bot (Only if you have Telegram account on this number!) and get verification code of 6 digits.
- Enter the code in the terminal and you will see if the verification was successful.

::

    ** Enter your verification code (6 digits): 123456 // Enter

    ** Trying to authorize...
    Verification completed.

- If this is a new number that is not already open an account, you will be required to fill in some details like name and email in order to create an account.
- If you keep getting ``404`` error, you may want to run the `upload_random_data() <https://meapi.readthedocs.io/en/latest/reference.html#meapi.Me.upload_random_data>`_ function, in order to activate the account.

**Credentials:**

- If no path to the config file is provided, the config file will be created in the location from which the library was called.
- The config file ``config.json`` format is:

.. literalinclude:: ../../config.json.example
  :language: JSON

- You can copy/move this file between projects. Just specify the path to the config file when you initialize the Me class:

.. code-block:: python

    from meapi import Me
    me = Me(phone_number=123456789, config_file="/home/david/credentials/config.json")

Official method
^^^^^^^^^^^^^^^

- You can also use the official verification and verify directly with an access token.
    Me has an official API which can be accessed by submitting a formal request at `this <https://meapp.co.il/api/>`_. link (Probably paid).
    I guess you get a API KEY with which you can get an access token similar to the app.
    But I do not know what the scope of this token are and whether it is possible to contact with it the same endpoints that the official app addresses.
- If anyone can shed light on the official authentication method, I would be happy if he would `contact me <https://t.me/davidlev>`_. so that I could better support it and exclude or add certain functions.
- If you have an access token and you are interested in connecting with it - do the following:

.. code-block:: python

    from meapi import Me
    me = Me(access_token='XXXXXXXXXX') # Enter your access token

