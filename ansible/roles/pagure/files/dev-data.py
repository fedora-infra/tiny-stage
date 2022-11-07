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

userslist = []

from fasjson_client import Client
c = Client('http://fasjson.tinystage.test/fasjson', principal='admin@TINYSTAGE.TEST')

def insert_data(session):
    _config["EMAIL_SEND"] = False
    _config["TESTING"] = True

    userdata = c.list_users().result
    for user in userdata:
        userslist.append(user['username'])
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

    projects = ["0ad-data", "0install", "0xFFFF", "2048-cli", "2ping", "389-admin", "389-admin-console", "389-adminutil", "389-console", "389-directory-server", "389-ds", "389-ds-base", "389-ds-console", "389-dsgw", "3Depict", "3dprinter-udev-rules", "3mux", "3proxy", "4diac-forte", "4Pane", "4th", "4ti2", "5minute", "64tass", "6tunnel", "7kaa", "8Kingdoms", "8sync", "90-Second-Portraits", "915resolution", "99soft-oss-parent", "9wm", "a2jmidid", "a2ps", "a52dec", "aajohan-comfortaa-fonts", "aalib", "aalto-xml", "aardvark-dns", "aasaver", "abakus", "abattis-cantarell-fonts", "abbayedesmorts-gpl", "abby", "abc", "abcde", "abcm2ps", "abcMIDI", "abduco", "abe", "abgraph", "abicheck", "abi-compliance-checker", "abi-dumper", "abi-tracker", "abiword", "abook", "aboot", "abootimg", "abrt", "abrt-addon-python3", "abrt-java-connector", "abrt-server-info-page", "abseil-cpp", "abuse", "abyssinica-fonts", "academic-admin", "accel-config", "accerciser", "access-modifier-annotation", "accountsdialog", "accounts-qml-module", "accountsservice", "accrete", "accumulo", "acd_cli", "ace", "acegisecurity", "aces_container", "AcetoneISO", "AcetoneISO2", "acheck", "acheck-rules", "ack", "acl", "acme-tiny", "acpi", "acpica-tools", "acpid", "acpitool", "act", "activeio", "activemq", "activemq-cpp", "activemq-protobuf", "adanaxisgpl", "adapt"]
    namespaces = ['rpms', 'containers', 'modules', 'flatpaks']
    for project in projects:
        thisusername = userslist[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % 10 ]
        namespace = namespaces[int.from_bytes(bytes(project,'utf-8'), byteorder='big') % len(namespaces) ]
        u = pagure.lib.query.get_user(
            session, key=thisusername
        )

        p = pagure.lib.model.Project(
            user_id=u.id,
            name=project,
            is_fork=False,
            parent_id=None,
            description=f"{project} {namespace}",
            namespace=namespace,
            hook_token=project
        )
        p.close_status = ["Invalid", "Insufficient data", "Fixed", "Duplicate"]
        try:
            print(f"adding {project} for user {thisusername} in namespace {namespace}")
            session.add(p)
            session.commit()
        except IntegrityError as e:
            print(e)
            print("error")
            session.rollback()


        # group = pagure.lib.query.search_groups(
        #     session, pattern=None, group_name="rel-eng", group_type=None
        # )
        # repo = pagure.lib.query.get_authorized_project(session, "test")
        # item = pagure.lib.model.ProjectGroup(
        #     project_id=repo.id, group_id=group.id, access="commit"
        # )


if __name__ == "__main__":
    session = None
    if not session:
        session = pagure.lib.query.create_session(_config["DB_URL"])

    insert_data(session)
