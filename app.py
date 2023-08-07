from flask import Flask, render_template
from decrypter.decrypter import PasswordDecrypter

app = Flask(__name__)
port = 8888

decrypter = PasswordDecrypter()
login_data = decrypter.main()

@app.route('/')
def home():
    return render_template('index.html', login_data=login_data)

if __name__ == '__main__':
    app.run(debug=True, port=port)