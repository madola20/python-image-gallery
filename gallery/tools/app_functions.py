import psycopg2
from .secrets import *
import boto3
import json

db_hostname = "image-gallery.c3dkgwsygvad.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_username = "image_gallery"
password_file = "gallery/ui/temp_pw_file.txt"
connection = None
cursor = None




def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']


def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)



def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=db_name, user=get_username(secret), password=get_password(secret))

def fetch_results():
    return cursor.fetchall()

def execute(query,args=None):
    global connection
    global cursor
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
        return cursor
    
def existing(query_username):
    res1 = execute("select exists(select 1 from users where username='" + query_username + "');")
    res2 = str(cursor.fetchall())

    
    if res2 == "[(True,)]":
        return True
    
    else:
        return False
