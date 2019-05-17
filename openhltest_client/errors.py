""" Common restconf error classes

All 400 and above responses MUST adhere to the following payload response structure:
{
	"ietf-restconf:errors" : {
		"error" : [
			{
				"error-type" : "transport|rpc|protocol|application",
				"error-tag" : "see table below",
				"error-message" : "vendor supplied message"
			}
		]
	}
}

+-------------------------+------------------+
| error-tag               | status code      |
+-------------------------+------------------+
| in-use                  | 409              |
| invalid-value           | 400, 404, or 406 |
| (request) too-big       | 413              |
| (response) too-big      | 400              |
| missing-attribute       | 400              |
| bad-attribute           | 400              |
| unknown-attribute       | 400              |
| bad-element             | 400              |
| unknown-element         | 400              |
| unknown-namespace       | 400              |
| access-denied           | 401 or 403       |
| lock-denied             | 409              |
| resource-denied         | 409              |
| rollback-failed         | 500              |
| data-exists             | 409              |
| data-missing            | 409              |
| operation-not-supported | 405 or 501       |
| operation-failed        | 412 or 500       |
| partial-operation       | 500              |
| malformed-message       | 400              |
+-------------------------+------------------+
"""
from requests import Response


class OpenHLTestError(Exception):
    """The base error class for all OpenHLTest errors"""
    def __init__(self, response):
        self._errors = response.json()['ietf-restconf:errors']['error']
        self._status_code = response.status_code
        self._reason = response.reason
        self.__iter__()

    def __iter__(self):
        self._index = -1
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._index + 1 >= len(self._errors):
            raise StopIteration
        else:
            self._index += 1
        return self[self._index]
    
    def __len__(self):
        """The total number of objects that have been retrieved from the server

        Returns: 
            number: 
        """
        return len(self._errors)

    def __getitem__(self, index):
        if index >= len(self._errors):
            raise IndexError	
        elif index < 0 and len(self._errors) + index in range(len(self._errors)):
            index = len(self._errors) + index
        item = self.__class__(self._parent)
        item._errors.append(self.errors[index])
        return item

    def __str__(self):
        """Get all the instances encapsulated by this container without changing the current index

        Returns:
            str: A string representation of the encapsulated instances
        """
        instances = ''
        for i in range(len(self)):
            properties = self._errors[i]
            instances += '%s: %s %s\n' % (self.__class__.__name__, self.StatusCode, self.Reason)
            instances += '\t%s %s: %s\n' % (properties['error-type'], properties['error-tag'], properties['error-message'])
        return instances.strip('\n')

    @property
    def Reason(self):
        return self._reason

    @property
    def StatusCode(self):
        return self._status_code
    
    @property
    def ErrorType(self):
        return self._errors[self._index]['error-type']

    @property
    def ErrorTag(self):
        return self._errors[self._index]['error-tag']

    @property
    def ErrorMessage(self):
        return self._errors[self._index]['error-message']


class UnauthorizedError(OpenHLTestError):
    """Access is unauthorized

    Authorization has not been successfully completed.
    """
    def __init__(self, response):
        super(UnauthorizedError, self).__init__(response)


class AlreadyExistsError(OpenHLTestError):
    """The requested resource already exists on the server"""
    def __init__(self, response):
        super(AlreadyExistsError, self).__init__(response)


class BadRequestError(OpenHLTestError):
    """The server has determined that the request is incorrect"""
    def __init__(self, response):
        super(BadRequestError, self).__init__(response)


class NotFoundError(OpenHLTestError):
    """The requested resource does not exist on the server"""
    def __init__(self, response):
        super(NotFoundError, self).__init__(response)


class ServerError(OpenHLTestError):
    """The server has encountered an uncategorized error condition"""
    def __init__(self, response):
        super(ServerError, self).__init__(response)
