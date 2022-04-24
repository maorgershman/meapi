.. image:: https://user-images.githubusercontent.com/42866208/164971421-c1f96d70-5cd8-4142-ae8d-16a7af11635b.png
  :width: 95
  :alt: Alternative text

meapi: Unofficial api for 'Me - Caller ID & Spam Blocker'
#########################################################

.. image:: https://img.shields.io/pypi/dm/meapi?style=flat-square
    :alt: PyPI Downloads
    :target: https://pypi.org/project/meapi/


.. image:: https://www.codefactor.io/repository/github/david-lev/meapi/badge/main
   :target: https://www.codefactor.io/repository/github/david-lev/meapi/overview/main
   :alt: CodeFactor


**This README is not finished and still in the middle of writing.**
___________________________________________________________________

📞 meapi is a Python3 library to identify and get information about phone numbers, indicate and report spam, get socials and more.

🔐 To **get started**, read the `Authentication instructions <https://meapi.readthedocs.io/en/latest/setup.html>`_.

📖 For a **complete documentation** of available functions, see the `Reference <https://meapi.readthedocs.io/en/latest/reference.html>`_.

Installation:
-------------

Install using pip:
^^^^^^^^^^^^^^^^^
.. code-block:: bash

    pip3 install meapi

Install from source:
^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    git clone https://github.com/david-lev/meapi.git
    cd meapi && python3 setup.py install


Features 🎉
----------
| **Searching:**

* Search phone numbers
* Get user full profile: pictures, birthdays, locations, socials and more
* Spam indication
* ...

| **Social:**

* How people call me
* Get and manage user comments
* See who watched your profile
* See who deleted you from his contacts book
* Get notifications
* ...


Usage 👨‍💻
----------
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


Requirements 💾
---------------

- Python 3.6 or higher - https://www.python.org

Setup and Usage 📖
------------------

See the `Documentation <https://meapi.readthedocs.io/>`_ for detailed instructions

Contributing 🙏
---------------

Pull requests are welcome. There are still some features that are not yet implemented.

Disclaimer ⛔️
------------
This application is intended for educational purposes only. Any use in professional manner or to harm anyone or any organization doesn't relate to me and can be considered as illegal.
