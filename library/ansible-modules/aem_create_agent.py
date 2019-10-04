#!/usr/bin/python

import os
import pyaem
import commands
import re
import json

def main ():
    module = AnsibleModule(
        argument_spec = dict(
            host = dict(required=True),
            port = dict(required=True),
            aem_username = dict(required=True),
            aem_password = dict(required=True),
            stack = dict(required=True),
            agent_id = dict(required=True),
            agent_name = dict(required=True),
            agent_type = dict(required=True),
            agent_loglevel = dict(required=True),
            agent_retrydelay = dict(required=True),
            dest_group = dict(required=True),
            dest_username = dict(required=True),
            dest_password = dict(required=True),
            dest_url = dict(required=True),
            run_mode = dict(required=True)
        )
    )

    host = module.params['host']
    port = module.params['port']
    stack = module.params['stack']
    agent_id = module.params['agent_id']
    agent_name = module.params['agent_name']
    agent_type = module.params['agent_type']
    agent_loglevel = module.params['agent_loglevel']
    agent_retrydelay = module.params['agent_retrydelay']
    dest_username = module.params['dest_username']
    dest_password = module.params['dest_password']
    dest_group = module.params['dest_group']
    dest_url = module.params['dest_url']
    run_mode = module.params['run_mode']

    agent_title = '{0} agent to {1} {2}'.format(agent_type, dest_group, agent_id)

    aem_username = module.params['aem_username']
    aem_password = module.params['aem_password']

    aem = pyaem.PyAem(aem_username, aem_password, host, port)

    params = {
        'jcr:content/jcr:title': agent_title,
        'jcr:content/jcr:description': agent_title,
        'jcr:content/logLevel': agent_loglevel,
        'jcr:content/retryDelay': agent_retrydelay
    }
    result = aem.create_agent(agent_name, agent_type, dest_username, dest_password, dest_url, run_mode, **params)

    if result.is_failure():
        print(json.dumps({ 'failed': True, 'msg': result.message }))
    else:
        print(json.dumps({ 'msg': result.message }))

from ansible.module_utils.basic import *
main()
