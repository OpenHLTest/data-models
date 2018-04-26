from httptransport import HttpTransport
from yangbase import YangBase


class Openhltest(YangBase):
	"""This module is the top level of the test hierarchy. 
	"""
	def __init__(self, ip_address, rest_port):
		self.YANG_MODULE = ''
		self.YANG_CLASS = ''
		super(Openhltest, self).__init__(HttpTransport(ip_address, rest_port), None)

	def sessions(self, name=None):
		"""Get the sessions object(s) from the server.

		A list of test tool sessions.

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the sessions list.  

		Returns:  
			:obj:`list` of :obj:`Sessions` | :obj:`Sessions`: If arg name is None a list of Sessions objects otherwise a single Sessions object.  

		Raises:  
			NotFoundError: name is not in the list of sessions objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(Sessions(self, name))

	def create_sessions(self, name):
		"""Create a child sibling sessions instance on the server.

		A list of test tool sessions.

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`Sessions`: An object encapsulating an instance of the sessions model.  

		Raises:  
			AlreadyExistsError: An instance of sessions with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(Sessions(self, name), locals())


class Sessions(YangBase):
	"""A list of test tool sessions.
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'sessions'
		self.YANG_KEY = 'name'
		super(Sessions, self).__init__(parent, yang_key_value)

	def config(self):
		"""Get the config object from the server

		This container aggregates all other top level configuration submodules.

		Returns:  
			:obj:`SessionsConfig`: An object encapsulating an instance of the config model.  

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfig(self))

	def statistics(self):
		"""Get the statistics object from the server

		The statistics pull model

		Returns:  
			:obj:`SessionsStatistics`: An object encapsulating an instance of the statistics model.  

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsStatistics(self))

	def delete(self):
		"""Delete this sessions instance on the server.

		A list of test tool sessions.

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	def update(self):
		"""Update this sessions instance on the server with any changed property values.

		A list of test tool sessions.

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: The unique name of the test tool session. Once the session has been created the name cannot be modified."""
		return self._get_value('name')

	@property
	def session_type(self):
		""":str:`enum`: The type of test tool session. Once the session has been created the session-type cannot be modified.  
		Enums:  
			L2L3: A layer 23 test tool session  
			L4L7: A layer 47 test tool session. This is currently not supported and is a feature placeholder  
		"""
		return self._get_value('session-type')

	@session_type.setter
	def session_type(self, value):
		return self._set_value('session-type', value)


class SessionsConfig(YangBase):
	"""This container aggregates all other top level configuration submodules.
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'config'
		super(SessionsConfig, self).__init__(parent, None)

	def ports(self, name=None):
		"""Get the ports object(s) from the server.

		A list of abstract test ports

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the ports list.  

		Returns:  
			:obj:`list` of :obj:`SessionsConfigPorts` | :obj:`SessionsConfigPorts`: If arg name is None a list of SessionsConfigPorts objects otherwise a single SessionsConfigPorts object.  

		Raises:  
			NotFoundError: name is not in the list of ports objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigPorts(self, name))

	def create_ports(self, name):
		"""Create a child sibling ports instance on the server.

		A list of abstract test ports

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`SessionsConfigPorts`: An object encapsulating an instance of the ports model.  

		Raises:  
			AlreadyExistsError: An instance of ports with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(SessionsConfigPorts(self, name), locals())

	def protocol_groups(self, name=None):
		"""Get the protocol-groups object(s) from the server.

		A list of emulated protocol groups

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the protocol-groups list.  

		Returns:  
			:obj:`list` of :obj:`SessionsConfigProtocolGroups` | :obj:`SessionsConfigProtocolGroups`: If arg name is None a list of SessionsConfigProtocolGroups objects otherwise a single SessionsConfigProtocolGroups object.  

		Raises:  
			NotFoundError: name is not in the list of protocol-groups objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigProtocolGroups(self, name))

	def create_protocol_groups(self, name):
		"""Create a child sibling protocol-groups instance on the server.

		A list of emulated protocol groups

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`SessionsConfigProtocolGroups`: An object encapsulating an instance of the protocol-groups model.  

		Raises:  
			AlreadyExistsError: An instance of protocol-groups with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(SessionsConfigProtocolGroups(self, name), locals())

	def traffic_groups(self, name=None):
		"""Get the traffic-groups object(s) from the server.

		A list of traffic groups

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the traffic-groups list.  

		Returns:  
			:obj:`list` of :obj:`SessionsConfigTrafficGroups` | :obj:`SessionsConfigTrafficGroups`: If arg name is None a list of SessionsConfigTrafficGroups objects otherwise a single SessionsConfigTrafficGroups object.  

		Raises:  
			NotFoundError: name is not in the list of traffic-groups objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigTrafficGroups(self, name))

	def create_traffic_groups(self, name):
		"""Create a child sibling traffic-groups instance on the server.

		A list of traffic groups

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`SessionsConfigTrafficGroups`: An object encapsulating an instance of the traffic-groups model.  

		Raises:  
			AlreadyExistsError: An instance of traffic-groups with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(SessionsConfigTrafficGroups(self, name), locals())

	def delete(self):
		"""Delete this config instance on the server.

		This container aggregates all other top level configuration submodules.

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	class ConnectPortsInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.port_map = []

		class PortMap(object):
			"""TBD
			"""
			def __init__(self):
				self.port_name = ''
				self.chassis = ''
				self.card = ''
				self.port = ''

	class ConnectPortsOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def connect_ports(self, connect_ports_input):
		"""Execute the connect-ports action on the server

		Connect abstract test ports to physical hardware test ports and/or virtual machine test ports

		Args:  
			connect_ports_input (:obj:`ConnectPortsInput`):  An object encapsulating an instance of the connect-ports action input model.  

		Returns:  
			:obj:`ConnectPortsOutput`:  An object encapsulating an instance of the connect-ports action output model.  

		Raises:  
			BadRequestError: The connect_ports_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/connect-ports', connect_ports_input)

	class DisconnectPortsInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.port_names = []

	class DisconnectPortsOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def disconnect_ports(self, disconnect_ports_input):
		"""Execute the disconnect-ports action on the server

		Disconnect abstract test ports from any connected physical hardware test ports and/or virtual machine test ports

		Args:  
			disconnect_ports_input (:obj:`DisconnectPortsInput`):  An object encapsulating an instance of the disconnect-ports action input model.  

		Returns:  
			:obj:`DisconnectPortsOutput`:  An object encapsulating an instance of the disconnect-ports action output model.  

		Raises:  
			BadRequestError: The disconnect_ports_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/disconnect-ports', disconnect_ports_input)

	class StartProtocolsInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.protocol_group_names = []

	class StartProtocolsOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def start_protocols(self, start_protocols_input):
		"""Execute the start-protocols action on the server

		Start one or more emulated protocol groups. An empty list signifies that all protocol groups will be started.

		Args:  
			start_protocols_input (:obj:`StartProtocolsInput`):  An object encapsulating an instance of the start-protocols action input model.  

		Returns:  
			:obj:`StartProtocolsOutput`:  An object encapsulating an instance of the start-protocols action output model.  

		Raises:  
			BadRequestError: The start_protocols_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/start-protocols', start_protocols_input)

	class StopProtocolsInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.protocol_group_names = []

	class StopProtocolsOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def stop_protocols(self, stop_protocols_input):
		"""Execute the stop-protocols action on the server

		Stop one or more protocol groups. An empty list signifiels that all protocol groups will be stopped.

		Args:  
			stop_protocols_input (:obj:`StopProtocolsInput`):  An object encapsulating an instance of the stop-protocols action input model.  

		Returns:  
			:obj:`StopProtocolsOutput`:  An object encapsulating an instance of the stop-protocols action output model.  

		Raises:  
			BadRequestError: The stop_protocols_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/stop-protocols', stop_protocols_input)

	class StartTrafficInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.traffic_group_names = []

	class StartTrafficOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def start_traffic(self, start_traffic_input):
		"""Execute the start-traffic action on the server

		Start one or more traffic groups. An empty list signifies that all traffic groups will be started.

		Args:  
			start_traffic_input (:obj:`StartTrafficInput`):  An object encapsulating an instance of the start-traffic action input model.  

		Returns:  
			:obj:`StartTrafficOutput`:  An object encapsulating an instance of the start-traffic action output model.  

		Raises:  
			BadRequestError: The start_traffic_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/start-traffic', start_traffic_input)

	class StopTrafficInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.traffic_group_names = []

	class StopTrafficOutput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:output'
			self.errata = []

		class Errata(object):
			"""A list of rpc errors. An empty list indicates no errors occurred
			"""
			def __init__(self):
				self.name = ''
				self.detail = ''
				self.stack_trace = ''

	def stop_traffic(self, stop_traffic_input):
		"""Execute the stop-traffic action on the server

		Stop one or more traffic groups. An empty list signifies that all traffic groups will be stopped.

		Args:  
			stop_traffic_input (:obj:`StopTrafficInput`):  An object encapsulating an instance of the stop-traffic action input model.  

		Returns:  
			:obj:`StopTrafficOutput`:  An object encapsulating an instance of the stop-traffic action output model.  

		Raises:  
			BadRequestError: The stop_traffic_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/stop-traffic', stop_traffic_input)

	def clear(self):
		"""Execute the clear action on the server

		Clear the current configuration

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/clear')

	class LoadInput(object):
		"""TBD
		"""
		def __init__(self):
			self.YANG_PATH = 'openhltest:input'
			self.vendor_config = ''

	def load(self, load_input):
		"""Execute the load action on the server

		Load a vendor specific configuration

		Args:  
			load_input (:obj:`LoadInput`):  An object encapsulating an instance of the load action input model.  

		Raises:  
			BadRequestError: The load_input arg has invalid values.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/load', load_input)


class SessionsConfigPorts(YangBase):
	"""A list of abstract test ports
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsConfigPorts, self).__init__(parent, yang_key_value)

	def delete(self):
		"""Delete this ports instance on the server.

		A list of abstract test ports

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	def update(self):
		"""Update this ports instance on the server with any changed property values.

		A list of abstract test ports

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: The unique name of an abstract test port"""
		return self._get_value('name')


class SessionsConfigProtocolGroups(YangBase):
	"""A list of emulated protocol groups
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'protocol-groups'
		self.YANG_KEY = 'name'
		super(SessionsConfigProtocolGroups, self).__init__(parent, yang_key_value)

	def delete(self):
		"""Delete this protocol-groups instance on the server.

		A list of emulated protocol groups

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	def update(self):
		"""Update this protocol-groups instance on the server with any changed property values.

		A list of emulated protocol groups

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: The unique name of an emulated protocol group"""
		return self._get_value('name')

	@property
	def port_names(self):
		"""str: A list of abstract test port names"""
		return self._get_value('port-names')

	@port_names.setter
	def port_names(self, value):
		return self._set_value('port-names', value)


class SessionsConfigTrafficGroups(YangBase):
	"""A list of traffic groups
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'traffic-groups'
		self.YANG_KEY = 'name'
		super(SessionsConfigTrafficGroups, self).__init__(parent, yang_key_value)

	def delete(self):
		"""Delete this traffic-groups instance on the server.

		A list of traffic groups

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	def update(self):
		"""Update this traffic-groups instance on the server with any changed property values.

		A list of traffic groups

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: The unique name of a traffic group"""
		return self._get_value('name')


class SessionsStatistics(YangBase):
	"""The statistics pull model
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'statistics'
		super(SessionsStatistics, self).__init__(parent, None)

	def ports(self, name=None):
		"""Get the ports object(s) from the server.

		TBD

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the ports list.  

		Returns:  
			:obj:`list` of :obj:`SessionsStatisticsPorts` | :obj:`SessionsStatisticsPorts`: If arg name is None a list of SessionsStatisticsPorts objects otherwise a single SessionsStatisticsPorts object.  

		Raises:  
			NotFoundError: name is not in the list of ports objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsStatisticsPorts(self, name))

	def create_ports(self, name):
		"""Create a child sibling ports instance on the server.

		TBD

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`SessionsStatisticsPorts`: An object encapsulating an instance of the ports model.  

		Raises:  
			AlreadyExistsError: An instance of ports with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(SessionsStatisticsPorts(self, name), locals())

	def delete(self):
		"""Delete this statistics instance on the server.

		The statistics pull model

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._delete()

	def update(self):
		"""Update this statistics instance on the server with any changed property values.

		The statistics pull model

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def first_activity_timestamp(self):
		"""yang:date-and-time: Timestamp of the first request to this session."""
		return self._get_value('first-activity-timestamp')

	@property
	def last_activity_timestamp(self):
		"""yang:date-and-time: Timestamp of the last request to this session"""
		return self._get_value('last-activity-timestamp')

	def clear(self):
		"""Execute the clear action on the server

		Clear all statistic counters.

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/clear')


class SessionsStatisticsPorts(YangBase):
	"""TBD
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsStatisticsPorts, self).__init__(parent, yang_key_value)

	def update(self):
		"""Update this ports instance on the server with any changed property values.

		TBD

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: An abstract test port name"""
		return self._get_value('name')

	@property
	def connected_test_port_id(self):
		"""str: The id of the connected test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-id')

	@property
	def connected_test_port_description(self):
		"""str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-description')

	@property
	def connection_state(self):
		""":str:`enum`: The state of the connection to the physical hardware test port or virtual machine test port  
		Enums:  
			CONNECTING: TBD  
			CONNECTED_LINK_UP: TBD  
			CONNECTED_LINK_DOWN: TBD  
			DISCONNECTING: TBD  
			DISCONNECTED: TBD  
		"""
		return self._get_value('connection-state')

	@property
	def connection_state_details(self):
		"""str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connection-state-details')

	@property
	def speed(self):
		"""str: The actual speed of the test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('speed')

	@property
	def tx_frames(self):
		"""str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('tx-frames')

	@property
	def rx_frames(self):
		"""str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('rx-frames')


class SessionsStatisticEventsPorts(YangBase):
	"""TBD
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsStatisticEventsPorts, self).__init__(parent, yang_key_value)

	def update(self):
		"""Update this ports instance on the server with any changed property values.

		TBD

		Raises:  
			NotFoundError: This instance does not exist on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._update()

	@property
	def name(self):
		"""str: An abstract test port name"""
		return self._get_value('name')

	@property
	def connected_test_port_id(self):
		"""str: The id of the connected test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-id')

	@property
	def connected_test_port_description(self):
		"""str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-description')

	@property
	def connection_state(self):
		""":str:`enum`: The state of the connection to the physical hardware test port or virtual machine test port  
		Enums:  
			CONNECTING: TBD  
			CONNECTED_LINK_UP: TBD  
			CONNECTED_LINK_DOWN: TBD  
			DISCONNECTING: TBD  
			DISCONNECTED: TBD  
		"""
		return self._get_value('connection-state')

	@property
	def connection_state_details(self):
		"""str: Free form vendor specific information about the state of the connection to the physical hardware test port or virtual machine test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connection-state-details')

	@property
	def speed(self):
		"""str: The actual speed of the test port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('speed')

	@property
	def tx_frames(self):
		"""str: The total number of frames transmitted on the port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('tx-frames')

	@property
	def rx_frames(self):
		"""str: The total number of frames received on the the port. Empty if the abstract port is not connected to a test port."""
		return self._get_value('rx-frames')


