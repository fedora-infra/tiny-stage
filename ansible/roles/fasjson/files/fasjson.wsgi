import os
from fasjson.web.app import create_app

os.environ["KRB5CCNAME"] = "/tmp/krb5cc-httpd"
application = create_app()
