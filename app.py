from flask import Flask, render_template
from flask_mobility import Mobility
from decrypter.decrypter import decrypt

app = Flask(__name__)
port = 8888

login_data = decrypt()

Mobility(app)

@app.route('/')
def home():
    return render_template('index.html', login_data=login_data)

if __name__ == '__main__':
    app.run(debug=True, port=port)