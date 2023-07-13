import os
from fasjson.web.app import create_app

os.environ["KRB5CCNAME"] = "/tmp/krb5cc-httpd"
os.environ["GSS_USE_PROXY"] = "yes"
os.environ["FASJSON_CONFIG_PATH"] = "/etc/fasjson.cfg"
application = create_app()
