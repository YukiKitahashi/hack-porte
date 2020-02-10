import pymysql

def connectSQL(host='localhost',db='rmmini3',usr,pwd):
    conn = pymysql.connect(host=host,user=usr,password=pwd,db=db,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    return conn, cursor

def closeSQL(conn,cursor):
    cursor.close()
    conn.close()

def authentication(conn,cursor,usr,pwd):
    sql_template = 'select id from usrinfo where (usr=\"{usr}\" and pwd=\"{pwd}\");'
    sql = sql_template.replace('{usr}',usr).replace('{pwd}',pwd)
    print(sql)
    cursor.execute(sql)
    rets = cursor.fetchall()
    if(len(rets)==1):
        return rets[0]['id']
    closeSQL(conn,cursor)
    return -1

def showDevice(conn,cursor,usr_id):
    sql_template = 'select dev_name from devinfo where (usr_id={usr_id});'
    sql = sql_template.replace('{usr_id}',str(usr_id))
    cursor.execute(sql)
    rets = cursor.fetchall()
    dev_list = []
    for r in rets:
        dev_list.append(r['dev_name'])
    return dev_list

def getDevice(conn,cursor,usr_id,dev_name):
    sql_template = 'select * from devinfo where (usr_id={usr_id} and dev_name=\"{dev_name}\");'
    sql = sql_template.replace('{usr_id}',str(usr_id)).replace('{dev_name}',dev_name)
    cursor.execute(sql)
    rets = cursor.fetchall()
    if(len(rets)==1):
        return rets[0]
    closeSQL(conn,cursor)
    return -1

def showCommand(conn,cursor,dev_id):
    sql_template = 'select command from signalinfo where (dev_id={dev_id});'
    sql = sql_template.replace('{dev_id}',str(dev_id))
    cursor.execute(sql)
    rets = cursor.fetchall()
    cmd_list = []
    for r in rets:
        cmd_list.append(r['command'])
    return cmd_list

def getCommand(conn,cursor,dev_id,command):
    sql_template = 'select sign from signalinfo where (dev_id={dev_id} and command=\"{command}\");'
    sql = sql_template.replace('{dev_id}',str(dev_id)).replace('{command}',command)
    cursor.execute(sql)
    rets = cursor.fetchall()
    closeSQL(conn,cursor)
    if(len(rets)==1):
        return rets[0]['sign']
    return "no_signal"
