import flask
import munch
from flask_openid import OpenID

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["OPENID_ENDPOINT"] = "https://ipsilon.tinystage.test/idp/openid/"

oid = OpenID(app, "/var/tmp/openidstore", safe_roots=[])


@app.before_request
def before_request():
    flask.session.permanent = True


@oid.after_login
def do_login(resp):
    user = {"openid_identity_url": resp.identity_url, "username": resp.nickname}
    flask.session["user"] = user
    app.logger.debug(f"{user}")
    return flask.redirect(flask.url_for(".home"))


@app.route("/")
def home():
    title = "<h1>OpenID Test Application</h1>"
    if flask.session.get("user"):
        return flask.Response(
            f"{title}"
            f"<p>You are now logged in.</p>"
            f"<p><strong><a href=\"{flask.url_for('.logout')}\">logout</a></strong></p>"
            f"<p>Details: {flask.session['user']}</p>"
        )
    return flask.Response(
        f"{title}" f"<p><a href=\"{flask.url_for('login')}\">login</a></p>"
    )


@app.route("/login")
@oid.loginhandler
def login():
    if flask.session.get("user"):
        return redirect(flask.url_for(".home"))
    return oid.try_login(
        app.config["OPENID_ENDPOINT"],
        ask_for=["email", "nickname"],
        ask_for_optional=[],
    )


@app.route("/logout")
def logout():
    flask.session["user"] = None
    flask.flash("You have been logged out")
    return flask.redirect(flask.url_for(".home"))
