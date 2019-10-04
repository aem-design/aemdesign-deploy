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
            path_name = dict(required=True),
            path_primary_type = dict(required=True),
            path_mixin_types_csv = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    path_name = module.params['path_name']
    path_primary_type = module.params['path_primary_type']
    path_mixin_types_csv = module.params['path_mixin_types_csv']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    params = { 'jcr:primaryType': path_primary_type, 'jcr:mixinTypes': path_mixin_types_csv.split(',') }
    result = aem.create_path(path_name, **params)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
