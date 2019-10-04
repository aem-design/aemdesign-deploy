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
            user_name = dict(required=True),
            group_path = dict(required=True),
            group_name = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    user_name = module.params['user_name']
    group_path = module.params['group_path']
    group_name = module.params['group_name']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)

    result = aem.add_user_to_group(user_name, group_path, group_name)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
