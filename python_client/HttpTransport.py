"""OpenHlTest Restconf transport
"""

import sys
import os
import ssl
import time
import json
import requests
import urllib3

if sys.version < '2.7.9':
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
else:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HttpTransport(object):
    """OpenHlTest Restconf transport."""

    def __init__(self, hostname, rest_port=443):
        """ Setup the https connection parameters to a rest server

        Args:
            hostname: hostname or ip address
            rest_port: the rest port of the host
        """
        self._headers = {}
        self._verify_cert = False
        self.trace = False
        self._scheme = 'https'
        self._connection = '%s://%s:%s' % (self._scheme, hostname, rest_port)

    @property
    def trace(self):
        """True/False to trace all http commands and responses."""
        return self._trace
    @trace.setter
    def trace(self, value):
        self._trace = value

    def get(self, target):
        response = self._send_recv('GET', target.url)
        return self._populate_target(response, target)

    def create(self, parent, target, arg_dict):
        object_key = '%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)
        payload = { object_key: {} }
        for key in arg_dict.keys():
            if key == 'self':
                continue
            payload[object_key][key] = arg_dict[key]
        location = self._send_recv('POST', parent.url, payload)
        return self.get(target)

    def update(self, url, payload):
        return self._send_recv('PATCH', url, payload)

    def delete(self, url):
        return self._send_recv('DELETE', url)

    def execute(self, url, payload):
        return self._send_recv('POST', url, payload)

    def _print_trace(self, * args):
        if self.trace is True:
            print('%s %s' % (int(time.time()), ' '.join(args)))
    
    def _send_recv(self, method, url, payload=None, fid=None, file_content=None):
        headers = self._headers
        if url.startswith(self._scheme) == False:
            url = '%s/%s' % (self._connection, url.strip('/'))

        self._print_trace(method, url)
        
        if payload is not None:
            headers['Content-Type'] = 'application/json'
            if isinstance(payload, dict) is True:
                payload = json.dumps(payload)
            response = requests.request(method, url, data=payload, headers=headers, verify=self._verify_cert)
        elif method == 'POST' and fid is not None:
            headers['Content-Type'] = 'application/octet-stream'
            if fid.__class__.__name__ == 'BufferedReader':
                headers['Content-Length'] = os.fstat(fid.raw.fileno()).st_size
                response = requests.request(method, url, data=fid.raw, headers=headers, verify=self._verify_cert)
            else:                            
                response = requests.request(method, url, data=fid, headers=headers, verify=self._verify_cert)
        elif method == 'POST' and file_content is not None:
            headers['Content-Type'] = 'application/octet-stream'
            response = requests.request(method, url, data=json.dumps(file_content), headers=headers, verify=self._verify_cert)
        else:
            response = requests.request(method, url, data=None, headers=headers, verify=self._verify_cert)

        while(response.status_code == 202):
            time.sleep(1)
            location = response.headers['Location']
            if location.startswith('/') is True:
                location = '%s%s' % (self._connection, location)
            self._print_trace('GET', location)
            response = requests.request('GET', location, verify=self._verify_cert)
            
        if response.status_code == 201:
            return response.headers['Location']
        elif response.status_code == 204:
            return None
        elif str(response.status_code).startswith('2') is True:
            if response.headers.get('Content-Type'):
                if 'application/json' in response.headers['Content-Type']:
                   return response.json()
            return None
        else:
            raise Exception('%s %s %s' % (response.status_code, response.reason, response.text))

    def _populate_target(self, payload, target):
        payload = payload['%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)]
        if isinstance(payload, list):
            target_list = []
            for item in payload:
                target_item = target.create_sibling(item[target.YANG_KEY])
                target_item._values = item
                target_list.append(target_item)
            return target_list
        else:
            target._values = payload
        return target

