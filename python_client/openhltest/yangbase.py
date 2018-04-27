"""Base class that encapsulates CRUDX methods and property access
"""
from httptransport import HttpTransport

class YangBase(object):
    def __init__(self, parent, yang_key_value):
        """Base class that encapsulates CRUDX methods and property access
        
            Args:
                parent (HttpTransport | YangBase): Openhltest object will pass in an HttpTransport while 
                    all other objects should pass in self.
                yang_key_value (str | None): If the corresponding model is a rw list container then this 
                    will be the key value for a specific object or None for all objects
        """
        self._values = {}
        self._dirty = []

        if isinstance(parent, HttpTransport) is True:
            self._http_transport = parent
            self._rest_path = '/restconf/data'
        elif isinstance(parent, YangBase):
            self._http_transport = parent._http_transport
            module = self.YANG_MODULE
            self._rest_path = parent.url
            if self._rest_path.endswith('/') is False:
                self._rest_path += '/'
            if (self.YANG_MODULE in self._rest_path) is False:
                self._rest_path += self.YANG_MODULE + ':'
            self._rest_path += self.YANG_CLASS
            if yang_key_value is not None:
                self._rest_path = '%s=%s' % (self._rest_path, yang_key_value)
            
    @property
    def url(self):
        """str: The rest url for this object"""
        return self._rest_path

    def dump(self):
        """Output this object's rest url and property values"""
        print('object: %s' % self.url)
        for key in self._values.keys():
            print('\t%s: %s' %(key, self._values[key]))

    def refresh(self):
        """Get all properties for this object"""
        self._read(self)

    def _get_value(self, key):
        if key in self._values.keys():
            return self._values[key]
        else:
            return None

    def _set_value(self, key, value):
        self._values[key] = value
        self._dirty.append(key)

    def _create(self, target, payload):
        '''Create an instance of the target nested under this instance'''
        return self._http_transport._create(self, target, payload)

    def _read(self, target):
        '''Get and populate the target object'''
        self._dirty = []
        return self._http_transport._get(target)

    def _create_sibling(self, yang_key_value):
        sibling = self.__class__(self, None)
        sibling._rest_path = '%s=%s' % (self._rest_path, yang_key_value)
        return sibling

    def _update(self):
        '''Update the object with any values that are dirty.'''
        payload = {}
        for property_name in self._dirty:
            payload[property_name] = getattr(self, property_name)
        self._dirty = []
        return self._http_transport._update(self.url, payload=payload)
    
    def _delete(self):
        '''Delete the current object'''
        return self._http_transport._delete(self.url)
    
    def _execute(self, url, input_object, output_object=None):
        payload = YangInputEncoder().encode(input_object)
        response = self._http_transport._execute(url, payload)
        if response is not None and output_object is not None:
            return self._yang_output_decoder(response, output_object)
        else:
            return response

    def _yang_output_decoder(self, response, yang_output):
        '''Takes a dict response and populates a generated yang output object'''
        self._yang_decode(response[yang_output.YANG_PATH], yang_output)
        return yang_output

    def _yang_decode(self, response, yang_output):
        for key in response.keys():
            if isinstance(response[key], list):
                yang_list = getattr(yang_output, key)
                for item in response[key]:
                    yang_object = getattr(yang_output, '%s%s' % (key[0].upper(), key[1:]))()
                    self._yang_decode(item, yang_object)
                    yang_list.append(yang_object)
            elif isinstance(response[key], dict):
                self._yang_decode(response[key], getattr(yang_output, key))
            else:
                setattr(yang_output, key.replace('-', '_'), response[key])


from json import JSONEncoder

class YangInputEncoder(JSONEncoder):
    '''Encodes python objects back into json dicts'''
    def default(self, o):
        yang_input = {
            o.YANG_PATH: self._yang_encode(o)
        }
        return yang_input

    def _yang_encode(self, o):
        if hasattr(o, '__dict__') is True:
            yang_dict = {}
            for property_name in vars(o):
                if property_name.startswith('__') or property_name == 'YANG_PATH':
                    continue
                yang_property = property_name.replace('_', '-')
                value = getattr(o, property_name)
                if hasattr(value, '__dict__') is True:
                    yang_dict[yang_property] = self._yang_encode(value)
                elif isinstance(value, list):
                    items = []
                    for item in value:
                        items.append(self._yang_encode(item))
                    yang_dict[yang_property] = items
                elif isinstance(value, bytes):
                    yang_dict[yang_property] = value.decode('utf-8')
                else:
                    yang_dict[yang_property] = value
            return yang_dict
        elif isinstance(o, list):
            items = []
            for item in o:
                items.append(self._yang_encode(item))
            return items
        else:
            return o

