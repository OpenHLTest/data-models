from requests import Response


    #  +---- errors
    #        +---- error*
    #           +---- error-type       enumeration
    #           +---- error-tag        string
    #           +---- error-app-tag?   string
    #           +---- error-path?      instance-identifier
    #           +---- error-message?   string
    #           +---- error-info?
	#
	# all 400 and above responses MUST return the following payload structure:
	# {
    #     "ietf-restconf:errors" : {
    #       "error" : [
    #         {
    #           "error-type" : "protocol",
    #           "error-tag" : "lock-denied",
    #           "error-message" : "Lock failed; lock already held"
    #         }
    #       ]
    #     }
    #   }


class OpenHLTest(Exception):
    """The base error class for all OpenHLTest errors"""
    def __init__(self, response):
        if isinstance(response, Response):
            if response.status_code == 202:
                self._url = response.url
                async_status = response.json()
                self._status_code = async_status["state"]
                self._reason = async_status["message"]
                self._text = async_status["result"]
            else:
                self._url = response.url
                self._status_code = response.status_code
                self._reason = response.reason
                self._text = response.text
            self._message = '%s => %s %s %s' % (self._url, self._status_code, self._reason, self._text)
        else:
            self._message = response

    @property
    def message(self):
        return self._message

    @property
    def status_code(self):
        return self._status_code
        
    def __str__(self):
        return self.message


class UnauthorizedError(OpenHLTest):
    """Access is unauthorized

	Authorization has not been successfully completed.
	"""
    def __init__(self, response):
        super(UnauthorizedError, self).__init__(response)


class AlreadyExistsError(OpenHLTest):
    """The requested resource already exists on the server"""
    def __init__(self, response):
        super(AlreadyExistsError, self).__init__(response)


class BadRequestError(OpenHLTest):
    """The server has determined that the request is incorrect"""
    def __init__(self, response):
        super(BadRequestError, self).__init__(response)


class NotFoundError(OpenHLTest):
    """The requested resource does not exist on the server"""
    def __init__(self, response):
        super(NotFoundError, self).__init__(response)


class ServerError(OpenHLTest):
    """The server has encountered an uncategorized error condition"""
    def __init__(self, response):
        super(ServerError, self).__init__(response)
