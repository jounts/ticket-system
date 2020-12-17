from auth.auth_app import app
from auth.db import db_check

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
