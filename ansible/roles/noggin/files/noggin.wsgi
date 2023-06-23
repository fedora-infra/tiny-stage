import os
from noggin.app import create_app

os.environ["KRB5CCNAME"] = "/tmp/krb5cc-httpd"
os.environ["GSS_USE_PROXY"] = "yes"
os.environ["NOGGIN_CONFIG_PATH"] = "/etc/noggin.cfg"
application = create_app()
