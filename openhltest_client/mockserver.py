"""Mock server to validate requests/responses

"""
from requests import Response
import json


class MockServer(object):
    def __init__(self):
        self._mock_storage = {}

    def _make_python_name(self, yang_name):
        camelCaseName = ''
        for piece in yang_name.split('-'):
            camelCaseName += piece[0].upper() + piece[1:]
        return camelCaseName

    def request(self, yang_class, method, url, locals_dict, payload):
        response = Response()
        if method == 'GET':
            response.status_code = 200
            response.reason = 'OK'
            response_object = {}
            response._content = json.dumps(self._get_from_mock_storage(yang_class, url), indent=4)
        elif method == 'POST' and url.split('/').pop() in yang_class.YANG_ACTIONS:
            method_name = self._make_python_name(url.split('/').pop())
            if 'Returns:' in getattr(yang_class, method_name).__doc__:
                output = getattr(yang_class, method_name).__doc__.replace('\n', '').replace('\t', '').replace(' ', '')
                start = output.find('Returns:(') + len('Returns:(')
                output = output[start:output.find(')', start)]
                output = output.replace('string', '')
                response.status_code = 200
                response.reason = 'OK'
                response._content = json.dumps({'openhltest:output': json.loads(output)}, indent=4)
            else:
                response.status_code = 204
                response.reason = 'No Content'
        elif method == 'POST':
            response.status_code = 201
            response.reason = 'Created'
            payload = json.loads(payload)
            key_value = locals_dict[self._make_python_name(yang_class.YANG_KEY)]
            response.headers['location'] = '%s/%s=%s' % (url, yang_class.YANG_NAME, key_value)
            self._mock_storage[response.headers['location']] = payload['openhltest:%s' % yang_class.YANG_NAME][0]
        elif method == 'PATCH':
            response.status_code = 204
            response.reason = 'No Content'
            self._update_mock_storage(yang_class, url, json.loads(payload))
        elif method == 'DELETE':
            response.status_code = 204
            response.reason = 'No Content'
            self._delete_from_mock_storage(url)
        return response

    def _get_from_mock_storage(self, yang_class, url):
        if yang_class.YANG_KEYWORD == 'container':
            if url not in self._mock_storage:
                self._mock_storage[url] = {}
            return { "openhltest:%s" % yang_class.YANG_NAME: self._mock_storage[url] }
        if yang_class.YANG_KEYWORD == 'list':
            key_pieces = url.split('/').pop().split('=')
            if len(key_pieces) == 2:
                return { "openhltest:%s" % yang_class.YANG_NAME: self._mock_storage[url] }
            else:
                list_content = []
                for key in self._mock_storage.keys():
                    if key[:key.rfind('=')]== url:
                        list_content.append(self._mock_storage[key])
                return { "openhltest:%s" % yang_class.YANG_NAME: list_content }

    def _update_mock_storage(self, yang_class, url, data):
        parent = url[:url.rfind('/')]
        category = 'openhltest:%s' % yang_class.YANG_NAME
        key = None
        if yang_class.YANG_KEYWORD == 'list':
            key = url[url.rfind('/'):]
            key = key[key.find('=') + 1:]
        if key is None:
            data_index = 0
        else:
            for i in range(len(self._mock_storage[parent][category])):
                if key == self._mock_storage[parent][category][i][yang_class.YANG_KEY]:
                    data_index = i
                    break
        self._mock_storage[parent][category][data_index] = data
        return None

    def _delete_from_mock_storage(self, url):
        for key in self._mock_storage.keys():
            if key.startswith(url):
                self._mock_storage.pop(key)
