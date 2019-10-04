#!/usr/bin/python

""" Download large files from Google Drive.
https://github.com/drodrig/utils/blob/master/google-drive-large-file-downloader.py
"""

import requests
import re
import sys
import json

def main ():
    module = AnsibleModule(
        argument_spec = dict(
            google_file_url = dict(required=True),
            file_name = dict(required=True)
        )
    )

    google_file_url = module.params['google_file_url']
    file_name = module.params['file_name']

    url = google_file_url
    r = requests.get(url)
    match = re.search(r'confirm=(.{4})', r.content)
    url = url + '&confirm=' + match.group(1)
    r2 = requests.get(url, cookies=r.cookies)
    open(file_name, 'wb').write(r2.content)

    print(json.dumps({ 'msg': 'Downloaded {file_name}'.format(file_name = file_name) }))

from ansible.module_utils.basic import *
main()
