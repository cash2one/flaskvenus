
from venus import app, db

if __name__ == '__main__':
    app.config.from_pyfile('settings_dev.py')
    db.init_app(app)
    app.run(debug=app.config['DEBUG'], host='0.0.0.0',port=80)
else :
    db.init_app(app)
