from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY, JWT_SECRET_KEY, UPLOAD_FOLDER, DATABASE
import os, datetime
from werkzeug.utils import secure_filename

ALLOWED_EXT = {'png','jpg','jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
jwt = JWTManager(app)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    fullname = data.get('fullname','')
    if not username or not password:
        return jsonify({'msg':'username & password required'}),400
    pw_hash = generate_password_hash(password)
    conn = get_db(); c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username,password,fullname) VALUES (?,?,?)', (username,pw_hash,fullname))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'msg':'username taken'}),400
    return jsonify({'msg':'ok'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = get_db(); c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?',(username,))
    row = c.fetchone()
    if not row: return jsonify({'msg':'invalid'}),401
    if not check_password_hash(row['password'], password):
        return jsonify({'msg':'invalid'}),401
    access = create_access_token(identity={'id':row['id'],'username':row['username'],'fullname':row['fullname']})
    return jsonify({'access_token':access})

@app.route('/api/presence', methods=['POST'])
@jwt_required()
def presence():
    user = get_jwt_identity()
    # multipart/form-data expected: type (in/out), lat, lon, note, photo file
    ttype = request.form.get('type')
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    note = request.form.get('note','')
    timestamp = datetime.datetime.utcnow().isoformat()
    photo_path = None
    if 'photo' in request.files:
        f = request.files['photo']
        if f and allowed_file(f.filename):
            fname = secure_filename(f"{user['id']}_" + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') + '_' + f.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(save_path)
            photo_path = fname
    # compute duration if needed: for simplicity, if this is 'out', find last 'in' and compute minutes
    duration_minutes = None
    conn = get_db(); c = conn.cursor()
    if ttype == 'out':
        c.execute('SELECT timestamp FROM attendance WHERE user_id=? AND type=? ORDER BY id DESC LIMIT 1',(user['id'],'in'))
        last_in = c.fetchone()
        if last_in:
            t_in = datetime.datetime.fromisoformat(last_in['timestamp'])
            t_out = datetime.datetime.fromisoformat(timestamp)
            duration_minutes = int((t_out - t_in).total_seconds()//60)
    c.execute('INSERT INTO attendance (user_id,timestamp,type,lat,lon,photo_path,note,duration_minutes) VALUES (?,?,?,?,?,?,?,?)',
              (user['id'], timestamp, ttype, lat, lon, photo_path, note, duration_minutes))
    conn.commit()
    return jsonify({'msg':'ok'})

@app.route('/api/records', methods=['GET'])
@jwt_required()
def records():
    # only admin-like user should see all; for simplicity, if username == 'admin' return all
    user = get_jwt_identity()
    conn = get_db(); c = conn.cursor()
    if user['username']=='admin':
        c.execute('SELECT a.*, u.username, u.fullname FROM attendance a JOIN users u ON u.id=a.user_id ORDER BY a.id DESC')
    else:
        c.execute('SELECT a.*, u.username, u.fullname FROM attendance a JOIN users u ON u.id=a.user_id WHERE a.user_id=? ORDER BY a.id DESC',(user['id'],))
    rows = [dict(r) for r in c.fetchall()]
    return jsonify(rows)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
