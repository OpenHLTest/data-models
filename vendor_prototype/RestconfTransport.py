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

class RestconfTransport(object):
    """OpenHlTest Restconf transport."""

    def __init__(self, hostname, rest_port=443):
        """ Setup the http connection parameters to a host

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

    def get(self, url, fid=None):
         return self._send_recv('GET', url, payload=None, fid=fid)
    
    def post(self, url, payload=None, fid=None, file_content=None):
        return self._send_recv('POST', url, payload, fid, file_content)

    def patch(self, url, payload):
        return self._send_recv('PATCH', url, payload)

    def delete(self, url, payload=None):
        return self._send_recv('DELETE', url, payload)

    def help(self, url):
        return self._send_recv('OPTIONS', url)

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
            response = requests.request(method, url, data=json.dumps(payload), headers=headers, verify=self._verify_cert)
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
            response = requests.request('GET', response.headers['Location'], verify=self._verify_cert)
            self._print_trace('GET', response.headers['Location'])
            time.sleep(1)
            
        if response.status_code == 201:
            return self.get(response.headers['Location'])
        elif response.status_code == 204:
            return None
        elif str(response.status_code).startswith('2') is True:
            if response.headers.get('Content-Type'):
                if 'application/json' in response.headers['Content-Type']:
                    return self._make_lambda(response.json())
                elif 'application/octet-stream' in response.headers['Content-Type'] and fid is not None:
                    for chunk in response.iter_content(chunk_size=1024): 
                        if chunk: 
                            fid.write(chunk)
            return None
        else:
            raise Exception('%s %s %s' % (response.status_code, response.reason, response.text))

    def _make_lambda(self, contentObject):
        if isinstance(contentObject, list):
            data_list = []
            for item in contentObject:
                data_item = self._make_lambda(item)
                data_list.append(data_item)
            return data_list
        elif isinstance(contentObject, dict):
            data_object = lambda: None
            for key in contentObject:
                value = contentObject[key]
                if isinstance(value, dict) or isinstance(value, list):
                    value = self._make_lambda(value)
                setattr(data_object, key, value)
            def dump_operation():
                for name in dir(data_object):
                    if name.startswith('__') or name.startswith('func_') or name == 'dump':
                        continue
                    value = getattr(data_object, name)
                    print('%s: %s' % (name, value))
            setattr(data_object, 'dump', dump_operation)
            return data_object
        else:
            return contentObject