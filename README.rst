meapi: Unofficial api for 'Me - Caller ID & Spam Blocker'
#########################################################

.. image:: https://img.shields.io/pypi/dm/meapi?style=flat-square
    :alt: PyPI Downloads
    :target: https://pypi.org/project/meapi/


.. image:: https://www.codefactor.io/repository/github/david-lev/meapi/badge/main
   :target: https://www.codefactor.io/repository/github/david-lev/meapi/overview/main
   :alt: CodeFactor


**This README is not finished and still in the middle of writing.**
_________________________________________________________________

meapi is a Python3 library to identify phone numbers, report spam, get socials and more.

.. features

Features
--------
| **Searching**:

* Search phone numbers
* Get user full profile
* Know if is spammer

| **Social**:

* Get and manage user comments
* Get notificatioms


Usage
------
.. code-block:: python

    from meapi import Me

    me = Me(phone_nuber=972123456789)
    search_res = me.search_phone('+865-456-234-12'))
    if search_res:
        print(search_res['contact']['name'])

    if search_res['contact'].get('user'):
        uuid = search_res['contact']['user']['uuid']
        print(me.get_profile_info(uuid))

    for comment in me.get_comments(uuid)['comments']:
        print(f"Comment: '{comment['message']}' by '{comment['author']['first_name']}'.)

    print(me.who_watched())
    print(me.who_deleted())
    print(me.get_notifications())

.. end-features

Requirements
==============

- Python 3.6 or higher - https://www.python.org

Setup and Usage
===============

See the `Documentation <https://meapi.readthedocs.io/>`_ for detailed instructions

Contributing
==============

Pull requests are welcome. There are still some features that are not yet implemented.

Disclaimer
==============
This application is intended for educational purposes only. Any use in professional manner or to harm anyone or any organization doesn't relate to me and can be considered as illegal.