#!/usr/bin/python

import os
import pyaem
import commands
import json

def main ():
    module = AnsibleModule(
        argument_spec = dict(
            host = dict(required=True),
            port = dict(required=True),
            user_path = dict(required=True),
            user_name = dict(required=True),
            password = dict(required=True),
            group_name = dict(required=False)
        )
    )

    host = module.params['host']
    port = module.params['port']
    user_path = module.params['user_path']
    user_name = module.params['user_name']
    password = module.params['password']
    group_name = module.params['group_name']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)

    if group_name != None:
        result = aem.create_user(user_path, user_name, password, membership = group_name)
    else:
        result = aem.create_user(user_path, user_name, password)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
