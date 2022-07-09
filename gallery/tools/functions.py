import psycopg2

class Functions():
    
    def get_password():
        f = open(password_file, "r")
        result = f.readline()
        f.close()
        return result[:-1]
    
    def connect():
        global connection
        connection = psycopg2.connect(host=db_hostname, dbname=db_name, user=db_username, password=get_password())
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
        
        :
        if res2 == "[(True,)]":
            return True
        
        else:
            return False
