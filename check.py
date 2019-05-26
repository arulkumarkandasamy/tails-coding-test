import os
from flask import Flask
from stores.config import config


app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
app.config.from_pyfile('config.cfg', silent=True)


def application_data():
    return {"maintainer": "Damyan Bogoev",
            "git_repo": "https://github.com/damyanbogoev/flask-bookshelf"}


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8090)))
