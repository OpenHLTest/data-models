# Python client auto generated from OpenHlTest yang models
The intent of this folder is to act as a repository for the OpenHlTest python client module.

## Straw man proposal
```python
import OpenHlTest

# create the top level datastore object, internally creates the http transport
openhltest = OpenHlTest('127.0.0.1', port=443)

# create a session (yang rw list)
session = openhltest.sessions_create(name='demo',  session_type = 'L2L3')

# get the config (yang container), needs a refresh
config = session.config
config.update(description='test')

# get a port (yang rw list)
port = config.ports_get('Ethernet - 001')
print(port.name)

# get a list of ports (yang rw list)
for port in config.ports_get():
	print(port.name)

# create a port
# key is mandatory
# named args for the remainder of params
port = config.ports_create('Ethernet - 002',  description='abc')

# update a port, named args / json object / dict?
port.update(description='xyz')

# delete a port, uses the internal restconf_path
port.delete()

# execute an action, optionally produce a connect_ports_input class
config.connect_ports([{name: 'Ethernet - 001', chassis: '1.1.1.1', card: 1, port: 1}])


# print the restconf of the object, informational, used internally
print(port.restconf_path) -> 'openhltest-session:sessions=demo/config/ports=Ethernet - 001'
```

