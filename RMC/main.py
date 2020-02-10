import ir
import sqlfunc as sql
from getpass import getpass
import netaddr
import sys

if __name__ == '__main__':
    usr = raw_input('USER ID >>> ')
    pwd = getpass('PASSWORD >>> ')

    conn,cursor = sql.connectSQL()
    usr_id = sql.authentication(conn,cursor,usr,pwd)

    if(usr_id==-1):
        print('NOT AUTHENTICATED')
        sys.exit()

    dev_list = sql.showDevice(conn,cursor,usr_id)
    if(len(dev_list)==0):
        print('THERE IS NO DEVICES.')
        sys.exit()

    print('DEVICE LIST')
    for dev in dev_list:
        print(dev)
    dev_name = raw_input('INPUT DEVICE NAME >>> ')

    dev_info = sql.getDevice(conn,cursor,usr_id,dev_name)
    if(dev_info==-1):
        print('THERE IS NOT SUCH A DEVICE.')
        sys.exit()

    cmd_list = sql.showCommand(conn,cursor,dev_info['id'])
    if(len(cmd_list)==0):
        print('THERE ARE NO COMMANDS.')
        sys.exit()

    print('COMMAND LIST')
    for cmd in cmd_list:
        print(cmd)

    cmd_name = raw_input('INPUT COMMAND NAME >>> ')
    signal = sql.getCommand(conn,cursor,dev_info['id'],cmd_name)
    if(signal=='no_signal'):
        print('THERE IS NOT SUCH A COMMAND.')
        sys.exit()

    IP = dev_info['ip']
    MAC = netaddr.EUI(dev_info['mac'])
    Port = dev_info['port']
    RM3Device = ir.RM3Mini(IP, MAC, Port)
    RM3Device.sendIR(signal)
    sys.exit()
