#!/usr/bin/env python3
from faker import Faker

import python_freeipa

USER_PASSWORD = "testuserpw"

fake = Faker()
fake.seed_instance(0)

ipa = python_freeipa.ClientLegacy(
    host="ipa.example.test", verify_ssl="/etc/ipa/ca.crt"
)
ipa.login("admin", "adminPassw0rd!")


# create a developers fasgroup
try:
    ipa.group_add("developers", "A group for developers", fasgroup=True)
except python_freeipa.exceptions.FreeIPAError as e:
    print(e)

# create a designers fasgroup
try:
    ipa.group_add("designers", "A group for designers", fasgroup=True)
except python_freeipa.exceptions.FreeIPAError as e:
    print(e)

for x in range(50):
    firstName = fake.first_name()
    lastName = fake.last_name()
    username = firstName + lastName
    fullname = firstName + " " + lastName
    print(f"adding user {fullname}")
    try:
        ipa.user_add(
            username,
            firstName,
            lastName,
            fullname,
            fasircnick=[username, username + "_"],
            faslocale="en-US",
            fastimezone="Australia/Brisbane",
            fasstatusnote="active",
            fasgpgkeyid=[],
        )
        if x % 3 == 0:
            ipa.group_add_member("developers", username)
            if x < 10:
                ipa._request(
                    "group_add_member_manager",
                    "developers",
                    {"user": username},
                )
        if x % 5 == 0:
            ipa.group_add_member("designers", username)
            if x <= 15:
                ipa._request(
                    "group_add_member_manager",
                    "designers",
                    {"user": username},
                )

    except python_freeipa.exceptions.FreeIPAError as e:
        print(e)
