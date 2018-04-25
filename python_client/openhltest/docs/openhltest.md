<h1 id="openhltest">openhltest</h1>


<h2 id="openhltest.Openhltest">Openhltest</h2>

```python
Openhltest(self, ip_address, rest_port)
```
This module is the top level of the test hierarchy.

<h3 id="openhltest.Openhltest.sessions">sessions</h3>

```python
Openhltest.sessions(self, name=None)
```
Get the sessions object(s) from the server.

A list of test tool sessions.

Args:
 name (:obj:`str`, optional, default=None): A key value in the sessions list.

Returns:
 :obj:`list` of :obj:`Sessions` | :obj:`Sessions`: If arg name is None a list of Sessions objects otherwise a single Sessions object.

Raises:
 NotFoundError: name is not in the list of sessions objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.Openhltest.create_sessions">create_sessions</h3>

```python
Openhltest.create_sessions(self, name)
```
Create a sessions instance on the server.

A list of test tool sessions.

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`Sessions`: An object encapsulating an instance of the sessions model.

Raises:
 AlreadyExistsError: An instance of sessions with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h2 id="openhltest.Sessions">Sessions</h2>

```python
Sessions(self, parent, yang_key_value=None)
```
A list of test tool sessions.

<h3 id="openhltest.Sessions.config">config</h3>

```python
Sessions.config(self)
```
Get the config object from the server

This container aggregates all other top level configuration submodules.

Returns:
 :obj:`SessionsConfig`: An object encapsulating an instance of the config model.

Raises:
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.Sessions.statistics">statistics</h3>

```python
Sessions.statistics(self)
```
Get the statistics object from the server

The statistics pull model

Returns:
 :obj:`SessionsStatistics`: An object encapsulating an instance of the statistics model.

Raises:
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.Sessions.name">name</h3>

str: The unique name of the test tool session. Once the session has been created the name cannot be modified.
<h3 id="openhltest.Sessions.session_type">session_type</h3>

:str:`enum`: The type of test tool session. Once the session has been created the session-type cannot be modified.
Enums:
 L2L3: A layer 23 test tool session
 L4L7: A layer 47 test tool session. This is currently not supported and is a feature placeholder

<h2 id="openhltest.SessionsConfig">SessionsConfig</h2>

```python
SessionsConfig(self, parent)
```
This container aggregates all other top level configuration submodules.

<h3 id="openhltest.SessionsConfig.ports">ports</h3>

```python
SessionsConfig.ports(self, name=None)
```
Get the ports object(s) from the server.

A list of abstract test ports

Args:
 name (:obj:`str`, optional, default=None): A key value in the ports list.

Returns:
 :obj:`list` of :obj:`SessionsConfigPorts` | :obj:`SessionsConfigPorts`: If arg name is None a list of SessionsConfigPorts objects otherwise a single SessionsConfigPorts object.

Raises:
 NotFoundError: name is not in the list of ports objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.create_ports">create_ports</h3>

```python
SessionsConfig.create_ports(self, name)
```
Create a ports instance on the server.

A list of abstract test ports

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`SessionsConfigPorts`: An object encapsulating an instance of the ports model.

Raises:
 AlreadyExistsError: An instance of ports with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.protocol_groups">protocol_groups</h3>

```python
SessionsConfig.protocol_groups(self, name=None)
```
Get the protocol-groups object(s) from the server.

A list of emulated protocol groups

Args:
 name (:obj:`str`, optional, default=None): A key value in the protocol-groups list.

Returns:
 :obj:`list` of :obj:`SessionsConfigProtocolGroups` | :obj:`SessionsConfigProtocolGroups`: If arg name is None a list of SessionsConfigProtocolGroups objects otherwise a single SessionsConfigProtocolGroups object.

Raises:
 NotFoundError: name is not in the list of protocol-groups objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.create_protocol_groups">create_protocol_groups</h3>

```python
SessionsConfig.create_protocol_groups(self, name)
```
Create a protocol-groups instance on the server.

A list of emulated protocol groups

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`SessionsConfigProtocolGroups`: An object encapsulating an instance of the protocol-groups model.

Raises:
 AlreadyExistsError: An instance of protocol-groups with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.traffic_groups">traffic_groups</h3>

```python
SessionsConfig.traffic_groups(self, name=None)
```
Get the traffic-groups object(s) from the server.

A list of traffic groups

Args:
 name (:obj:`str`, optional, default=None): A key value in the traffic-groups list.

Returns:
 :obj:`list` of :obj:`SessionsConfigTrafficGroups` | :obj:`SessionsConfigTrafficGroups`: If arg name is None a list of SessionsConfigTrafficGroups objects otherwise a single SessionsConfigTrafficGroups object.

Raises:
 NotFoundError: name is not in the list of traffic-groups objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.create_traffic_groups">create_traffic_groups</h3>

```python
SessionsConfig.create_traffic_groups(self, name)
```
Create a traffic-groups instance on the server.

A list of traffic groups

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`SessionsConfigTrafficGroups`: An object encapsulating an instance of the traffic-groups model.

Raises:
 AlreadyExistsError: An instance of traffic-groups with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.connect_ports">connect_ports</h3>

```python
SessionsConfig.connect_ports(self, connect_ports_input)
```
Execute the connect-ports action on the server

Connect abstract test ports to physical hardware test ports and/or  virtual machine test ports

:return: ConnectPortsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.disconnect_ports">disconnect_ports</h3>

```python
SessionsConfig.disconnect_ports(self, disconnect_ports_input)
```
Execute the disconnect-ports action on the server

Disconnect abstract test ports from any connected physical hardware test ports and/or virtual machine test ports

:return: DisconnectPortsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.start_protocols">start_protocols</h3>

```python
SessionsConfig.start_protocols(self, start_protocols_input)
```
Execute the start-protocols action on the server

Start one or more emulated protocol groups. An empty list signifies that all protocol groups will be started.

:return: StartProtocolsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.stop_protocols">stop_protocols</h3>

```python
SessionsConfig.stop_protocols(self, stop_protocols_input)
```
Execute the stop-protocols action on the server

Stop one or more protocol groups.  An empty list signifiels that all protocol groups will be stopped.

:return: StopProtocolsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.start_traffic">start_traffic</h3>

```python
SessionsConfig.start_traffic(self, start_traffic_input)
```
Execute the start-traffic action on the server

Start one or more traffic groups. An empty list signifies that all traffic groups will be started.

:return: StartTrafficOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.stop_traffic">stop_traffic</h3>

```python
SessionsConfig.stop_traffic(self, stop_traffic_input)
```
Execute the stop-traffic action on the server

Stop one or more traffic groups.  An empty list signifies that all traffic groups will be stopped.

:return: StopTrafficOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.clear">clear</h3>

```python
SessionsConfig.clear(self)
```
Execute the clear action on the server

Clear the current configuration

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.load">load</h3>

```python
SessionsConfig.load(self, load_input)
```
Execute the load action on the server

Load a vendor specific configuration

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h2 id="openhltest.SessionsConfigPorts">SessionsConfigPorts</h2>

```python
SessionsConfigPorts(self, parent, yang_key_value=None)
```
A list of abstract test ports

<h3 id="openhltest.SessionsConfigPorts.name">name</h3>

str: The unique name of an abstract test port
<h2 id="openhltest.SessionsConfigProtocolGroups">SessionsConfigProtocolGroups</h2>

```python
SessionsConfigProtocolGroups(self, parent, yang_key_value=None)
```
A list of emulated protocol groups

<h3 id="openhltest.SessionsConfigProtocolGroups.name">name</h3>

str: The unique name of an emulated protocol group
<h2 id="openhltest.SessionsConfigTrafficGroups">SessionsConfigTrafficGroups</h2>

```python
SessionsConfigTrafficGroups(self, parent, yang_key_value=None)
```
A list of traffic groups

<h3 id="openhltest.SessionsConfigTrafficGroups.name">name</h3>

str: The unique name of a traffic group
<h2 id="openhltest.SessionsStatistics">SessionsStatistics</h2>

```python
SessionsStatistics(self, parent)
```
The statistics pull model

<h3 id="openhltest.SessionsStatistics.ports">ports</h3>

```python
SessionsStatistics.ports(self, name=None)
```
Get the ports object(s) from the server.

TBD

Args:
 name (:obj:`str`, optional, default=None): A key value in the ports list.

Returns:
 :obj:`list` of :obj:`SessionsStatisticsPorts` | :obj:`SessionsStatisticsPorts`: If arg name is None a list of SessionsStatisticsPorts objects otherwise a single SessionsStatisticsPorts object.

Raises:
 NotFoundError: name is not in the list of ports objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsStatistics.create_ports">create_ports</h3>

```python
SessionsStatistics.create_ports(self, name)
```
Create a ports instance on the server.

TBD

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`SessionsStatisticsPorts`: An object encapsulating an instance of the ports model.

Raises:
 AlreadyExistsError: An instance of ports with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsStatistics.first_activity_timestamp">first_activity_timestamp</h3>

yang:date-and-time: Timestamp of the first request to this session.
<h3 id="openhltest.SessionsStatistics.last_activity_timestamp">last_activity_timestamp</h3>

yang:date-and-time: Timestamp of the last request to this session
<h3 id="openhltest.SessionsStatistics.clear">clear</h3>

```python
SessionsStatistics.clear(self)
```
Execute the clear action on the server

Clear all statistic counters.

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h2 id="openhltest.SessionsStatisticsPorts">SessionsStatisticsPorts</h2>

```python
SessionsStatisticsPorts(self, parent, yang_key_value=None)
```
TBD

<h3 id="openhltest.SessionsStatisticsPorts.name">name</h3>

str: An abstract test port name
<h3 id="openhltest.SessionsStatisticsPorts.connected_test_port_id">connected_test_port_id</h3>

str: The id of the connected test port.  Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.connected_test_port_description">connected_test_port_description</h3>

str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.connection_state">connection_state</h3>

:str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port
Enums:
 CONNECTING: TBD
 CONNECTED_LINK_UP: TBD
 CONNECTED_LINK_DOWN: TBD
 DISCONNECTING: TBD
 DISCONNECTED: TBD

<h3 id="openhltest.SessionsStatisticsPorts.connection_state_details">connection_state_details</h3>

str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.speed">speed</h3>

str: The actual speed of the test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.tx_frames">tx_frames</h3>

str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.rx_frames">rx_frames</h3>

str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port.
<h2 id="openhltest.SessionsStatisticEventsPorts">SessionsStatisticEventsPorts</h2>

```python
SessionsStatisticEventsPorts(self, parent, yang_key_value=None)
```
TBD

<h3 id="openhltest.SessionsStatisticEventsPorts.name">name</h3>

str: An abstract test port name
<h3 id="openhltest.SessionsStatisticEventsPorts.connected_test_port_id">connected_test_port_id</h3>

str: The id of the connected test port.  Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.connected_test_port_description">connected_test_port_description</h3>

str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.connection_state">connection_state</h3>

:str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port
Enums:
 CONNECTING: TBD
 CONNECTED_LINK_UP: TBD
 CONNECTED_LINK_DOWN: TBD
 DISCONNECTING: TBD
 DISCONNECTED: TBD

<h3 id="openhltest.SessionsStatisticEventsPorts.connection_state_details">connection_state_details</h3>

str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.speed">speed</h3>

str: The actual speed of the test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.tx_frames">tx_frames</h3>

str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.rx_frames">rx_frames</h3>

str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port.
