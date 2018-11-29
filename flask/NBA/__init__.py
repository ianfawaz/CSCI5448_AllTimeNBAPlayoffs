#adapted from flask tutorial: http://flask.pocoo.org/docs/1.0/tutorial/


import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    apps = Flask(__name__, instance_relative_config=True)#i changed all app to apps to get rid of conflict on from . import app on line 39
    apps.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(apps.instance_path, 'NBA.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        apps.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        apps.config.from_mappsing(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(apps.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @apps.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(apps)

    from . import auth
    apps.register_blueprint(auth.bp)

    from . import app#was import blog, and below was blog.bp
    apps.register_blueprint(app.bp)
    apps.add_url_rule('/', endpoint='index')

    return apps