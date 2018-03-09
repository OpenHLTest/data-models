# Vendor prototype demo - restconf requests
The following restconf requests will be considered the baseline for a vendor demonstration of the openhltest data-models prototype.

Notes
1) The restconf requests that follow are defined according to RFC 2616.
2) {{host}} is meant to be a placeholder for https://{host}:{port>}
3) Server implementations should have the options of returning a 202 Accepted response for long duration requests.  
  3.1 This will avoid client timeouts by returning a Location header url that can be polled.  
  3.2 A GET to the polling url will can return one of the two following responses:  
     3.2.1 If the request has not completed a 202 Accepted response will be returned  
	 3.2.2 If the request has completed the actual response for the original request will be returned 


### POST request
```
POST /restconf/data HTTP/1.1
Content-Type: application/json
Content-Length: <length of following payload>

{
	"openhltest-session:sessions": {
		"name": "demo",
		"session-type": "L2L3"
	}
}
```

### 202 Accepted response
```
HTTP/1.1 202 Accepted
Location: /restconf/data/accepted-status=3
```

### Polling request
```
GET /restconf/data/accepted-status=3 HTTP/1.1
```

### Polling response not complete
```
HTTP/1.1 202 Accepted
Location: /restconf/data/accepted-status=3
```

### Polling response complete
```
HTTP/1.1 201 Created
Location: /restconf/data/openhltest-session:sessions=demo
```
  
  
## 1) Create an instance of a test tool session
---
### REQUEST
```
POST {{host}}/restconf/data HTTP/1.1
Content-Type: application/json

{
	"openhltest-session:sessions": {
		"name": "demo",
		"session-type": "L2L3"
	}
}
```
### SUCCESS RESOURCE CREATED
```
HTTP/1.1 201 OK
Location: {{host}}/restconf/data/openhltest-session:sessions=demo
```
### ERROR RESOURCE ALREADY EXISTS
```
HTTP/1.1 409 Conflict
```


## 2) Load a vendor specific binary configuration
---
Normally a POST to the config node with JSON or YAML would mean creating new nodes under the parent node specified in the url.  
The ability of the server implementation to accept application/octet-stream allows a user to specify a binary config as opposed to JSON or YAML.  
This would overwrite the entire config.  
This is not specified in restconf but is meant to assist customers in transitioning from binary configurations to JSON/YAML configurations.  
### REQUEST
```
POST {{host}}/restconf/data/openhltest-session:sessions=demo/config HTTP/1.1
Content-Type: application/octet-stream

.<vendor binary config filename here>
```
### SUCCESS NO CONTENT
```
HTTP/1.1 204 No Content
```


## 3) Retrieve only read/write configuration nodes in JSON format
---
The response ports, protocol-groups and traffic-groups objects are for informational purposes only and will differ depending on the content loaded in step 2.
### REQUEST
```
GET {{host}}/restconf/data/openhltest-session:sessions=demo/config?content=config
Accept-Encoding: application/json
```
### RESPONSE
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: <length of following payload>

{
	"openhltest-session:config": {
		"ports": [
			{
				"name": "Ethernet - 001"
			}
		],
		"protocol-groups": [
			{
				"name": "Topology 1"
				"port-names": [
					"Ethernet - 001"
				]
			}
		],
		"traffic-groups": [
			{
				"name": "Traffic Item 1"
			}
		]
	}
}
```


## 4) Connect physical hardware to abstract test ports
---
The following input is informational and will differ depending on the data loaded in step 2.
It demonstrates connecting two physical test ports to named abstract ports.   
### REQUEST
```
POST {{host}}/restconf/data/openhltest-session:sessions=demo/config/connect-ports
Content-Type: application/json

{
	"input": [
		{
			"port-name": "Ethernet - 001",
			"chassis": "10.36.74.53",
			"card": 6,
			"port": 2
		},
		{
			"port-name": "Ethernet - 002",
			"chassis": "10.36.74.53",
			"card": 7,
			"port": 2
		}
	]
}
```
### RESPONSE
```
HTTP/1.1 204 No Content
```


## 5) Start all protocols
---
### REQUEST
```
POST {{host}}/restconf/data/openhltest-session:sessions=demo/config/start-protocols
Content-Type: application/json

{
	"input": []
}
```
### RESPONSE
```
HTTP/1.1 204 No Content
```


## 6) Clear all statistic counters
---
### REQUEST
```
POST {{host}}/restconf/data/openhltest-session:sessions=demo/statistics/clear-statistics
```
### RESPONSE
```
HTTP/1.1 204 No Content
```


## 7) Start all traffic
---
### REQUEST
```
POST {{host}}/restconf/data/openhltest-session:sessions=demo/config/start-traffic
Content-Type: application/json

{
	"input": []
}
```
### RESPONSE
```
HTTP/1.1 204 No Content
```


## 8) Retrieve statistics
---
### REQUEST
```
GET {{host}}/restconf/data/openhltest-session:sessions=demo/statistics?content=all
Accept-Encoding: application/json
```
### RESPONSE
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: <length of following payload>

{
	"openhltest-session-statistics": {
		"first-activity-timestamp": "",
		"last-activity-timestamp": "",
		"ports": [
			{
				"name": "Ethernet - 001",
				"connected-test-port-id": "10.36.74.53/6/2",
				"connected-test-port-description": "vendor specific port information",
				"connection-state": "CONNECTED_LINK_UP",
				"connection-state-details": "vendor specific connection information",
				"speed": "10000",
				"tx-frames": "0",
				"rx-frames": "0"
			}
		]
	}
}
```
