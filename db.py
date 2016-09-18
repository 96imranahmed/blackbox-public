import MySQLdb
from flask import request
import httplib2
import json
from oauth2client import client
from oauth2client import GOOGLE_AUTH_URI
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import GOOGLE_TOKEN_URI
conn = None
cur = None

def db_execute(sql):
    global cur
    global conn
    try:
        cur.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='Blackbox$default')
        cur = conn.cursor()
        cur.execute(sql)

def queryDB(identifier, data_in):
    global conn
    global cur
    if conn is None:
        conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db='Blackbox$default')
        cur = conn.cursor()
    else:
        conn.ping(True)
    if identifier == 'new_user_check':
        sql = 'select * from `users` where user_id = ' + str(data_in)
        db_execute(sql)
        if (cur.rowcount == 0):
            return False
        else:
            return True
    elif identifier == 'add_user':
        try:
            sql = 'insert into `users` (user_id) values (' + str(data_in) + ')'
            db_execute(sql)
            conn.commit()
        except:
            conn.rollback()
    elif identifier == 'del_user':
        try:
            sql = 'delete from `users` where user_id =' + str(data_in)
            db_execute(sql)
            conn.commit()
        except:
            conn.rollback()
    elif identifier == 'get_user_name':
        sql = 'select (name) from `users` where user_id = ' + str(data_in)
        db_execute(sql)
        row = cur.fetchone()
        if (row == None or row[0] == None) :
            sql = 'UPDATE `users` SET name = \'_is_updating_\' where user_id = ' + str(data_in)
            db_execute(sql)
            conn.commit()
            return 0
        else:
            return row[0]
    elif identifier == 'set_user_name':
        try:
            sql = 'UPDATE `users` SET name = \'' + str(data_in[1]) + '\' where user_id = ' + str(data_in[0])
            print(sql)
            db_execute(sql)
            conn.commit()
        except:
            conn.rollback()
    elif identifier == 'google_cal_check':
        sql = 'select `google_calendar_token` from `users` where user_id = ' + str(data_in)
        db_execute(sql)
        row = cur.fetchone()
        if row[0] == None:
            return False
        else:
            tokens = row[0].split('||')
            try:
                credentials = client.AccessTokenCredentials(tokens[0], request.headers.get('User-Agent'))
                http = httplib2.Http()
                http = credentials.authorize(http)
                cur_cred = json.loads(credentials.to_json())
                if (cur_cred['invalid'] == False):
                    print('Current authentication tokens are valid')
                else:
                    credentials = client.OAuth2Credentials(None,
                                                           "999131376789-4ktm5jvahkbbj61n47hg7c0nl6a72jlm.apps.googleusercontent.com",
                                                           "r-vJNSz_WZyr9vSc9QRKzHS2", tokens[1], None,
                                                           GOOGLE_TOKEN_URI, None, revoke_uri=GOOGLE_REVOKE_URI,
                                                           id_token=None, token_response=None)
                    http = httplib2.Http()
                    http = credentials.authorize(http)
                    cur_cred = json.loads(credentials.to_json())
                    refresh_token = cur_cred['refresh_token']
                    cur_token = cur_cred['access_token']
                    queryDB('google_token_enter', [str(data_in), str(cur_token) + '||' + str(refresh_token)])
                    new_cred = client.AccessTokenCredentials(cur_token, request.headers.get('User-Agent'))
                    return new_cred
                    print('Tried to renew authentication tokens')
                    print(cur_cred)
                return True
            except:
                return False
    elif identifier == 'google_token_enter':
        try:
            sql = 'UPDATE `users` SET google_calendar_token = \'' + str(data_in[1]) + '\' where user_id = ' + str(data_in[0])
            db_execute(sql)
            conn.commit()
        except:
            conn.rollback()