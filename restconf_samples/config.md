### get the entire config for a specific session
### accept-encoding support: 
### 	application/json - returns the config data in json format
### 	application/yaml - returns the config data in yaml format
### 	application/octet-stream - returns the entire config in vendor specific binary format
GET {{host}}/restconf/data/openhltest-session:sessions=regression-1/config?content=all
Accept-Encoding: application/json


### load a vendor specific binary config
### content type support: application/octet-stream
PATCH {{host}}/restconf/data/openhltest-session:sessions=regression-1/config
Content-Type: application/octet-stream

.<vendor binary config filename here>


### load an OpenHLTest config in a specific session
### content-type support: application/json; application/yaml
POST {{host}}/restconf/data/openhltest-session:session=regression-1
Content-Type: application/json

{
	"openhltest-config": {
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