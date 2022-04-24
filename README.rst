.. image:: https://user-images.githubusercontent.com/42866208/164977163-2837836d-15bd-4a75-88fd-4e3fe2fd5dae.png
  :width: 95
  :alt: Alternative text

`meapi <https://github.com/david-lev/meapi>`_: Unofficial api for 'Me - Caller ID & Spam Blocker'
##################################################################################################

.. image:: https://img.shields.io/pypi/dm/meapi?style=flat-square
    :alt: PyPI Downloads
    :target: https://pypi.org/project/meapi/

.. image:: https://www.codefactor.io/repository/github/david-lev/meapi/badge/main
   :target: https://www.codefactor.io/repository/github/david-lev/meapi/overview/main
   :alt: CodeFactor

.. image:: https://readthedocs.org/projects/meapi/badge/?version=latest&style=flat-square
   :target: https://meapi.readthedocs.io
   :alt: Docs

.. image:: https://badges.aleen42.com/src/telegram.svg
   :target: https://t.me/me_api
   :alt: Telegram

________________________

☎️ meapi is a Python3 library to identify, discover and get information about phone numbers, indicate and report spam, get and manage socials, profile management and much more.

🔐 To **get started**, read the `Authentication guide <https://meapi.readthedocs.io/en/latest/setup.html>`_.

📖 For a **complete documentation** of available functions, see the `Reference <https://meapi.readthedocs.io/en/latest/reference.html>`_.

>>️ *For more information about Me® -* `Click here <https://meapp.co.il/>`_.


🎛 Installation
--------------
.. installation

- **Install using pip3:**

.. code-block:: bash

    pip3 install -U meapi

- **Install from source:**

.. code-block:: bash

    git clone https://github.com/david-lev/meapi.git
    cd meapi && python3 setup.py install

.. end-installation

🎉 **Features**
---------------

🔎 Searching:
^^^^^^^^^^^^^

* Search phone numbers
* Get user full profile: profile picture, birthday, location, platform, socials and more
* Spam indication and report

🌐 Social:
^^^^^^^^^^

* Get user social networks: facebook, instagram, twitter, spotify and more
* See how people call you
* Get mutual contacts
* See who watched your profile
* See who deleted you from his contacts book
* Get, publish and manage comments
* Report spam on phone numbers
* Read app notifications

⚙️ Settings:
^^^^^^^^^^^^^

* Change profile information
* Connect social networks (And get verified blue check)
* Upload contacts and calls history
* Block profiles and numbers
* Update your location
* Delete or suspend your account


👨‍💻 **Usage**
----------------
.. code-block:: python

    from meapi import Me

    me = Me(phone_nuber=972123456789)
    # If you have official access token:
    # me = Me(access_token='XXXXXXXX')

    search_res = me.search_phone('+865-456-234-12'))
    if search_res:
        print(search_res['contact']['name'])

    if search_res['contact'].get('user'):
        uuid = search_res['contact']['user']['uuid']
        print(me.get_profile_info(uuid))

📚 For more usage examples, read the `Examples <https://meapi.readthedocs.io/en/latest/examples.html>`_ page.

💾 **Requirements**
--------------------

- Python 3.6 or higher - https://www.python.org

📖 **Setup and Usage**
-----------------------

See the `Documentation <https://meapi.readthedocs.io/>`_ for detailed instructions

⛔ **Disclaimer**
------------------

**This application is intended for educational purposes only. Any use in professional manner or to harm anyone or any organization doesn't relate to me and can be considered as illegal.
Me name, its variations and the logo are registered trademarks of NFO LTD. I have nothing to do with the registered trademark.**

🏆 **Credits**
---------------

- `Magisk <https://github.com/topjohnwu/Magisk/>`_ for device rooting.
- `LSPosed <https://github.com/LSPosed/LSPosed>`_ for xposed framework.
- `TrustMeAlready <https://github.com/ViRb3/TrustMeAlready>`_ to disable SSL verification.
- `mitmproxy <https://github.com/mitmproxy/mitmproxy>`_ to monitor the app network requests.
- `ytmusicapi <https://github.com/sigma67/ytmusicapi/>`_ for the structure of this project.
- `readthedocs <https://github.com/readthedocs/readthedocs.org>`_ for hosting the docs.
