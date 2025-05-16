from flask import Flask
from flask_session import Session
from marketplace import basket, catalogue, item, users

app = Flask(__name__)

# Session config - for keeping users logged in.
# This will log users out when they close the browser
app.config["SESSION_PERMANENT"] = False
# This will store session data on the filesystem
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(basket.bp)
app.register_blueprint(item.bp)
app.register_blueprint(users.bp)
app.register_blueprint(catalogue.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
