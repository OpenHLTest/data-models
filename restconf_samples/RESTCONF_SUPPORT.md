# RESTCONF SUPPORT
This is a synopsis of the minimum required RESTCONF method requests and responses that will be initially supported by the OpenHLTest working group members.
For additional information review the full [RESTCONF RFC](https://tools.ietf.org/html/rfc8040).  

#### Samples
Sample RESTCONF reqeusts are provided in RFC2616 format specific to the [vscode REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).
For samples of RESTCONF requests see the following:
* [manage test tool sessions](./session.rest) by listing, creating and deleting them
* [load a test tool configuration](./config.rest) into a session
* [execute actions](./actions.rest) on a test tool configuration
* [retrieve statistics](./statistics.rest) from a test tool session

#### Data Resource Identifiers
1) A RESTCONF data resource identifier is encoded from left to right, starting with the top-level data node, according to the "api-path" rule in Section 3.5.3.1.  
2) The node name of each ancestor of the target resource node is encoded in order, ending with the node name for the target resource.  
3) If a node in the path is defined in a module other than its parent node or its parent is the datastore, then the module name followed by a colon character (":") MUST be prepended to the node name in the resource identifier.
```
restconf/data/openhltest-session:sessions=regression-1/config
| dataStore  | moduleName       | id     | keyValue   | id   |
```

# Resource retrieval support
#### GET Request
1) The RESTCONF server MUST support the GET method.    
2) The request MUST contain a request URI that contains at least the root resource.
3) Supported Accept-Encoding mime types are application/json, application/yaml.

#### GET Response
1) A server MAY return a "404 Not Found" status-line, as described in Section 6.5.4 in [RFC7231]. 
2) If the target resource of a retrieval request is for an operation resource, then a "405 Method Not Allowed" status-line MUST be returned by the server.

#### Examples
```
GET {{host}}/restconf/data/openhltest-session:session=regression-1/config?content=all

GET {{host}}/restconf/data/openhltest-session:session=regression-1/config/ports?depth=1
```

# Resource creation support
#### POST Request
1) If the target resource type is a datastore or data resource, then the POST is treated as a request to create a top-level resource or child resource, respectively.  
2) The message-body is expected to contain the content of a child resource to create within the parent (target resource).  
3) The message-body MUST contain exactly one instance of the expected data resource.  The data model for the child tree is the subtree, as defined by YANG for the child resource.

#### POST Response
1) If the POST method succeeds, a "201 Created" status-line is returned and there is no response message-body. A "Location" header field identifying the child resource that was created MUST be present in the response in this case.
2) If the data resource already exists, then the POST request MUST fail and a "409 Conflict" status-line MUST be returned.  

#### Examples
```
### create child port resources
POST {{host}}/restconf/data/opehltest-session:sessions=regression-1
Content-Type: application/json

{
	"config": {
		"ports": [
			{
				"name": "PE-2/6"
			},
			{
				"name": "PE-2/7"
			}
		]
	}	
}

### create a port resource
POST {{host}}/restconf/data/opehltest-session:sessions=regression-1/config
Content-Type: application/json

{
	"ports": [
		{
			"name": "PE-2/6"
		}
	]
}
```

# Action support
#### POST Request
1) Data-model-specific operations defined with the YANG "action" can be invoked with the POST method.
2) The "action" statement is used to define an operation connected to a specific container or list data node.
3) An "action" is invoked as POST {+restconf}/data/<data-resource-identifier>/<action>
#### POST Response
1) If the POST request succeeds, a "200 OK" status-line is returned if there is a response message-body, and a "204 No Content" status-line is returned if there is no response message-body.
2) If the user is not authorized to invoke the target operation, an error response containing a "403 Forbidden" status-line SHOULD be returned.
3) A server MAY return a "404 Not Found" status-line, as described in Section 6.5.4 in [RFC7231].
#### Examples
```
### start all protocols
POST {{host}}/restconf/data/openhltest-session:session=regression-1/config/start-protocols
Content-Type: application/json

{
	"input": []
}

### clear all statistic counters
POST {{host}}/restconf/data/openhltest-session:session=regression-1/statistics/clear-statistics
```

# Resource update support
#### PATCH Request
1) The plain patch mechanism merges the contents of the message-body with the target resource.  
2) The message-body for a plain patch MUST be present and MUST be represented by the media type "application/json" or "application/yaml".
3) Plain patch can be used to ONLY create/update, but not delete, a child resource within the target resource. 
4) If the target resource represents a YANG list instance, then the key leaf values, in message-body representation, MUST be the same as the key leaf values in the request URI.
5) The PATCH method MUST NOT be used to change the key leaf values for a data resource instance.
#### PATCH Response
1) If the target resource instance does not exist, the server MUST NOT create it. 
2) If the PATCH request succeeds, a "200 OK" status-line is returned if there is a message-body, and "204 No Content" is returned if no response message-body is sent.

# Resource removal support
#### DELETE Request
1) The RESTCONF server MUST support the DELETE method.  
2) The DELETE method is used to delete the target resource.  
3) If the target resource represents a configuration leaf-list or list data node, then it MUST represent a single YANG leaf-list or list instance.  
4) The server MUST NOT use the DELETE method to delete more than one such instance.
#### DELETE Response
1) If the DELETE request succeeds, a "204 No Content" status-line is returned.
2) If the user is not authorized to delete the target resource, then an error response containing a "403 Forbidden" status-line SHOULD be returned.  
3) A server MAY return a "404 Not Found" status-line and the error-tag value "invalid-value" is returned in this case.


