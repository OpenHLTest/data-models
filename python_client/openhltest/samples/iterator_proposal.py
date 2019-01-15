import sys
import os
path = os.path.realpath(__file__)
sys.path.insert(0, path[0:path.rfind('openhltest') + len('openhltest')])

from openhltest import *
from httptransport import HttpError
import base64
import time

openhltest = Openhltest('127.0.0.1', 443)

# all child container nodes without presence are properties
# all child list nodes and child container nodes with presence are methods
# accessing a child property returns a single object of the class
# accessing a child method returns a single object of the class with all instances from the server encapsulated within the object
# specifying named parameters in a child method reduces the possible indexes to only those named parameter matches
# the object has __iter__, __next__, __getitem__ methods to allow access to the encapsulated instances
sessions = openhltest.sessions()
sessions = openhltest.sessions(name='demo1')

# child classes that are rw yang lists have explicit add, remove methods
sessions.add(name='demo2')

# print details about the class instance
# to print out all encapsulated instances in the object iterate it
for session in sessions:
	print(session)

# accessing child classes that are yang containers without presence
# will return an object with the one and only one instance data from the server
# encapsulated in the object
# there are no add, remove methods for that object
config = sessions.config

# add, remove methods return a reference to self
# add appends instance data internally in addition to on the server
# the following adds two ports on the server and also holds the instance data locally
# if the add operation is successful

# ports @property returns an instance of Ports class
# Ports instance contains 2 internal data objects of ports node from the server
my_ports = config.ports
my_ports.add(name='Port 1', location='1.1.1.1/1/1')
my_ports.location = '1.1.1.2'
my_ports.update(location='1.1.1.2')
my_ports.add(name='Port 2', location='1.1.1.1/1/2')
my_ports = config.ports.find(location='^1.1.1.1')
my_ports.connect()

# the __len__ method will allow for determining how many instances
# are currently encapsulated by an object
print(len(my_ports))

# __getitem__ allows for access by index
# the following will print out the instance data encapsulated in the object at index 0
print(my_ports[0])

# index property allows for determining current instance
print(ports.index)

# the following will retrieve all instances of ports where name 
# starts with the word 'Port'
ports = config.ports(name='^Port')

# the following find retrieves all instances of ports
ports = config.ports()

# all objects will have an update method to allow for updating one or more
# configurable leaf nodes for the current encapsulated instance
config.traffic_groups(name='Traffic Group 1').update(mesh_type='ONE_TO_ONE', bidirectional=False)

# all objects will also allow for configurable leaf nodes to be update individually
config.traffic_groups(name='Traffic Group 1').mesh_type = 'ONE_TO_ONE'

# remove allows for deletion of some or all encapsulated instances
# remove the current encapsulated instance
ports.remove()
# access by index and remove
ports[0].remove()
# remove all encapsulated instances by iterating
for port in ports:
	port.remove()
