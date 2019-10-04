#!/usr/bin/python

import os
# import pyaem
import commands
import time
import json
import docker

def main ():
    module = AnsibleModule(
        argument_spec = dict(
            host = dict(required=True),
            port = dict(required=True),
            group_name = dict(required=True),
            package_name = dict(required=True),
            package_version = dict(required=False),
            file_path = dict(required=False),
            aem_username = dict(required=True),
            aem_password = dict(required=True),
            api_command = dict(required=True)
        )
    )

    #stick everything into a dictionary for easy reuse
    params = dict(
        host = module.params['host'],
        port = module.params['port'],
        group_name = module.params['group_name'],
        package_name = module.params['package_name'],
        package_version = module.params['package_version'],
        file_path = module.params['file_path'],

        aem_username = module.params['aem_username'],
        aem_password = module.params['aem_password'],
        api_command = module.params['api_command'],

        container_image = 'aemdesign/ansible-playbook',
        container_entrypoint = '/usr/bin/python',
        container_user = 'root',
        container_remove = True,
        container_privileged = True,
        container_volume = "%s:/ansible/playbooks:ro" % ( '/tmp' if module.params['file_path'] is None else module.params['file_path'] )
    )

    client = docker.Client()

    hostconfig=client.create_host_config()

    #create pyaem init command
    params['pyaem_init'] = "aem = pyaem.PyAem('%(aem_username)s', '%(aem_password)s', '%(host)s', '%(port)s'); " % params
    # params['pyaem_error'] = "if result.is_failure(): print(json.dumps({ 'failed': True, 'msg': result.message })); else: print(json.dumps({ 'msg': result.message }));"
    params['pyaem_error'] = "print( json.dumps({ 'failed': True, 'msg': result.message }) if result.is_failure() else json.dumps({ 'msg': result.message }) )"



    params['pyaem_cmd'] = ''

    #create pyaem function command
    if any(True for match in
           [
               'is_package_installed',
               'is_package_uploaded',
               'install_package_sync'
           ]
           if match in params['api_command']
        ):
        params['pyaem_cmd'] = "result = aem.%(api_command)s('%(group_name)s', '%(package_name)s', '%(package_version)s' ); " % params
    elif 'upload_package_sync' in params['api_command']:
        if not params['file_path']:
            module.fail_json(msg={
                'msg':'Missing file Path',
                'api_command': params['api_command']
            })
            return False

        hostconfig = client.create_host_config(privileged=params['container_privileged'],binds=[
            params['container_volume']
        ])
        params['pyaem_cmd'] = "result = aem.upload_package_sync('%(group_name)s', '%(package_name)s', '%(package_version)s', '/ansible/playbooks', force = 'true'); " % params
    else:
        module.fail_json(msg={
            'msg':'Unsuported api_command',
            'api_command': params['api_command']
        })
        return False

    #join pyaem init and function commands
    params['pyaemscript'] = "-c \"import json; import pyaem; %(pyaem_init)s %(pyaem_cmd)s %(pyaem_error)s \"" % params

    #create helper for debugging
    params['pyaemscriptmanual'] = "docker run -it --privileged --entrypoint %(container_entrypoint)s -v %(container_volume)s %(container_image)s %(pyaemscript)s" % params


    container = client.create_container(
        image=params['container_image'],
        command=params['pyaemscript'],
        user=params['container_user'],
        entrypoint=[params['container_entrypoint']],
        host_config=hostconfig
    )
    containerstart = client.start(container=container.get('Id'))

    logs = ''
    for char in client.logs(container=container, stream=True):
        logs = logs + char

    if params['container_remove']:
        client.remove_container(container=container.get('Id'))

    result = {
        'cmd': params['pyaemscript'],
        'logs': logs,
        'container': container,
        'test': params['pyaemscriptmanual'],
        'status': containerstart
    }

    module.exit_json(msg={
        'failed': 'error' in logs,
        'msg': result
    })
    return True


from ansible.module_utils.basic import *
main()
