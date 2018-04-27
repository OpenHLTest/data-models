"""OpenHlTest Restconf transport
"""

import sys
import os
import ssl
import time
import json
import requests

class HttpError(Exception):
    def __init__(self, response):
        """The base error class for all OpenHlTest errors"""
        self._status_code = response.status_code
        self._reason = response.reason
        self._text = response.text

    @property
    def message(self):
        return '%s %s %s' % (self._status_code, self._reason, self._text)

class AlreadyExistsError(HttpError):
    def __init__(self, response):
        """The requested object exists on the server"""
        super(AlreadyExistsError, self).__init__(response)

class BadRequestError(HttpError):
    def __init__(self, response):
        """The server has determined that the request is incorrect"""
        super(BadRequestError, self).__init__(response)

class NotFoundError(HttpError):
    def __init__(self, response):
        """The requested object does not exist on the server"""
        super(NotFoundError, self).__init__(response)

class ServerError(HttpError):
    def __init__(self, response):
        """The server has encountered an uncategorized error condition"""
        super(ServerError, self).__init__(response)

class HttpTransport(object):
    """OpenHlTest Restconf transport."""

    def __init__(self, hostname, rest_port=443):
        """ Set the connection parameters to a rest server

        Args:
            hostname (str): hostname or ip address
            rest_port (int, optional, default=443): the rest port of the server
        """
        if sys.version < '2.7.9':
            import requests.packages.urllib3
            requests.packages.urllib3.disable_warnings()
        else:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._headers = {}
        self._verify_cert = False
        self.trace = False
        self._scheme = 'https'
        self._connection = '%s://%s:%s' % (self._scheme, hostname, rest_port)

    @property
    def trace(self):
        """bool: Trace all requests and responses."""
        return self._trace
    @trace.setter
    def trace(self, value):
        self._trace = value

    def _get(self, target):
        response = self._send_recv('GET', target.url)
        return self._populate_target(response, target)

    def _create(self, parent, target, arg_dict):
        object_key = '%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)
        payload = { object_key: {} }
        for key in arg_dict.keys():
            if key == 'self':
                continue
            payload[object_key][key] = arg_dict[key]
        location = self._send_recv('POST', parent.url, payload)
        return self._get(target)

    def _update(self, url, payload):
        return self._send_recv('PATCH', url, payload)

    def _delete(self, url):
        return self._send_recv('DELETE', url)

    def _execute(self, url, payload):
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
        elif response.status_code == 400:
            raise BadRequestError(response)
        elif response.status_code == 404:
            raise NotFoundError(response)
        elif response.status_code == 409:
            raise AlreadyExistsError(response)
        else:
            raise ServerError(response)

    def _populate_target(self, payload, target):
        payload = payload['%s:%s' % (target.YANG_MODULE, target.YANG_CLASS)]
        if isinstance(payload, list):
            target_list = []
            for item in payload:
                target_item = target._create_sibling(item[target.YANG_KEY])
                target_item._values = item
                target_list.append(target_item)
            return target_list
        else:
            target._values = payload
        return target

