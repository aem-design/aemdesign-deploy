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
            agent_name = dict(required=True),
            run_mode = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    agent_name = module.params['agent_name']
    run_mode = module.params['run_mode']

    aem_username = os.getenv('crx_username')
    aem_password = os.getenv('crx_password')

    aem = pyaem.PyAem(aem_username, aem_password, host, port)
    result = aem.delete_agent(agent_name, run_mode)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
