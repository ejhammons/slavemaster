#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
RESTful server to manage web slaves

Commands accepted
=================

/list    List current slaves

/add     Add new slave

/delete  Delete slave

"""

from bottle import get, put, post, delete, run, request
import json
import re
import subprocess

slave_file_list='/etc/lsyncd/servers.conf'


def read_slaves():
    """
    Reads the slaves from slave_file_list
    """

    slaves=[]
    with open(slave_file_list,"r") as slave_fh:
        for line in slave_fh.readlines():
            if not re.match('^#',line):
                slave=re.search('\S+',line)
                if slave:
                    slaves.append(slave.group(0))
    return slaves

def read_raw_slaves():
    """
    Reads the raw contents of slave_file_list
    """

    with open(slave_file_list,"r") as slave_fh:
        slaves=slave_fh.readlines()
    return slaves

def write_slaves(slaves):
    """
    Writes the passed list to slave_file_list
    """

    with open(slave_file_list,"w") as slave_fh:
        slave_fh.writelines(slaves)



@get('/list')
def list_slaves():
    """
    Returns the current list of slaves
    """
    slaves=read_slaves()
    return json.dumps(slaves)

@post('/add')
def add_slave():
    """
    Adds slave passed as json data to the slaves list
    """
    slaves=read_raw_slaves()
    slaves.append(request.json[0]+'\n')
    write_slaves(slaves)
    return json.dumps(read_slaves())

@post('/delete')
def delete_slave():
    """
    Deletes the slave passed as json data from the list of slaves
    """

    slaves=read_raw_slaves()
    matched=True
    while matched:
        matched=False
        for line in slaves:
            if not re.match('^#',line):
                if re.search(request.json[0],line):
                    matched=True
                    slaves.remove(line)
    write_slaves(slaves)
    return json.dumps(read_slaves())

@get('/restart-lsyncd')
def restart_lsyncd():
    """
    Restarts the lsyncd service on the master
    """

    rc=subprocess.call("service lsyncd restart", shell=True, stdout=open("/dev/null","w"))
    return rc

if __name__ == "__main__":
    run(host='0.0.0.0', port=5143, debug=True)
