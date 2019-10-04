#!/usr/bin/python

import commands
import urllib2
import warnings
import json
#TODO: remove, depreciated
def main ():
    warnings.warn("deprecated use ansible role [aem-license]")
    module = AnsibleModule(
        argument_spec = dict(
            url = dict(required=True)
        )
    )

    url = module.params['url']

    try:
      f = urllib2.urlopen('{0}')
      if f.getcode() == 200:
        print(json.dumps({ 'msg': 'AEM license page is ready' }))
      else:
        print(json.dumps({ 'failed': True, 'msg': 'Unexpected status code {0} when checking AEM license page'.format(f.getcode()) }))
    except Exception as e:
      print(json.dumps({ 'failed': True, 'msg': 'Unexpected exception when checking AEM license page: {0}'.format(e) }))

from ansible.module_utils.basic import *
main()
