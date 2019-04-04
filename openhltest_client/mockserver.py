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
        elif method == 'POST' and '/restconf/operations' in url:
            method_name = self._make_python_name(url.split('/').pop())
            if 'Returns:' in getattr(yang_class, method_name).__doc__:
                response.status_code = 200
                response.reason = 'OK'
                response._content = json.dumps({'openhltest:output': {}}, indent=4)
            else:
                response.status_code = 204
                response.reason = 'No Content'
        elif method == 'POST' and '/restconf/data' in url:
            response.status_code = 201
            response.reason = 'Created'
            key_value = locals_dict[yang_class.YANG_KEY[0].upper() + yang_class.YANG_KEY[1:]]
            if url.find('/restconf/data/openhltest:') == -1:
                response.headers['location'] = '%s/openhltest:%s=%s' % (url, yang_class.YANG_NAME, key_value)
            else:
                response.headers['location'] = '%s/%s=%s' % (url, yang_class.YANG_NAME, key_value)
            self._add_to_mock_storage(yang_class, response.headers['location'], json.loads(payload))
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
        parent = url[:url.rfind('/')]
        category = 'openhltest:%s' % yang_class.YANG_NAME
        if yang_class.YANG_KEYWORD == 'container':
            key = yang_class.YANG_NAME
            if parent not in self._mock_storage:
                self._mock_storage[parent] = {}
                self._mock_storage[parent][category] = []
                mock_object = {}
                for name in yang_class.YANG_PROPERTY_MAP.values():
                    mock_object[name] = None
                self._mock_storage[parent][category].append(mock_object)
            content = {
                category: self._get_item_from_mock_storage(yang_class, parent, category)
            }
            return content            
        elif '=' in url[url.rfind('/'):]:
            # this is asking for one list item
            key = url[url.rfind('/'):]
            key = key[key.find('=') + 1:]
            content = {
                category: self._get_item_from_mock_storage(yang_class, parent, category, key)
            }
            return content
        else:
            # this is asking for the entire list
            parent = url[:url.rfind('/')]
            category = 'openhltest:%s' % yang_class.YANG_NAME
            content = {
                category: []
            }
            for item in self._mock_storage[parent][category]:
                content[category].append(item)
            return content
    
    def _get_item_from_mock_storage(self, yang_class, parent, category, key=None):
        item_list = self._mock_storage[parent][category]
        if key is not None:
            for item in item_list:
                if key == item[yang_class.YANG_KEY]:
                    return item
        else:
            return self._mock_storage[parent][category][0]

    def _add_to_mock_storage(self, yang_class, url, data):
        """Adds a list item to the mock storage
        """
        parent = url[:url.rfind('/')]
        category = 'openhltest:%s' % yang_class.YANG_NAME
        key = data[category][0][yang_class.YANG_KEY]
        if parent not in self._mock_storage:
            self._mock_storage[parent] = {}
        if category not in self._mock_storage[parent]:
            self._mock_storage[parent][category] = []
        self._mock_storage[parent][category].append(data[category][0])

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
