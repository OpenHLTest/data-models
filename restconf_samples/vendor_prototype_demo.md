# Vendor prototype demo - restconf requests
The following restconf requests will be considered the baseline for a vendor demonstration of the openhltest data-models prototype.

Notes
1) The restconf requests that follow are defined according to RFC 2616.
2) {{host}} is meant to be a placeholder for https://{host}:{port>}
3) Server implementations should have the options of returning a 202 Accepted response for long duration requests.  
  3.1 This will avoid client timeouts by returning a completion url that can be polled.  
  3.2 Once the request has completed the polling response will return the actual response for the original request. 
  3.3 This is beyond the scope of the demo and is meant to be a placeholder for further discussion.  

### 202 Accepted proposal
```
HTTP/1.1 202 Accepted
Content-Type: application/json
Content-Length: <length of following payload>

{
	"id": "3",
	"status": "IN_PROGRESS",
	"status-url": "/restconf/data/openhltest-session:session=demo/pending-requests=3",
	"execution-time-ms": 23356543,
	"result": null
}
```
### Pending request complete
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: <length of following payload>

{
	"id": "3",
	"status": "COMPLETE",
	"status-url": "/restconf/data/openhltest-session:session=demo/pending-requests=3",
	"execution-time-ms": 2335633443,
	"result": {
		<json response if any will go here>
	}
}
```
  
  
## 1) Create an instance of a test tool session
---
### REQUEST
```
POST {{host}}/restconfig/data/openhltest-session:sessions HTTP/1.1
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
Location: {{host}}/restconfig/data/openhltest-session:sessions=demo
```
### ERROR RESOURCE ALREADY EXISTS
```
HTTP/1.1 409 Conflict
```


## 2) Load a vendor specific binary configuration
---
Normally patching the config node with JSON or YAML would mean updating all nodes that already exist or creating new ones.  
The ability of the server implementation to accept application/octet-stream allows a user to specify a binary config as opposed to JSON or YAML.  
This would overwrite the entire config instead of patching/creating nodes.  
This is not specified in restconf but is meant to assist customers in transitioning from binary configurations to JSON/YAML configurations.  
### REQUEST
```
PATCH {{host}}/restconfig/data/openhltest-session:sessions=demo/config HTTP/1.1
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
