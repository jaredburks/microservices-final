# app.py
import os
import shutil
from flask import Flask, send_file, g, render_template, request, Response, jsonify, redirect
from flask import *
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from datetime import datetime 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['SECRET_KEY'] = '12345678'
db = SQLAlchemy()

# LoginManager is needed to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
 
usage_stats = []  # in-memory storage

def record_usage():
    stats = {
        'timestamp': datetime.now(),
        'endpoint': request.path,
        'method': request.method,
        #'user_id': g.user.id if hasattr(g, 'user') else None, 
        'status_code': Response.status_code,
    }
    usage_stats.append(stats)  # Add the stats to the list

@app.before_request
def before_request():
    g.start_time = datetime.now()

@app.after_request
def after_request(response):
    record_usage()
    return response
 
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/admin")
def admin():
    return render_template("admin.html", stats=usage_stats)  # Pass the stats

@app.route('/')
def index():
    return render_template("index.html")

UPLOAD_FOLDER = 'uploads'  # Base upload directory. Used as temp folder. Deleted after zip to save space.

@app.route("/upload", methods=["POST"])
def upload():
    if 'dataset' not in request.form or 'subdirectory1' not in request.form or 'subdirectory2' not in request.form:
        return jsonify({'error': 'Missing form data'}), 400 

    dataset_name = request.form['dataset']
    subdirectory1_name = request.form['subdirectory1']
    subdirectory2_name = request.form['subdirectory2']

    # Create dataset directory
    dataset_dir = os.path.join(UPLOAD_FOLDER, dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)

    # Create subdirectories 
    subdirectory1_path = os.path.join(dataset_dir, subdirectory1_name)
    subdirectory2_path = os.path.join(dataset_dir, subdirectory2_name)
    os.makedirs(subdirectory1_path, exist_ok=True)
    os.makedirs(subdirectory2_path, exist_ok=True)

    # Process uploaded files
    if 'pic_set_1' in request.files:
        for file in request.files.getlist('pic_set_1'):
            filename = secure_filename(file.filename)  # Should sanitize filenames for security and consistency.
            file.save(os.path.join(subdirectory1_path, filename))

    if 'pic_set_2' in request.files:
        for file in request.files.getlist('pic_set_2'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(subdirectory2_path, filename))

    # Zip the dataset directory
    shutil.make_archive(base_name=f'{dataset_name}_dataset', format='zip', root_dir=UPLOAD_FOLDER, base_dir=dataset_name)
    shutil.rmtree(UPLOAD_FOLDER) # Delete uploads directory.

    # Return the zipped dataset file
    print("Dataset created!")
    return send_file(f'{dataset_name}_dataset.zip', mimetype='zip', as_attachment=True)

if __name__ == '__main__': 
    app.run(debug=False) 