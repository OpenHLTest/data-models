"""Base class for restconf transactions
"""
from openhltest_client.transport import Transport
from openhltest_client.errors import *
import json


try:
    basestring
except NameError:
    basestring = str


class Base(object):
    """Base
    
    Designed around __iter__, __next__, __getitem__
    _object_properties is a list of property dicts returned by the server
    _index is the current pointer into the _object_properties
    _properties returns the current properties as dictated by _index
    """
    def __init__(self, parent):
        if isinstance(parent, Transport):
            self._parent = None
            self._transport = parent
        else:
            self._parent = parent
            self._transport = parent._transport
        self._set_properties(None, clear=True)

    def __iter__(self):
        self._index = -1
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._index + 1 >= len(self._object_properties):
            raise StopIteration
        else:
            self._index += 1
        return self[self._index]

    def __getitem__(self, index):
        if index >= len(self._object_properties):
            raise IndexError	
        elif index < 0 and len(self._object_properties) + index in range(len(self._object_properties)):
            index = len(self._object_properties) + index
        item = self.__class__(self._parent)
        item._object_properties.append(self._object_properties[index])
        return item

    @property
    def index(self):
        """The current index of the objects that have been retrieved from the server

        Returns:
            number:
        """
        return self._index

    def __len__(self):
        """The total number of objects that have been retrieved from the server

        Returns: 
            number: 
        """
        return len(self._object_properties)

    @property
    def YangPath(self):
        """The yang path of the current resource
        
        Returns: 
            str: The yang path of the current resource

        Raises:
            ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_value('yang-path')

    @property
    def _properties(self):
        return self._object_properties[self._index]

    def _clear(self):
        self._object_properties = []
        self._index = len(self._object_properties) - 1

    def _check_arg_type(self, object_to_test, arg_type):
        if isinstance(object_to_test, arg_type) is not True:
            raise TypeError('the parameter supplied is of %s but must be of <type \'%s\'>' % (type(object_to_test), arg_type.__name__))

    def _get_value(self, name):
        """The main accessor for all attributes
        """
        try:
            return self._properties[name]
        except Exception as e:
            raise NotFoundError('The attribute %s is not in the internal list of object dicts. (%s)' % (name, e))
  
    def _set_value(self, name, value):
        """This is only called internally to set values after a successful update
        """
        try:
            if name in self.YANG_PROPERTY_MAP.values():
                self._properties[name] = value
        except Exception as e:
            raise e
        
    def __str__(self):
        """Get all the instances encapsulated by this container without changing the current index

        Returns:
            str: A string representation of the encapsulated instances
        """
        instances = ''
        for i in range(len(self)):
            properties = self._object_properties[i]
            instances += '\n%s[%s]: %s' % (self.__class__.__name__, i, properties['yang-path'])
            for key in sorted(properties.keys()):
                if key == 'yang-path':
                    continue
                property_name = '%s%s' % (key[0].upper(), key[1:])
                if property_name in self.__class__.__dict__:
                    instances += '\n\t%s: %s' % (property_name, properties[key])
        return instances.strip('\n')

    def _set_properties(self, properties, clear=False):
        if clear is True:
            self._clear()
        if properties is None:
            return
        if isinstance(properties, dict) is True:
            self._object_properties.append(properties)
        else:
            for item in properties:
                self._object_properties.append(item)
        self._index = len(self._object_properties) - 1
 
    def _build_relative_url(self, start, key_value):
        relative_url = start
        if relative_url is None:
            relative_url = ''
        if key_value is not None:
            relative_url = '%s=%s' % (relative_url, key_value)
        parent = self._parent
        while isinstance(parent, Base):
            if parent.YANG_KEYWORD == 'module':
                break
            parent_path = parent.YANG_NAME
            if parent.YANG_KEY is not None:
                parent_path = '%s=%s' % (parent.YANG_NAME, parent._get_value(parent.YANG_KEY))
            if len(relative_url) == 0:
                relative_url = parent_path
            else:
                relative_url = '%s/%s' % (parent_path, relative_url)
            parent = parent._parent
        return relative_url

    def _create(self, locals_dict):
        relative_url = self._build_relative_url(None, None)
        response = self._transport._create(yang=self.__class__, url=relative_url, locals_dict=locals_dict)
        self._set_properties(response)
        return self

    def _read(self, key_value=None):
        relative_url = self._build_relative_url(self.YANG_NAME, key_value)
        response = self._transport._read(yang=self.__class__, url=relative_url)
        self._set_properties(response, clear=True)
        return self

    def _update(self, locals_dict):
        if self.YANG_KEY is not None:
            relative_url = self._build_relative_url(self.YANG_NAME, self._get_value(self.YANG_KEY))
        else:
            relative_url = self._build_relative_url(self.YANG_NAME, None)
        self._transport._update(yang=self.__class__, url=relative_url, locals_dict=locals_dict)
        for key in locals_dict.keys():
            self._set_value(key, locals_dict[key])
        return self
    
    def _delete(self):
        for i in range(len(self)):
            key = self._object_properties[i][self.YANG_KEY]
            relative_url = self._build_relative_url(self.YANG_NAME, key)
            self._transport._delete(yang=self.__class__, url=relative_url)
        self._clear()

    def _execute(self, operation, payload=None):
        if self.YANG_KEY is not None:
            relative_url = self._build_relative_url(self.YANG_NAME, self._get_value(self.YANG_KEY))
        else:
            relative_url = self._build_relative_url(self.YANG_NAME, None)
        relative_url = '%s/%s' % (relative_url, operation)
        return self._transport._execute(yang=self.__class__, url=relative_url, locals_dict=payload)


