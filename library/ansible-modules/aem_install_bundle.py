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
            bundle_name = dict(required=True),
            bundle_version = dict(required=True),
            file_path = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    bundle_name = module.params['bundle_name']
    bundle_version = module.params['bundle_version']
    file_path = module.params['file_path']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.install_bundle(bundle_name, bundle_version, file_path)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
