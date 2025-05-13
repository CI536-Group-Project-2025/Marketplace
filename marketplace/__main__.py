from flask import Flask
import psycopg2
from marketplace import item, users

app = Flask("Marketplace")

app.register_blueprint(item.bp)
app.register_blueprint(users.bp)

@app.route('/')
def hello():
    # This route should return the catalogue page
    return f"Hello World!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
