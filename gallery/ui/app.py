from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from werkzeug.utils import secure_filename

import boto3

import psycopg2
import sys

from functools import wraps

from ..data.user import *
from ..data.postgres_user_dao import PostgresUserDAO
from ..data.db import User

from ..tools.s3 import *
sys.path.append('/home/ec2-user')


app = Flask(__name__)
app.secret_key = b'safsf987s9f7w9#$*bygh$@'
s3 = boto3.resource('s3')


connect()

def get_user_dao():
    return PostgresUserDAO()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        the_user = get_user_dao().get_user_by_username(request.form["username"])
        if the_user is None or the_user.password != request.form["password"]:
            return redirect("/invalidLogin")
        else:
            session["username"] = request.form["username"]
            if check_admin():
                return redirect('/admin/users')
            else:
                return redirect("/")
    else:
        return render_template('login.html')

@app.route('/gallery', methods=['GET', 'POST'])
def display_gallery():
    if request.method == 'POST':
        del_object = request.form['object']
        s3.meta.client.delete_object(Bucket='python-image-gallery-bucket', Key=del_object)
        return redirect ('/gallery')
    
    else:
        images = []
        #s3 = boto3.resource('s3')
        user_bucket = s3.Bucket("python-image-gallery-bucket")
        for file in user_bucket.objects.all():
            images.append(file.key)
            return render_template('gallery.html', images=images)

@app.route('/upload', methods=['GET','POST'])
def upload_image():
    if request.method == 'POST':
        img = request.files['file']
        filename = secure_filename(img.filename)
        img.save(filename)
        #session['file'] = request.form['file']
        s3.meta.client.upload_file(Bucket='python-image-gallery-bucket', Filename=filename, Key=filename, ExtraArgs={'ContentType':'image/jpeg'})
        return redirect('/')
    else:
        return render_template('upload_images.html')

@app.route('/debugSession')
def debugSession():
    result = ""
    for key, value in session.items():
        result += key+ "->"+str(value)+"<br />"
        return result
    
@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid login"

##############
# define admin
#############
def check_admin():
    return 'username' in session and session['username'] == 'fred'

def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view (**kwargs)
    return decorated

@app.route('/admin/users')
@requires_admin
def list_users():
    res = execute('select username, password from users')
    #return render_template('user.html', users=get_user_dao().get_users())
    results = fetch_results()
    
    user_info = []
    for row in results:
        a,b = row
        user_info.append((a,b))
        
        return render_template('main_admin_page.html', users=user_info)

@app.route('/admin/delete_user')
@requires_admin
def user():
    return 'peace out'

@app.route('/admin/modify_user')
@requires_admin
def modify_user():
    return 'modify user'

@app.route('/admin/create_user')
@requires_admin
def create_user():
    return 'create user'
            
