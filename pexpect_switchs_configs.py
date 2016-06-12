#!/usr/bin/env python

import os,pexpect

if not os.path.exists('/tmp/switch'):
        os.system("svn co  svn+ssh://root@xxx.xxxx.com/sw/systems/subversion/switch /tmp/switch")

os.chdir("/tmp/switch")


swlist = [ 'core01','core02','sw25','sw26','sw27','sw28','sw12', 'sw07','sw08', 'sw09', 'sw05', 'sw06', 'sw03', 'sw04', 'sw02', 'sw13', 'sw15', 'sw20', 'sw21','sw23','sw29','sw24','sw11','sw10','sw01','sw14','sw16','sw17','sw18', 'sw19', 'sw22']
namelist = ["conf","arp","mac"]

def get(cmd,sw):
        ssh = pexpect.spawn(cmd + sw)
        ssh.expect('[#$>]')
        ssh.sendline('en')
        ssh.expect('[#$>]')
        ssh.sendline('skip')
        ssh.expect('[#$>]')
        for name in namelist:
                ssh.sendline('show %s' %name)
                ssh.logfile_read = open(sw+"."+name,'w')
                ssh.expect('[#$>]')
        ssh.sendline('quit')
        ssh.expect('[#$>]')
        ssh.sendline('exit')
        # 为了ssh能从交换机退出必须加上下面的异常处理
        try:
                ssh.expect('[#$>]')
        except:
                pass



for sw in swlist:
        #免除错误提示
        cmd = '/usr/bin/sshpass -p "PASSWORD" ssh -o StrictHostKeychecking=no USERNAME@'
        #for name in namelist:
        get(cmd,sw)

os.system('cd /tmp/switch ; svn add --force . ;svn commit -m "switch config update";rm -rf /tmp/switch')
