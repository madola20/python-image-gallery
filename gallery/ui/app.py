from flask import Flask
import psycopg2
import sys

from flask import render_template
from ..tools.app_functions import *
from ..tools.secrets import *

sys.path.append('/home/ec2-user')
#from functions import Functions


#############################
#DATABASE SETUP
############################

#############################
#func_class = Function()

app = Flask(__name__)




@app.route('/admin')
def list_users():
    # func_class.connect()
    connect()
    res = execute('select username, password from users')
    results = fetch_results()
    
    user_info = []
    for row in results:
        a,b = row
        user_info.append((a,b))
        # func_class.co
        return render_template('main_admin_page.html', users=user_info)
    
    @app.route('/admin/delete_user')
    def user():
        return 'peace out'
    
    @app.route('/admin/modify_user')
    def modify_user():
        return 'modify user'
    
    @app.route('/admin/create_user')
    def create_user():
        return 'create user'
                                                     
