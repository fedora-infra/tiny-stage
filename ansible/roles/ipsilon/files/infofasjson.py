from ipsilon.info.common import InfoProviderBase, InfoProviderInstaller
from ipsilon.util.plugin import PluginObject
from ipsilon.util.policy import Policy
from ipsilon.util import config as pconfig

import fasjson_client


class InfoProvider(InfoProviderBase):
    def __init__(self, *args):
        super(InfoProvider, self).__init__(*args)
        self.name = "fasjson"
        self.description = """
Info plugin that retrieves user data from FASJSON. """

        self.new_config(
            self.name,
            pconfig.String(
                "FASJSON url",
                "The FASJSON Url.",
                "http://fasjson.tinystage.test/fasjson/",
            ),
        )

    @property
    def fasjson_url(self):
        return self.get_config_value("FASJSON url")

    def get_user_attrs(self, user):
        data = {
            "email": "test@test.test",
            "fasAgreements": ["FCPA", "Pants"],
            "fasGroups": ["developerz", "designerz"],
            "email": "test@test.test",
        }
        # self.error(f'pants:{userattrs}')
        # self.error(f'pants:{extras}')
        return data

        # client = fasjson_client.Client(url=self.fasjson_url)

        # try:
        #     data = client.get_user(username=user).result
        # except Exception as ex:  # pylint: disable=broad-except
        #     self.error('Unable to retrieve info for %s: %s' % (user, ex))
        #     self.debug('URL: %s' % self.fasjson_url)
        #     return {}
        # if not data:
        #     return {}

        # self.error(f'{data}')
        # raise Exception(data)
        # return fas_make_userdata(data)


class Installer(InfoProviderInstaller):
    def __init__(self, *pargs):
        super(Installer, self).__init__()
        self.name = "fasjson"
        self.pargs = pargs

    def install_args(self, group):
        group.add_argument(
            "--info-fasjson",
            choices=["yes", "no"],
            default="no",
            help="Configure FAS info",
        )

    def configure(self, opts, changes):
        if opts["info_fasjson"] != "yes":
            return

        # Add configuration data to database
        po = PluginObject(*self.pargs)
        po.name = "fasjson"
        po.wipe_data()
        po.wipe_config_values()

        # config = dict()
        # if 'info_fasjson_url' in opts:
        #     config['FASJSON URL'] = opts['info_fasjson_url']
        # po.save_plugin_config(config)

        # Update global config to add login plugin
        po.is_enabled = True
        po.save_enabled_state()
