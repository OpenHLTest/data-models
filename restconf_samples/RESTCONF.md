
# If the POST method succeeds, a "201 Created" status-line is returned
#    and there is no response message-body.  A "Location" header field
#    identifying the child resource that was created MUST be present in
#    the response in this case.
# If the data resource already exists, then the POST request MUST fail
#    and a "409 Conflict" status-line MUST be returned.  The error-tag
#    value "resource-denied" is used in this case.




# If the DELETE request
#    succeeds, a "204 No Content" status-line is returned.

# If the user is not authorized to delete the target resource, then an
#    error response containing a "403 Forbidden" status-line SHOULD be
#    returned.  The error-tag value "access-denied" is returned in this
#    case.  
# A server MAY return a "404 Not Found" status-line and 
#   the error-tag value "invalid-value" is returned in this case


