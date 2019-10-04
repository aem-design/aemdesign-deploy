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
            old_password = dict(required=True),
            new_password = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    user_name = module.params['user_name']
    user_path = module.params['user_path']
    old_password = module.params['old_password']
    new_password = module.params['new_password']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.change_password(user_path, user_name, old_password, new_password)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
