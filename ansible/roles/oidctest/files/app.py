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
app.config["OIDC_SCOPES"] = ['openid', 'email', 'profile', 'https://id.fedoraproject.org/scope/groups', 'https://id.fedoraproject.org/scope/agreements']
# Set up FAS extension
OIDC = OpenIDConnect(app, credentials_store=flask.session)

@app.before_request
def before_request():
    """Set the flask session as permanent."""
    flask.session.permanent = True

@app.route("/logged_in")
@OIDC.require_login
def logged_in():

    return flask.Response(f"You are now logged in. Try to logout by going to http://localhost:5000/logout {OIDC.user_getfield('email')} {OIDC.user_getfield('zoneinfo')} {OIDC.user_getfield('preferred_username')}")

@app.route("/")
def landing_page():
    if OIDC.user_loggedin:
        return flask.redirect(flask.url_for('.logged_in'))
    else:
        return flask.Response("Landing page, try to go to <a href='https://oidctest.tinystage.test/login'>https://oidctest.tinystage.test/login</a>")

@app.route("/login")
def login():
    return flask.redirect(flask.url_for('.logged_in'))

@app.route("/logout")
def logout():
    if OIDC.user_loggedin:
        OIDC.logout()
        flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('.landing_page'))
