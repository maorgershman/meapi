Examples
--------

- Initialize me client:

.. code-block:: python

    me = Me(phone_number='+972123456789')

- Get all the numbers that kept you in their contacts, but you did not keep them:

.. code-block:: python

    contacts_numbers_and_names = {}
    for contact in me.get_unsaved_contacts():
        full_name = str(contact['user']['first_name'])
        if contact['user']['last_name']:
            full_name += (" " + contact['user']['last_name'])
        contacts_numbers_and_names[str(contact['user']['phone_number'])] = full_name
    print(contacts_numbers_and_names)
    # >> {'9721234567890': 'Mike Hannigan', '9720987654321': 'Regina Phalange'...}

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
        # Do what you have to do, now the users you are viewing their profiles will not receive the notification you have viewed on their profile..
        user_profile = me.get_profile_info(uuid="xxxxx-xxxxx-xxxx-xxxx")
        who_watched = me.who_watched()
        who_deleted = me.who_deleted()
    if me.change_social_settings(who_deleted_enabled=False, who_watched_enabled=False):
        print("Success!")

- Provide txt file with numbers and get csv file with data:

.. code-block:: python

    phone_prefix = ""  # if the phones without prefix, replace this with your prefix_phone country (972 etc.)
    with open("phone_numbers.txt", "r") as phones_file:
        phones = phones_file.read()

    header = "first_name,last_name,county,phone,email,gender,bio,profile_picture_url,date_of_birth,device_type,suggested_as_spam\n"

    phones_info = []
    counter = 0
    phones = phones.split("\n")
    if not phones:
        raise Exception("No phones found!")
    for phone in phones:
        counter += 1
        print(f"{counter} out of {len(phones)}")
        if len(phones_info) / 10 == 0:  # every 10 founds
            print(f"** {len(phones_info)} out of {len(phones)} found so far.")
        try:
            phone = str(phone_prefix) + str(me.valid_phone_number(phone))
        except:
            print("Not a valid phone number! " + phone)
        first_name, last_name, county, phone_number, email, gender, bio, profile_picture_url, date_of_birth, device_type, suggested_as_spam = ("\"\"",) * 11
        results = me.phone_search(phone)
        if results:
            first_name = results['contact']['name']
            suggested_as_spam = results['contact']['suggested_as_spam']
            if results['contact']['user']:
                extra_info = me.get_profile_info(results['contact']['user']['uuid'])

                # start to associate the info
                first_name = results['contact']['user']['first_name'].replace(",", ".")
                last_name = results['contact']['user']['last_name'].replace(",", ".") or "\"\""
                county = extra_info['profile']['country_code'] or "\"\""
                phone_number = results['contact']['user']['phone_number'] or "\"\""
                email = results['contact']['user']['email'].replace(",", ".") or "\"\""
                gender = extra_info['profile']['gender'] or "\"\""
                bio = extra_info['profile']['slogan'].replace(",", ".") or "\"\""
                profile_picture_url = extra_info['profile']['profile_picture'] or "\"\""
                date_of_birth = extra_info['profile']['date_of_birth'] or "\"\""
                device_type = extra_info['profile']['device_type'] or "\"\""
            print(f"** Found results for {phone_number}! {first_name} {last_name}.", first_name)
            phones_info.append([str(i) for i in [first_name, last_name, county, phone_number, email, gender, bio, profile_picture_url, date_of_birth, device_type, suggested_as_spam]])

    if phones_info:
        with open('contacts.csv', 'w') as contacts_file:
            contacts_file.write(header)
            contacts_file.write("\n".join([",".join(phone) for phone in phones_info]))

More examples soon...
^^^^^^^^^^^^^^^^^^^^^