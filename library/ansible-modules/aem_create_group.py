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
            group_path = dict(required=True),
            group_name = dict(required=True),
            group_desc = dict(required=True),
            group_parent = dict(required=True, type='str')
        )
    )

    host = module.params['host']
    port = module.params['port']
    group_path = module.params['group_path']
    group_name = module.params['group_name']
    group_desc = module.params['group_desc']
    group_parent = module.params['group_parent']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)

    params = { 'profile/givenName': group_desc }

    if group_parent != '':
        params['membership'] = group_parent

    result = aem.create_group(group_path, group_name, **params)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
