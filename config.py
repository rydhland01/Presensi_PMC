import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
SECRET_KEY = 'change-this-to-a-strong-secret'
JWT_SECRET_KEY = 'change-this-too'
DATABASE = os.path.join(BASEDIR, 'presensi.db')
