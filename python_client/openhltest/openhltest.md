<h1 id="openhltest">openhltest</h1>


<h2 id="openhltest.SessionsStatisticEventsPorts">SessionsStatisticEventsPorts</h2>

```python
SessionsStatisticEventsPorts(self, parent, yang_key_value=None)
```
TBD

<h3 id="openhltest.SessionsStatisticEventsPorts.connected_test_port_id">connected_test_port_id</h3>

str: The id of the connected test port.  Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.connection_state_details">connection_state_details</h3>

str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.name">name</h3>

str: An abstract test port name
<h3 id="openhltest.SessionsStatisticEventsPorts.connection_state">connection_state</h3>

:str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port
Enums:
 CONNECTING: TBD
 CONNECTED_LINK_UP: TBD
 CONNECTED_LINK_DOWN: TBD
 DISCONNECTING: TBD
 DISCONNECTED: TBD

<h3 id="openhltest.SessionsStatisticEventsPorts.connected_test_port_description">connected_test_port_description</h3>

str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.rx_frames">rx_frames</h3>

str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.speed">speed</h3>

str: The actual speed of the test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticEventsPorts.tx_frames">tx_frames</h3>

str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port.
<h2 id="openhltest.SessionsConfigPhysicalLayersTenGigLan">SessionsConfigPhysicalLayersTenGigLan</h2>

```python
SessionsConfigPhysicalLayersTenGigLan(self, parent)
```
The conditional container for detailed ten gig  lan physical layer information

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.ignore_link_status">ignore_link_status</h3>

bool: Allow the port to continue transmitting traffic if the link(s) with its peer port(s) goes down
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.flow_control_directed_address">flow_control_directed_address</h3>

str: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.auto_mdix">auto_mdix</h3>

bool: Detect if the connection would require a crossover, and automatically chooses  the MDI or MDI-X configuration to properly match the other end of the link
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.autonegotiate">autonegotiate</h3>

bool: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.forward_error_correction">forward_error_correction</h3>

bool: Enable message encoding to control data transmission errors.
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.ppm">ppm</h3>

int32: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.lasi_monitoring_enabled">lasi_monitoring_enabled</h3>

bool: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.speed">speed</h3>

:str:`enum`: TBD
Enums:
 TEN_M: TBD
 ONE_HUNDRED_M: TBD
 ONE_G: TBD
 TWO_G: TBD
 THREE_G: TBD
 FOUR_G: TBD
 FIVE_G: TBD
 SIX_G: TBD
 SEVEN_G: TBD
 EIGHT_G: TBD
 NINE_G: TBD
 TEN_G: TBD
 TWENTY_G: TBD
 TWENTY_FIVE_G: TBD
 THIRTY_G: TBD
 FORTY_G: TBD
 FIFTY_G: TBD
 HUNDRED_G: TBD
 FOUR_HUNDRED_G: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.loopback">loopback</h3>

:str:`enum`: TBD
Enums:
 NORMAL: TBD
 LOOPBACK: TBD
 MONITOR: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.media">media</h3>

:str:`enum`: TBD
Enums:
 COPPER: TBD
 FIBER: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.forward_error_correction_mode">forward_error_correction_mode</h3>

:str:`enum`: TBD
Enums:
 NONE: TBD
 RS_FEC: TBD
 KR_FEC: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.autonegotiate_masterslave">autonegotiate_masterslave</h3>

:str:`enum`: TBD
Enums:
 MASTER: TBD
 SLAVE: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.flow_control">flow_control</h3>

bool: Manage the rate of data transmission by enabling PAUSE frames.
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.ppm_enable">ppm_enable</h3>

bool: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersTenGigLan.autonegotiate_masterslave_enable">autonegotiate_masterslave_enable</h3>

bool: TBD
<h2 id="openhltest.SessionsStatisticsPorts">SessionsStatisticsPorts</h2>

```python
SessionsStatisticsPorts(self, parent, yang_key_value=None)
```
TBD

<h3 id="openhltest.SessionsStatisticsPorts.connected_test_port_id">connected_test_port_id</h3>

str: The id of the connected test port.  Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.connection_state_details">connection_state_details</h3>

str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.name">name</h3>

str: An abstract test port name
<h3 id="openhltest.SessionsStatisticsPorts.connection_state">connection_state</h3>

:str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port
Enums:
 CONNECTING: TBD
 CONNECTED_LINK_UP: TBD
 CONNECTED_LINK_DOWN: TBD
 DISCONNECTING: TBD
 DISCONNECTED: TBD

<h3 id="openhltest.SessionsStatisticsPorts.connected_test_port_description">connected_test_port_description</h3>

str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.rx_frames">rx_frames</h3>

str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.speed">speed</h3>

str: The actual speed of the test port. Empty if the abstract port is not connected to a test port.
<h3 id="openhltest.SessionsStatisticsPorts.tx_frames">tx_frames</h3>

str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port.
<h2 id="openhltest.Sessions">Sessions</h2>

```python
Sessions(self, parent, yang_key_value=None)
```
A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.

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

str: The unique name of test tool session
<h3 id="openhltest.Sessions.session_type">session_type</h3>

:str:`enum`: The type of test tool session. Once the session has been created the session-type cannot be changed.
Enums:
 L2L3: TBD
 L4L7: TBD

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

<h2 id="openhltest.SessionsStatistics">SessionsStatistics</h2>

```python
SessionsStatistics(self, parent)
```
The statistics pull model

<h3 id="openhltest.SessionsStatistics.username">username</h3>

str: name of authenticated user who started the session
<h3 id="openhltest.SessionsStatistics.clear">clear</h3>

```python
SessionsStatistics.clear(self)
```
Execute the clear action on the server

Clear all statistic counters.

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsStatistics.last_activity_timestamp">last_activity_timestamp</h3>

yang:date-and-time: Timestamp of the last request to this session
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

<h3 id="openhltest.SessionsStatistics.vendor_user_interface">vendor_user_interface</h3>

str: a vendor specific link to a user interface
<h3 id="openhltest.SessionsStatistics.first_activity_timestamp">first_activity_timestamp</h3>

yang:date-and-time: Timestamp of the first request to this session.
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

<h2 id="openhltest.SessionsConfigProtocolGroups">SessionsConfigProtocolGroups</h2>

```python
SessionsConfigProtocolGroups(self, parent, yang_key_value=None)
```
A list of emulated protocol groups

<h3 id="openhltest.SessionsConfigProtocolGroups.name">name</h3>

str: The unique name of an emulated protocol group
<h2 id="openhltest.SessionsConfigPhysicalLayers">SessionsConfigPhysicalLayers</h2>

```python
SessionsConfigPhysicalLayers(self, parent, yang_key_value=None)
```
A list of physical layer definitions

<h3 id="openhltest.SessionsConfigPhysicalLayers.layer_type">layer_type</h3>

:str:`enum`: Determines which detailed physical layer conditional container is active
Enums:
 ETHERNET: TBD
 TEN_GIG_LAN: TBD
 TEN_GIG_WAN: TBD
 FORTY_GIG: TBD
 HUNDRED_GIG: TBD
 FOUR_HUNDRED_GIG: TBD
 ATM: TBD
 POS: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayers.ten_gig_lan">ten_gig_lan</h3>

```python
SessionsConfigPhysicalLayers.ten_gig_lan(self)
```
Get the ten-gig-lan object from the server

The conditional container for detailed ten gig  lan physical layer information

Returns:
 :obj:`SessionsConfigPhysicalLayersTenGigLan`: An object encapsulating an instance of the ten-gig-lan model.

Raises:
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfigPhysicalLayers.name">name</h3>

str: The unique name of the physical layer definition
<h3 id="openhltest.SessionsConfigPhysicalLayers.ethernet">ethernet</h3>

```python
SessionsConfigPhysicalLayers.ethernet(self)
```
Get the ethernet object from the server

The conditional container for detailed ethernet physical layer information

Returns:
 :obj:`SessionsConfigPhysicalLayersEthernet`: An object encapsulating an instance of the ethernet model.

Raises:
 ServerError: An abnormal server error has occurred.

<h2 id="openhltest.OpenhltestSession">OpenhltestSession</h2>

```python
OpenhltestSession(self, ip_address, rest_port)
```
This module defines session capabilities.

<h3 id="openhltest.OpenhltestSession.sessions">sessions</h3>

```python
OpenhltestSession.sessions(self, name=None)
```
Get the sessions object(s) from the server.

A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.

Args:
 name (:obj:`str`, optional, default=None): A key value in the sessions list.

Returns:
 :obj:`list` of :obj:`Sessions` | :obj:`Sessions`: If arg name is None a list of Sessions objects otherwise a single Sessions object.

Raises:
 NotFoundError: name is not in the list of sessions objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.OpenhltestSession.create_sessions">create_sessions</h3>

```python
OpenhltestSession.create_sessions(self, name)
```
Create a sessions instance on the server.

A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`Sessions`: An object encapsulating an instance of the sessions model.

Raises:
 AlreadyExistsError: An instance of sessions with the supplied key value already exists on the server.
 ServerError: An abnormal server error has occurred.

<h2 id="openhltest.SessionsConfigPhysicalLayersEthernet">SessionsConfigPhysicalLayersEthernet</h2>

```python
SessionsConfigPhysicalLayersEthernet(self, parent)
```
The conditional container for detailed ethernet physical layer information

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.ignore_link_status">ignore_link_status</h3>

bool: Allow the port to continue transmitting traffic if the link(s) with its peer port(s) goes down
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.auto_mdix">auto_mdix</h3>

bool: Detect if the connection would require a crossover, and automatically chooses  the MDI or MDI-X configuration to properly match the other end of the link
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.autonegotiate">autonegotiate</h3>

bool: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.forward_error_correction">forward_error_correction</h3>

bool: Enable message encoding to control data transmission errors.
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.ppm">ppm</h3>

int32: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.auto_instrumentation">auto_instrumentation</h3>

:str:`enum`: TBD
Enums:
 END_OF_FRAME: TBD
 FLOATING: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.speed">speed</h3>

:str:`enum`: TBD
Enums:
 TEN_M: TBD
 ONE_HUNDRED_M: TBD
 ONE_G: TBD
 TWO_G: TBD
 THREE_G: TBD
 FOUR_G: TBD
 FIVE_G: TBD
 SIX_G: TBD
 SEVEN_G: TBD
 EIGHT_G: TBD
 NINE_G: TBD
 TEN_G: TBD
 TWENTY_G: TBD
 TWENTY_FIVE_G: TBD
 THIRTY_G: TBD
 FORTY_G: TBD
 FIFTY_G: TBD
 HUNDRED_G: TBD
 FOUR_HUNDRED_G: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.loopback">loopback</h3>

:str:`enum`: TBD
Enums:
 NORMAL: TBD
 LOOPBACK: TBD
 MONITOR: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.media">media</h3>

:str:`enum`: TBD
Enums:
 COPPER: TBD
 FIBER: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.forward_error_correction_mode">forward_error_correction_mode</h3>

:str:`enum`: TBD
Enums:
 NONE: TBD
 RS_FEC: TBD
 KR_FEC: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.autonegotiate_masterslave">autonegotiate_masterslave</h3>

:str:`enum`: TBD
Enums:
 MASTER: TBD
 SLAVE: TBD

<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.flow_control">flow_control</h3>

bool: Manage the rate of data transmission by enabling PAUSE frames.
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.ppm_enable">ppm_enable</h3>

bool: TBD
<h3 id="openhltest.SessionsConfigPhysicalLayersEthernet.autonegotiate_masterslave_enable">autonegotiate_masterslave_enable</h3>

bool: TBD
<h2 id="openhltest.SessionsConfigTrafficGroups">SessionsConfigTrafficGroups</h2>

```python
SessionsConfigTrafficGroups(self, parent, yang_key_value=None)
```
A list of traffic groups

<h3 id="openhltest.SessionsConfigTrafficGroups.name">name</h3>

str: The unique name of a traffic group
<h2 id="openhltest.SessionsConfigPorts">SessionsConfigPorts</h2>

```python
SessionsConfigPorts(self, parent, yang_key_value=None)
```
A list of abstract test ports

<h3 id="openhltest.SessionsConfigPorts.name">name</h3>

str: The unique name of an abstract test port
<h2 id="openhltest.SessionsConfig">SessionsConfig</h2>

```python
SessionsConfig(self, parent)
```
This container aggregates all other top level configuration submodules.

<h3 id="openhltest.SessionsConfig.load">load</h3>

```python
SessionsConfig.load(self, load_input)
```
Execute the load action on the server

Load a vendor specific configuration

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.stop_protocols">stop_protocols</h3>

```python
SessionsConfig.stop_protocols(self, stop_protocols_input)
```
Execute the stop-protocols action on the server

Stop one or more protocol groups.  An empty list signifiels that all protocol groups will be stopped.

:return: StopProtocolsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.connect_ports">connect_ports</h3>

```python
SessionsConfig.connect_ports(self, connect_ports_input)
```
Execute the connect-ports action on the server

Connect abstract test ports to physical hardware test ports and/or  virtual machine test ports

:return: ConnectPortsOutput.
:raises ServerException: An abnormal server error has occurred.

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

<h3 id="openhltest.SessionsConfig.create_physical_layers">create_physical_layers</h3>

```python
SessionsConfig.create_physical_layers(self, name)
```
Create a physical-layers instance on the server.

A list of physical layer definitions

Args:
 name (str): A unique key value that does not exist in the list on the server.

Returns:
 :obj:`SessionsConfigPhysicalLayers`: An object encapsulating an instance of the physical-layers model.

Raises:
 AlreadyExistsError: An instance of physical-layers with the supplied key value already exists on the server.
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

<h3 id="openhltest.SessionsConfig.start_traffic">start_traffic</h3>

```python
SessionsConfig.start_traffic(self, start_traffic_input)
```
Execute the start-traffic action on the server

Start one or more traffic groups. An empty list signifies that all traffic groups will be started.

:return: StartTrafficOutput.
:raises ServerException: An abnormal server error has occurred.

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

<h3 id="openhltest.SessionsConfig.physical_layers">physical_layers</h3>

```python
SessionsConfig.physical_layers(self, name=None)
```
Get the physical-layers object(s) from the server.

A list of physical layer definitions

Args:
 name (:obj:`str`, optional, default=None): A key value in the physical-layers list.

Returns:
 :obj:`list` of :obj:`SessionsConfigPhysicalLayers` | :obj:`SessionsConfigPhysicalLayers`: If arg name is None a list of SessionsConfigPhysicalLayers objects otherwise a single SessionsConfigPhysicalLayers object.

Raises:
 NotFoundError: name is not in the list of physical-layers objects.
 ServerError: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.disconnect_ports">disconnect_ports</h3>

```python
SessionsConfig.disconnect_ports(self, disconnect_ports_input)
```
Execute the disconnect-ports action on the server

Disconnect abstract test ports from any connected physical hardware test ports and/or virtual machine test ports

:return: DisconnectPortsOutput.
:raises ServerException: An abnormal server error has occurred.

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

<h3 id="openhltest.SessionsConfig.start_protocols">start_protocols</h3>

```python
SessionsConfig.start_protocols(self, start_protocols_input)
```
Execute the start-protocols action on the server

Start one or more emulated protocol groups. An empty list signifies that all protocol groups will be started.

:return: StartProtocolsOutput.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.clear">clear</h3>

```python
SessionsConfig.clear(self)
```
Execute the clear action on the server

Clear the current configuration

:return: None.
:raises ServerException: An abnormal server error has occurred.

<h3 id="openhltest.SessionsConfig.stop_traffic">stop_traffic</h3>

```python
SessionsConfig.stop_traffic(self, stop_traffic_input)
```
Execute the stop-traffic action on the server

Stop one or more traffic groups.  An empty list signifies that all traffic groups will be stopped.

:return: StopTrafficOutput.
:raises ServerException: An abnormal server error has occurred.

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

