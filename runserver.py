
from venus import app, init_app

if __name__ == '__main__':
    app.config.from_pyfile('settings_dev.py')
    init_app()
    app.run(debug=app.config['DEBUG'], host='0.0.0.0',port=80)
else :
    init_app()
