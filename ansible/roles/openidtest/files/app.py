# An simple demonstration application to use Fedora OpenID
# authentication system
# setup a client secrets file by doing
#
# pip3 install oidc-register
# oidc-register https://iddev.fedorainfracloud.org/openidc/ http://localhost:5000
#
# Then run the application, (save it as app.py)
# flask run
#
# then open your browser at http://localhost:5000

#imports for Flask
import flask
#from fedora.client import AuthError, AppError
from flask_oidc import OpenIDConnect
import munch

# Set up Flask application
app = flask.Flask(__name__)
# Application configuration (add secret key of your choice)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["SECRET_KEY"] = "secretkey"

# Set up FAS extension
OIDC = OpenIDConnect(app, credentials_store=flask.session)

@app.before_request
def before_request():
    """Set the flask session as permanent."""
    flask.session.permanent = True
    # Check if already logged in
    if OIDC.user_loggedin:
        if not hasattr(flask.session, 'fas_user') or not flask.session.fas_user:
            flask.session.fas_user = munch.Munch({
                'username': OIDC.user_getfield('nickname'),
                'email': OIDC.user_getfield('email') or '',
                'cla_done':
                  'http://admin.fedoraproject.org/accounts/cla/done'
                  in (OIDC.user_getfield('cla') or []),
                  })
        flask.g.user = flask.session.fas_user
    else:
        flask.g.fas_user = None
        flask.session.fas_user = None

@app.route("/logged_in")
@OIDC.require_login
def logged_in():
    return flask.Response("You are now logged in. Try to logout by going to http://localhost:5000/logout")

@app.route("/")
def landing_page():
    return flask.Response("Landing page, try to go to http://localhost:5000/login")

@app.route("/login")
def login():
    return flask.redirect(flask.url_for('.logged_in'))

@app.route("/logout")
def logout():
    if hasattr(flask.g, 'fas_user') and flask.g.fas_user is not None:
        OIDC.logout()
        flask.g.fas_user = None
        flask.session.fas_user = None
        flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('.landing_page'))
