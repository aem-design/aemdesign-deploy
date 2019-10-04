#!/usr/bin/python

import commands
import urllib2
import json

#TODO: remove, depreciated
def main ():
    warnings.warn("deprecated use ansible role [aem-verify]")
    module = AnsibleModule(
        argument_spec = dict(
            url = dict(required=True)
        )
    )

    url = module.params['url']

    try:
      f = urllib2.urlopen('{0}/libs/granite/core/content/login.html'.format(url.rstrip('/')))
      if f.getcode() == 200:
        print(json.dumps({ 'msg': 'AEM login page is ready' }))
      else:
        print(json.dumps({ 'failed': True, 'msg': 'Unexpected status code {0} when checking AEM login page'.format(f.getcode()) }))
    except Exception as e:
      print(json.dumps({ 'failed': True, 'msg': 'Unexpected exception when checking AEM login page: {0}'.format(e) }))

from ansible.module_utils.basic import *
main()
