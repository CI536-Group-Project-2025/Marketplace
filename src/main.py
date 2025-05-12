from flask import Flask
import item

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello World!\n"

app.register_blueprint(item.bp)
#@app.route('/item/<int:id>')
#def item(id):
#    return f"Item {id}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
