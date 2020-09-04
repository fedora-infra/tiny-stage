#!/usr/bin/python3

import re
import sys


IPA_ADMIN_USER = "{{ ipa_admin_user }}"
IPA_ADMIN_PASSWORD = "{{ ipa_admin_password }}"
IPA_INSTANCE = "ipa.{{ ansible_domain }}"

block_re = re.compile(r"^\s*\[(?P<id>.+)\]\s*$")
key_val_re = re.compile(r"^\s*(?P<key>\S+)\s*=\s*(?P<value>\S(?:.*\S)?)\s*$")

in_block = None

for line in sys.stdin:
    line = line.rstrip("\n")
    m = block_re.match(line)
    if m:
        in_block = m.group("id")

    m = key_val_re.match(line)
    if m:
        key = m.group("key")
        value = m.group("value")

        if in_block == "ipa":
            if key == "instances":
                print(f'{key} = ["{IPA_INSTANCE}"]')
                continue
            elif key == "username":
                print(f'{key} = "{IPA_ADMIN_USER}"')
                continue
            elif key == "password":
                print(f'{key} = "{IPA_ADMIN_PASSWORD}"')
                continue

    print(line)
