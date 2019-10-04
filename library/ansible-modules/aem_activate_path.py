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
            path = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    path = module.params['path']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.activate_path(path, ignoredeactivated = 'true', onlymodified = 'false')

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
