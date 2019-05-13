"""Http transport class with CRUDX implementations of Transport methods
"""
import sys
import json
from requests import Session, Response
from openhltest_client.transport import Transport
from openhltest_client.mockserver import MockServer
from openhltest_client.base import Base
from openhltest_client.errors import *


class HttpTransport(Transport):

    def __init__(self, openhltest_server=None, api_key=None, log_file_name=None):
        """RestConf style transport

        Args:
            openhltest_server (str): ipaddress/hostname:port, if port is not specified then it will default to 443, default scheme is https
            api_key (str): optional api key to be used by the vendor implementation for authorization
            log_file_name (str): optional name of logger logfile, default is stdio
        """
        super(HttpTransport, self).__init__(log_file_name)

        if sys.version_info.major == 2 and sys.version_info.minor == 7 and sys.version_info.micro < 9:
            requests.packages.urllib3.disable_warnings()
        else:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self._openhltest_server = openhltest_server
        self._verify_cert = False
        self._ignore_env_proxy = False
        self._api_key = None
        if openhltest_server is None:
            self._session = MockServer()
            self._base_data_url = 'https://<ipaddress:port>/restconf/data'
            self._base_operations_url = 'https://<ipaddress:port>/restconf/operations'
        else:
            self._session = Session()
            self._base_data_url = 'https://%s/restconf/data' % (self._openhltest_server)
            self._base_operations_url = 'https://%s/restconf/operations' % (self._openhltest_server)

    @property
    def OpenHlTest(self):
        from openhltest_client.openhltest.openhltest import Openhltest
        return Openhltest(self)

    @property
    def ignore_env_proxy(self):
        return self._ignore_env_proxy
    @ignore_env_proxy.setter
    def ignore_env_proxy(self, value):
        self._ignore_env_proxy = value
        if self._ignore_env_proxy is True:
            self._session.proxies.update({
                'http': None,
                'https': None
            })

    @property
    def api_key(self):
        return self._api_key
    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def _build_payload(self, yang_class, locals_dict, method):
        payload = {}
        for key in locals_dict.keys():
            if key in yang_class.YANG_PROPERTY_MAP:
                value = locals_dict[key]
                if isinstance(value, Base):
                    for dependency_key in value.YANG_PROPERTY_MAP:
                        if value.YANG_PROPERTY_MAP[dependency_key] == value.YANG_KEY:
                            key_attr_name = dependency_key
                    value = []
                    for base_obj in locals_dict[key]:
                        value.append(getattr(base_obj, key_attr_name))   
                payload[yang_class.YANG_PROPERTY_MAP[key]] = value
        if method.lower() == 'post':
            return { 'openhltest:%s' % yang_class.YANG_NAME: [payload] }
        elif method.lower() == 'patch':
            return payload
        else:
            return { 'openhltest:%s' % yang_class.YANG_NAME: payload }

    def _normalize_payload(self, payload):
        for key in payload.keys():
            value = payload[key]
            if isinstance(value, Base):
                base_values = []
                for base_obj in value:
                    base_values.append(base_obj._get_value(base_obj.YANG_KEY))   
                payload[key] = base_values
            elif isinstance(value, dict):
                self._normalize_payload(payload[key])

    def _send_recv(self, yang_class, method, url, locals_dict=None):
        """Uses requests to send an http request

        Returns:
            200 - (dict | list): depends on the request
            201 - (str): the url of the new resource
            204 - (None): no content is returned
        """
        headers = {}
        if self._api_key is not None:
            headers['x-api-key'] = self._api_key
        payload = None
        if locals_dict is not None:
            headers['content-type'] = 'application/json'
            if method == 'POST' and url.split('/').pop() != yang_class.YANG_NAME:
                self._normalize_payload(locals_dict)
                payload = json.dumps({'openhltest:input': locals_dict}, indent=4)
            else:
                payload = json.dumps(self._build_payload(yang_class, locals_dict, method), indent=4)

        self._log_request(method, url, headers, payload)
        if self._openhltest_server is None:
            response = self._session.request(yang_class, method, url, locals_dict, payload)
        else:
            response = self._session.request(method, url, headers=headers, data=payload, verify=self._verify_cert)
        self._log_response(response)

        if response.status_code == 200 and method == 'POST' and url.split('/').pop() != yang_class.YANG_NAME:
            return json.loads(response.content)['openhltest:output']
        elif response.status_code == 200 and '/restconf/data' in url:
            return json.loads(response.content)['openhltest:%s' % yang_class.YANG_NAME]
        elif response.status_code == 201:
            return response.headers['location']
        elif response.status_code == 204:
            return None
        elif response.status_code == 400:
            raise BadRequestError(response)
        elif response.status_code == 401:
            raise UnauthorizedError(response)
        elif response.status_code == 404:
            raise NotFoundError(response)
        else:
            raise ServerError(response)

    def _log_request(self, method, url, headers, payload):
        message = '%s %s' % (method, url)
        for key in headers.keys():
           message += '\n%s: %s' % (key, headers[key])
        if payload is not None:
            message += '\n%s' % payload
        self.debug(message)

    def _log_response(self, response):
        message = '%s %s' % (response.status_code, response.reason)
        for key in response.headers.keys():
            message += '\n%s: %s' % (key, response.headers[key])
        if response.content is not None:
            message += '\n%s' % response.content
        self.debug(message)

    def _make_data_url(self, relative_url):
        if len(relative_url) > 0:
            return '%s/openhltest:%s' % (self._base_data_url, relative_url)
        else:
            return self._base_data_url

    def _make_operations_url(self, relative_url):
        if len(relative_url) > 0:
            return '%s/openhltest:%s' % (self._base_operations_url, relative_url)
        else:
            return self._base_operations_url

    def _create(self, **kwargs):
        """Create a new resource on the server

        Args:
            yang (class): the yang class making the request
            url (str): a relative resource based path including keys
            payload (dict): a dictionary of name/values to be set on the new resource being created
        """
        new_resource_url = self._send_recv(kwargs['yang'], 'POST', self._make_data_url(kwargs['url']), locals_dict=kwargs['locals_dict'])
        content_object = self._send_recv(kwargs['yang'], 'GET', new_resource_url)
        content_object['yang-path'] = '%s/%s=%s' % (kwargs['url'], kwargs['yang'].YANG_NAME, content_object[kwargs['yang'].YANG_KEY])
        return content_object
    
    def _read(self, **kwargs):
        """Read a resource from the server

        Args:
            yang (class): the yang class making the request
            url (str): a relative resource based path, nodes that are a keyed list must be include a key value
        """
        yang_class = kwargs['yang']
        content_object = self._send_recv(yang_class, 'GET', self._make_data_url(kwargs['url']))
        if isinstance(content_object, dict):
            content_object['yang-path'] = kwargs['url']
        else:
            for item in content_object:
                item['yang-path'] = '%s=%s' % (kwargs['url'], item[yang_class.YANG_KEY])
        return content_object

    def _update(self, **kwargs):
        """Update an existing resource on the server

        Args:
            yang (class): the yang class making the request
            url (str): a relative resource based path including keys
            payload (dict): a dictionary of name/values to be set on the existing resource
        """
        return self._send_recv(kwargs['yang'], 'PATCH', self._make_data_url(kwargs['url']), locals_dict=kwargs['locals_dict'])
    
    def _delete(self, **kwargs):
        """Delete a resource on the server

        Args:
            yang (class): the yang class making the request
            url (str): a relative resource based path including keys
        """
        return self._send_recv(kwargs['yang'], 'DELETE', self._make_data_url(kwargs['url']))
    
    def _execute(self, **kwargs):
        """Execute an operation on the server
        Args:
            yang (class): the yang class making the request
            url (str): a relative resource based path including keys
            payload (dict): a dictionary of name/values to be set on the existing resource
        """
        return self._send_recv(kwargs['yang'], 'POST', self._make_data_url(kwargs['url']), locals_dict=kwargs['locals_dict'])
