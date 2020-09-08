from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'fedora-account'
    display_name = 'Fedora Account Information'
    scopes = {
        'https://id.fedoraproject.org/scope/groups': {
            'display_name': 'Fedora Account Group Memberships',
            'claims': ['groups']
        },
        'https://id.fedoraproject.org/scope/agreements': {
            'display_name': 'Fedora Account Signed Agreements',
            'claims': ['agreements']
        },
    }
