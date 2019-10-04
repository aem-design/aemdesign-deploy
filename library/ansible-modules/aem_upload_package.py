#!/usr/bin/python

import os
import pyaem
import commands
import time
import json

def main ():
    module = AnsibleModule(
        argument_spec = dict(
            host = dict(required=True),
            port = dict(required=True),
            group_name = dict(required=True),
            package_name = dict(required=True),
            package_version = dict(required=False),
            file_path = dict(required=True),
            aem_username = dict(required=True),
            aem_password = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    group_name = module.params['group_name']
    package_name = module.params['package_name']
    package_version = module.params['package_version']
    file_path = module.params['file_path']

    aem_username = module.params['aem_username']
    aem_password = module.params['aem_password']

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.upload_package_sync(group_name, package_name, package_version, file_path, force = 'true')

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
