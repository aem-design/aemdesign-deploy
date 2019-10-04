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
            path = dict(required=True),
            property_name = dict(required=True),
            property_value = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    path = module.params['path']
    property_name = module.params['property_name']
    property_value = module.params['property_value']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.set_property(path, property_name, property_value)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
