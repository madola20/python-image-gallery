import psycopg2
#from secrets import get_secret_image_gallery
import boto3
import json


db_hostname = "python-image-gallery-users.c3dkgwsygvad.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_username = "image_gallery"
password_file = "temp_pw_file.txt"
connection = psycopg2.connect(host=db_hostname, dbname=db_name, user=db_username,
                                                                         password="HARDCODED-NOW-INCORRECT")
cursor = None


def connect():
    connection = psycopg2.connect(host=db_hostname, dbname=db_name, user=db_username,password="HARDCODED-NOW-INCORRECT")
    
    
def execute(query, args=None):
    global connection
    global cursor
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
        return cursor
    
def fetch_results():
    return cursor.fetchall()
                                                
