from ipsilon.info.common import InfoProviderBase, InfoProviderInstaller
from ipsilon.util.plugin import PluginObject
from ipsilon.util.policy import Policy
from ipsilon.util import config as pconfig

import fasjson_client


fasjson_mapping = [
    ['email', 'email'],
    ['username', 'username'],
    ['timezone', 'timezone'],
    ['locale', 'locale'],
    ['human_name', 'human_name'],
    ['groups', 'groups'],
]


class InfoProvider(InfoProviderBase):

    def __init__(self, *args):
        super(InfoProvider, self).__init__(*args)
        self.mapper = Policy(fasjson_mapping)

        self.name = 'fasjson'
        self.description = """
Info plugin that retrieves user data from FASJSON. """

        self.new_config(
            self.name,
            pconfig.String(
                'FASJSON url',
                'The FASJSON Url.',
                'http://fasjson.tinystage.test/fasjson/'),
        )

    @property
    def fasjson_url(self):
        return self.get_config_value('FASJSON url')


    def get_user_attrs(self, user):
        user_data = None
        user_group_data = None
        try:
            client = fasjson_client.Client(url=self.fasjson_url)
            user_data = client.get_user(username=user).result
            user_group_data = client.list_user_groups(username=user).result
        except Exception as e:
            self.error(f'FASJSON error: {e}')


        if not user_data:
            user_data =  {"username": "ryancarr", "surname": "Carr", "givenname": "Ryan", "human_name": "Ryan Carr", "emails": ["ryancarr@tinystage.test"], "ircnicks": ["RyanCarr", "RyanCarr_"], "locale":
 "en-US", "timezone": "Australia/Brisbane", "gpgkeyids": None, "certificates": None, "creation": None, "locked": False, "uri": "http://fasjson.tinystage.test/fasjson/v1/users/ryancarr/"}

        if not user_group_data:
            user_group_data = [{'groupname': 'developers', 'uri': 'http://fasjson.tinystage.test/fasjson/v1/groups/developers/'}, {'groupname': 'designers', 'uri': 'http://fasjson.tinystage.test/fasjson/v1/groups/designers/'}]

        # assumption that first email is the default
        user_data['email'] = user_data['emails'][0]

        # add the groups to the user_data
        user_data['groups'] = [ g['groupname'] for g in user_group_data]


        userattrs, extras = self.mapper.map_attributes(user_data)
        self.debug(f'user_data: {user_data}')
        self.debug(f'Userattrs: {userattrs}')

        return userattrs


class Installer(InfoProviderInstaller):

    def __init__(self, *pargs):
        super(Installer, self).__init__()
        self.name = 'fasjson'
        self.pargs = pargs

    def install_args(self, group):
        group.add_argument('--info-fasjson', choices=['yes', 'no'], default='no',
                           help='Configure FAS info')

    def configure(self, opts, changes):
        if opts['info_fasjson'] != 'yes':
            return

        # Add configuration data to database
        po = PluginObject(*self.pargs)
        po.name = 'fasjson'
        po.wipe_data()
        po.wipe_config_values()

        # Update global config to add login plugin
        po.is_enabled = True
        po.save_enabled_state()
