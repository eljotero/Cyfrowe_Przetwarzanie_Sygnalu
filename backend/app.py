from flask import Flask
from signal import db, Signal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/<int:signalID>', methods=['POST'])
def process_signal(signalID):
    return signalID


if __name__ == '__main__':
    app.run()
