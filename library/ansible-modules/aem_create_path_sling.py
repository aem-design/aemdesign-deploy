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
            path_base = dict(required=True),
            path_type = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    path_name = module.params['path_name']
    path_base = module.params['path_base']
    path_type = module.params['path_type']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    params = { ':nameHint': path_name, 'jcr:primaryType': path_type, 'jcr:mixinTypes': 'rep:AccessControllable' }

    try:
        if not path_base.endswith("/*"):
            path_base = '{0}/*'.format(path_base)

        result = aem.create_path(path_base, **params)

        if result.is_failure():
            print(json.dumps({ 'failed': True, 'msg': result.message }))
        else:
            print(json.dumps({ 'msg': result.message }))
    except pyaem.PyAemException as e:
        print(json.dumps({ 'msg': 'Allow error due to inability to differentiate existing path from real error when response code is 500' + e.response['body'] }))

from ansible.module_utils.basic import *
main()
