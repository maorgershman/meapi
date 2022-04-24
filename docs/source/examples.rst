Examples
--------

- Initialize me client:

.. code-block:: python

    me = Me(phone_number='+972123456789')

- Give like all my approved comments:

.. code-block:: python

    for comment in me.get_comments()['comments']:
        if comment['status'] == 'approved' and not comment['is_liked']:
            if me.like_comment(comment['id']):
                print(f"Sending like on comment '{comment['message']}' writing by'{comment['author']['first_name']}'.")

- Send clarification comment to every contact that deleted you from his contacts book:

.. code-block:: python

    for deleter in me.who_deleted():
        comment_txt = f"Hi {deleter['user']['first_name']}, Why did you delete me from your contacts?"
        comment_id = me.publish_comment(uuid=deleter['user']['uuid'], comment=comment_txt)
        if comment_id:
            print(f"A clarification comment was sent to the deleter {deleter['user']['first_name']}. comment_id: {comment_id}")

- get all birthdays:

.. code-block:: python

    for notification in me.get_notifications(birthday_filter=True):
        print(f"Your friend {notification['context']['name']} is {me.get_age(notification['context']['uuid'])} years old.")


- Upload contacts from csv:

.. code-block:: python

    from re import sub

    with open("contacts.csv", "r") as contacts_file:
        content = contacts_file.read()
    contacts = [line.split(",") for line in content.split("\n")][1:]
    contacts_to_upload = []
    for cont in contacts:
        first_name, last_name, phone_number = cont
        contacts_to_upload.append({
                "country_code": "XX",
                "date_of_birth": None,
                "name": f"{first_name} {last_name}",
                "phone_number": int(sub(r'[\D]', '', phone_number))
        })
        me.add_contacts(contacts_to_upload)

- Change who_deleted & who_watched settings temporary to get this data:

.. code-block:: python

    if me.change_social_settings(who_deleted_enabled=True, who_watched_enabled=True):
        who_watched = me.who_watched()
        who_deleted = me.who_deleted()
    if me.change_social_settings(who_deleted_enabled=True, who_watched_enabled=True):
        print("Success!")

More examples soon...
^^^^^^^^^^^^^^^^^^^^^