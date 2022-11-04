#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Populate the pagure db with some dev data. """

from __future__ import print_function, unicode_literals, absolute_import

import pagure
import pagure.lib.model
import pagure.lib.query
from pagure.lib.login import generate_hashed_value

from sqlalchemy.exc import IntegrityError

_config = pagure.config.reload_config()


# userdata = [
#     { "username":"aaronhale", "fullname": "Aaron Hale", "email": "aaronhale@tinystage.test", "groups":["designers", "developers"]},
#     { "username":"alexandraclark", "fullname": "Alexandra Clark", "email": "alexandraclark@tinystage.test", "groups":["developers"]},

# ]

from fasjson_client import Client
c = Client('http://fasjson.tinystage.test/fasjson', principal='admin@TINYSTAGE.TEST')

def insert_data(session):
    _config["EMAIL_SEND"] = False
    _config["TESTING"] = True

    userdata = c.list_users().result
    for user in userdata:
        u = pagure.lib.model.User(
            user=user['username'],
            fullname=user['human_name'],
            password=generate_hashed_value("password"),
            token=None,
            default_email=user['emails'][0],
        )
        
        try:
            print(f"adding user {user['username']}")
            session.add(u)
            session.commit()
        except IntegrityError:
            session.rollback()
    
    grouplist = c.list_groups().result

    for group in grouplist:
        g = pagure.lib.model.PagureGroup(
            group_name=group['groupname'],
            group_type="user",
            user_id=1,
            display_name=group['groupname'],
            description=group['description'],
        )
        try:
            print(f"adding group {group['groupname']}")
            session.add(g)
            session.commit()
        except IntegrityError:
            session.rollback()

        members = c.list_group_members(groupname=group['groupname']).result

        for member in members:
            g = pagure.lib.query.search_groups(
                session, pattern=None, group_name=group['groupname'], group_type=None
            )
            u = pagure.lib.query.get_user(
                session, key=member['username']
            )
            
            try:
                print(f"adding user {member['username']} to group {group['groupname']}")
                session.add(pagure.lib.model.PagureUserGroup(user_id=u.id, group_id=g.id))
                session.commit()
            except IntegrityError:
                session.rollback()
            


if __name__ == "__main__":
    session = None
    if not session:
        session = pagure.lib.query.create_session(_config["DB_URL"])

    insert_data(session)
