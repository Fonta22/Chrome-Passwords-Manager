from flask import Flask, render_template
from decrypter.decrypter import Decrypter

app = Flask(__name__)
port = 8888

login_data = Decrypter.decrypt()

@app.route('/')
def home():
    return render_template('index.html', login_data=login_data)

if __name__ == '__main__':
    app.run(debug=True, port=port)