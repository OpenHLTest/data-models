# Sample action restconf requests
The following requests demonstrate how to connect hardware and/or virtual test ports to abstract ports.
Once those are connected protocols can be started, statistics cleared and traffic started.

All of these are actions defined in the openhltest data model.

The samples assume that a test tool session exists at the resource location of openhltest-session:session=regression-1.

#### Connect physical hardware to abstract test ports
```
POST {{host}}/restconf/data/openhltest-session:session=regression-1/config/connect-ports
Content-Type: application/json

{
	"input": [
		{
			"port-name": "PE-1/1",
			"chassis": "10.36.74.53",
			"card": 6,
			"port": 2
		},
		{
			"port-name": "PE-1/2",
			"chassis": "10.36.74.53",
			"card": 7,
			"port": 2
		}
	]
}
```

#### Start all protocols
```
POST {{host}}/restconf/data/openhltest-session:session=regression-1/config/start-protocols
Content-Type: application/json

{
	"input": []
}
```

#### Clear all statistic counters
```
POST {{host}}/restconf/data/openhltest-session:session=regression-1/statistics/clear-statistics
```

#### Start all traffic
```
POST {{host}}/restconf/data/openhltest-session:session=regression-1/config/start-traffic
Content-Type: application/json

{
	"input": []
}
```
