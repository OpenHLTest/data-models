from httptransport import HttpTransport
from yangbase import YangBase


class OpenhltestSession(YangBase):
	"""This module defines session capabilities.
	"""
	def __init__(self, ip_address, rest_port):
		self.YANG_MODULE = ''
		self.YANG_CLASS = ''
		super(OpenhltestSession, self).__init__(HttpTransport(ip_address, rest_port), None)

	def sessions(self, name=None):
		"""Get the sessions object(s) from the server.

		A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.

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
		"""Create a sessions instance on the server.

		A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.

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
	"""A list of test tool sessions. To start a test tool session create a new session. To stop a test tool session delete an existing session.
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
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

	@property
	def name(self):
		"""str: The unique name of test tool session"""
		return self._get_value('name')

	@property
	def session_type(self):
		""":str:`enum`: The type of test tool session. Once the session has been created the session-type cannot be changed.  
		Enums:  
			L2L3: TBD  
			L4L7: TBD  
		"""
		return self._get_value('session-type')

	@session_type.setter
	def session_type(self, value):
		return self._set_value('session-type', value)


class SessionsConfig(YangBase):
	"""This container aggregates all other top level configuration submodules.
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest-session'
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
		"""Create a ports instance on the server.

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

	def physical_layers(self, name=None):
		"""Get the physical-layers object(s) from the server.

		A list of physical layer definitions

		Args:  
			name (:obj:`str`, optional, default=None): A key value in the physical-layers list.  

		Returns:  
			:obj:`list` of :obj:`SessionsConfigPhysicalLayers` | :obj:`SessionsConfigPhysicalLayers`: If arg name is None a list of SessionsConfigPhysicalLayers objects otherwise a single SessionsConfigPhysicalLayers object.  

		Raises:  
			NotFoundError: name is not in the list of physical-layers objects.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigPhysicalLayers(self, name))

	def create_physical_layers(self, name):
		"""Create a physical-layers instance on the server.

		A list of physical layer definitions

		Args:  
			name (str): A unique key value that does not exist in the list on the server.  

		Returns:  
			:obj:`SessionsConfigPhysicalLayers`: An object encapsulating an instance of the physical-layers model.  

		Raises:  
			AlreadyExistsError: An instance of physical-layers with the supplied key value already exists on the server.  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._create(SessionsConfigPhysicalLayers(self, name), locals())

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
		"""Create a protocol-groups instance on the server.

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
		"""Create a traffic-groups instance on the server.

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

	class ConnectPortsInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class ConnectPortsOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def connect_ports(self, connect_ports_input):
		"""Execute the connect-ports action on the server

		Connect abstract test ports to physical hardware test ports and/or  virtual machine test ports

		:return: ConnectPortsOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/connect-ports', connect_ports_input)

	class DisconnectPortsInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class DisconnectPortsOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def disconnect_ports(self, disconnect_ports_input):
		"""Execute the disconnect-ports action on the server

		Disconnect abstract test ports from any connected physical hardware test ports and/or virtual machine test ports

		:return: DisconnectPortsOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/disconnect-ports', disconnect_ports_input)

	class StartProtocolsInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class StartProtocolsOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def start_protocols(self, start_protocols_input):
		"""Execute the start-protocols action on the server

		Start one or more emulated protocol groups. An empty list signifies that all protocol groups will be started.

		:return: StartProtocolsOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/start-protocols', start_protocols_input)

	class StopProtocolsInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class StopProtocolsOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def stop_protocols(self, stop_protocols_input):
		"""Execute the stop-protocols action on the server

		Stop one or more protocol groups.  An empty list signifiels that all protocol groups will be stopped.

		:return: StopProtocolsOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/stop-protocols', stop_protocols_input)

	class StartTrafficInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class StartTrafficOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def start_traffic(self, start_traffic_input):
		"""Execute the start-traffic action on the server

		Start one or more traffic groups. An empty list signifies that all traffic groups will be started.

		:return: StartTrafficOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/start-traffic', start_traffic_input)

	class StopTrafficInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	class StopTrafficOutput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:output'

	def stop_traffic(self, stop_traffic_input):
		"""Execute the stop-traffic action on the server

		Stop one or more traffic groups.  An empty list signifies that all traffic groups will be stopped.

		:return: StopTrafficOutput.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/stop-traffic', stop_traffic_input)

	def clear(self):
		"""Execute the clear action on the server

		Clear the current configuration

		:return: None.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/clear')

	class LoadInput(object):
		def __init__(self):
			self.YANG_PATH = 'openhltest-session:input'

	def load(self, load_input):
		"""Execute the load action on the server

		Load a vendor specific configuration

		:return: None.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/load', load_input)


class SessionsConfigPorts(YangBase):
	"""A list of abstract test ports
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsConfigPorts, self).__init__(parent, yang_key_value)

	@property
	def name(self):
		"""str: The unique name of an abstract test port"""
		return self._get_value('name')


class SessionsConfigPhysicalLayers(YangBase):
	"""A list of physical layer definitions
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'physical-layers'
		self.YANG_KEY = 'name'
		super(SessionsConfigPhysicalLayers, self).__init__(parent, yang_key_value)

	def ethernet(self):
		"""Get the ethernet object from the server

		The conditional container for detailed ethernet physical layer information

		Returns:  
			:obj:`SessionsConfigPhysicalLayersEthernet`: An object encapsulating an instance of the ethernet model.  

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigPhysicalLayersEthernet(self))

	def ten_gig_lan(self):
		"""Get the ten-gig-lan object from the server

		The conditional container for detailed ten gig  lan physical layer information

		Returns:  
			:obj:`SessionsConfigPhysicalLayersTenGigLan`: An object encapsulating an instance of the ten-gig-lan model.  

		Raises:  
			ServerError: An abnormal server error has occurred.  
		"""
		return self._read(SessionsConfigPhysicalLayersTenGigLan(self))

	@property
	def name(self):
		"""str: The unique name of the physical layer definition"""
		return self._get_value('name')

	@property
	def layer_type(self):
		""":str:`enum`: Determines which detailed physical layer conditional container is active  
		Enums:  
			ETHERNET: TBD  
			TEN_GIG_LAN: TBD  
			TEN_GIG_WAN: TBD  
			FORTY_GIG: TBD  
			HUNDRED_GIG: TBD  
			FOUR_HUNDRED_GIG: TBD  
			ATM: TBD  
			POS: TBD  
		"""
		return self._get_value('layer-type')

	@layer_type.setter
	def layer_type(self, value):
		return self._set_value('layer-type', value)


class SessionsConfigPhysicalLayersEthernet(YangBase):
	"""The conditional container for detailed ethernet physical layer information
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'ethernet'
		super(SessionsConfigPhysicalLayersEthernet, self).__init__(parent, None)

	@property
	def auto_mdix(self):
		"""bool: Detect if the connection would require a crossover, and automatically chooses  the MDI or MDI-X configuration to properly match the other end of the link"""
		return self._get_value('auto-mdix')

	@auto_mdix.setter
	def auto_mdix(self, value):
		return self._set_value('auto-mdix', value)

	@property
	def media(self):
		""":str:`enum`: TBD  
		Enums:  
			COPPER: TBD  
			FIBER: TBD  
		"""
		return self._get_value('media')

	@media.setter
	def media(self, value):
		return self._set_value('media', value)

	@property
	def ppm_enable(self):
		"""bool: TBD"""
		return self._get_value('ppm-enable')

	@ppm_enable.setter
	def ppm_enable(self, value):
		return self._set_value('ppm-enable', value)

	@property
	def ppm(self):
		"""int32: TBD"""
		return self._get_value('ppm')

	@ppm.setter
	def ppm(self, value):
		return self._set_value('ppm', value)

	@property
	def loopback(self):
		""":str:`enum`: TBD  
		Enums:  
			NORMAL: TBD  
			LOOPBACK: TBD  
			MONITOR: TBD  
		"""
		return self._get_value('loopback')

	@loopback.setter
	def loopback(self, value):
		return self._set_value('loopback', value)

	@property
	def autonegotiate(self):
		"""bool: TBD"""
		return self._get_value('autonegotiate')

	@autonegotiate.setter
	def autonegotiate(self, value):
		return self._set_value('autonegotiate', value)

	@property
	def autonegotiate_masterslave_enable(self):
		"""bool: TBD"""
		return self._get_value('autonegotiate-masterslave-enable')

	@autonegotiate_masterslave_enable.setter
	def autonegotiate_masterslave_enable(self, value):
		return self._set_value('autonegotiate-masterslave-enable', value)

	@property
	def autonegotiate_masterslave(self):
		""":str:`enum`: TBD  
		Enums:  
			MASTER: TBD  
			SLAVE: TBD  
		"""
		return self._get_value('autonegotiate-masterslave')

	@autonegotiate_masterslave.setter
	def autonegotiate_masterslave(self, value):
		return self._set_value('autonegotiate-masterslave', value)

	@property
	def flow_control(self):
		"""bool: Manage the rate of data transmission by enabling PAUSE frames."""
		return self._get_value('flow-control')

	@flow_control.setter
	def flow_control(self, value):
		return self._set_value('flow-control', value)

	@property
	def forward_error_correction(self):
		"""bool: Enable message encoding to control data transmission errors."""
		return self._get_value('forward-error-correction')

	@forward_error_correction.setter
	def forward_error_correction(self, value):
		return self._set_value('forward-error-correction', value)

	@property
	def forward_error_correction_mode(self):
		""":str:`enum`: TBD  
		Enums:  
			NONE: TBD  
			RS_FEC: TBD  
			KR_FEC: TBD  
		"""
		return self._get_value('forward-error-correction-mode')

	@forward_error_correction_mode.setter
	def forward_error_correction_mode(self, value):
		return self._set_value('forward-error-correction-mode', value)

	@property
	def ignore_link_status(self):
		"""bool: Allow the port to continue transmitting traffic if the link(s) with its peer port(s) goes down"""
		return self._get_value('ignore-link-status')

	@ignore_link_status.setter
	def ignore_link_status(self, value):
		return self._set_value('ignore-link-status', value)

	@property
	def speed(self):
		""":str:`enum`: TBD  
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
		"""
		return self._get_value('speed')

	@speed.setter
	def speed(self, value):
		return self._set_value('speed', value)

	@property
	def auto_instrumentation(self):
		""":str:`enum`: TBD  
		Enums:  
			END_OF_FRAME: TBD  
			FLOATING: TBD  
		"""
		return self._get_value('auto-instrumentation')

	@auto_instrumentation.setter
	def auto_instrumentation(self, value):
		return self._set_value('auto-instrumentation', value)


class SessionsConfigPhysicalLayersTenGigLan(YangBase):
	"""The conditional container for detailed ten gig  lan physical layer information
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'ten-gig-lan'
		super(SessionsConfigPhysicalLayersTenGigLan, self).__init__(parent, None)

	@property
	def auto_mdix(self):
		"""bool: Detect if the connection would require a crossover, and automatically chooses  the MDI or MDI-X configuration to properly match the other end of the link"""
		return self._get_value('auto-mdix')

	@auto_mdix.setter
	def auto_mdix(self, value):
		return self._set_value('auto-mdix', value)

	@property
	def media(self):
		""":str:`enum`: TBD  
		Enums:  
			COPPER: TBD  
			FIBER: TBD  
		"""
		return self._get_value('media')

	@media.setter
	def media(self, value):
		return self._set_value('media', value)

	@property
	def ppm_enable(self):
		"""bool: TBD"""
		return self._get_value('ppm-enable')

	@ppm_enable.setter
	def ppm_enable(self, value):
		return self._set_value('ppm-enable', value)

	@property
	def ppm(self):
		"""int32: TBD"""
		return self._get_value('ppm')

	@ppm.setter
	def ppm(self, value):
		return self._set_value('ppm', value)

	@property
	def loopback(self):
		""":str:`enum`: TBD  
		Enums:  
			NORMAL: TBD  
			LOOPBACK: TBD  
			MONITOR: TBD  
		"""
		return self._get_value('loopback')

	@loopback.setter
	def loopback(self, value):
		return self._set_value('loopback', value)

	@property
	def autonegotiate(self):
		"""bool: TBD"""
		return self._get_value('autonegotiate')

	@autonegotiate.setter
	def autonegotiate(self, value):
		return self._set_value('autonegotiate', value)

	@property
	def autonegotiate_masterslave_enable(self):
		"""bool: TBD"""
		return self._get_value('autonegotiate-masterslave-enable')

	@autonegotiate_masterslave_enable.setter
	def autonegotiate_masterslave_enable(self, value):
		return self._set_value('autonegotiate-masterslave-enable', value)

	@property
	def autonegotiate_masterslave(self):
		""":str:`enum`: TBD  
		Enums:  
			MASTER: TBD  
			SLAVE: TBD  
		"""
		return self._get_value('autonegotiate-masterslave')

	@autonegotiate_masterslave.setter
	def autonegotiate_masterslave(self, value):
		return self._set_value('autonegotiate-masterslave', value)

	@property
	def flow_control(self):
		"""bool: Manage the rate of data transmission by enabling PAUSE frames."""
		return self._get_value('flow-control')

	@flow_control.setter
	def flow_control(self, value):
		return self._set_value('flow-control', value)

	@property
	def forward_error_correction(self):
		"""bool: Enable message encoding to control data transmission errors."""
		return self._get_value('forward-error-correction')

	@forward_error_correction.setter
	def forward_error_correction(self, value):
		return self._set_value('forward-error-correction', value)

	@property
	def forward_error_correction_mode(self):
		""":str:`enum`: TBD  
		Enums:  
			NONE: TBD  
			RS_FEC: TBD  
			KR_FEC: TBD  
		"""
		return self._get_value('forward-error-correction-mode')

	@forward_error_correction_mode.setter
	def forward_error_correction_mode(self, value):
		return self._set_value('forward-error-correction-mode', value)

	@property
	def ignore_link_status(self):
		"""bool: Allow the port to continue transmitting traffic if the link(s) with its peer port(s) goes down"""
		return self._get_value('ignore-link-status')

	@ignore_link_status.setter
	def ignore_link_status(self, value):
		return self._set_value('ignore-link-status', value)

	@property
	def speed(self):
		""":str:`enum`: TBD  
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
		"""
		return self._get_value('speed')

	@speed.setter
	def speed(self, value):
		return self._set_value('speed', value)

	@property
	def lasi_monitoring_enabled(self):
		"""bool: TBD"""
		return self._get_value('lasi-monitoring-enabled')

	@lasi_monitoring_enabled.setter
	def lasi_monitoring_enabled(self, value):
		return self._set_value('lasi-monitoring-enabled', value)

	@property
	def flow_control_directed_address(self):
		"""str: TBD"""
		return self._get_value('flow-control-directed-address')

	@flow_control_directed_address.setter
	def flow_control_directed_address(self, value):
		return self._set_value('flow-control-directed-address', value)


class SessionsConfigProtocolGroups(YangBase):
	"""A list of emulated protocol groups
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'protocol-groups'
		self.YANG_KEY = 'name'
		super(SessionsConfigProtocolGroups, self).__init__(parent, yang_key_value)

	@property
	def name(self):
		"""str: The unique name of an emulated protocol group"""
		return self._get_value('name')


class SessionsConfigTrafficGroups(YangBase):
	"""A list of traffic groups
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'traffic-groups'
		self.YANG_KEY = 'name'
		super(SessionsConfigTrafficGroups, self).__init__(parent, yang_key_value)

	@property
	def name(self):
		"""str: The unique name of a traffic group"""
		return self._get_value('name')


class SessionsStatistics(YangBase):
	"""The statistics pull model
	"""
	def __init__(self, parent):
		self.YANG_MODULE = 'openhltest-session'
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
		"""Create a ports instance on the server.

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

	@property
	def username(self):
		"""str: name of authenticated user who started the session"""
		return self._get_value('username')

	@username.setter
	def username(self, value):
		return self._set_value('username', value)

	@property
	def vendor_user_interface(self):
		"""str: a vendor specific link to a user interface"""
		return self._get_value('vendor-user-interface')

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

		:return: None.  
		:raises ServerException: An abnormal server error has occurred.  
		"""
		return self._execute(self.url + '/clear')


class SessionsStatisticsPorts(YangBase):
	"""TBD
	"""
	def __init__(self, parent, yang_key_value=None):
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsStatisticsPorts, self).__init__(parent, yang_key_value)

	@property
	def name(self):
		"""str: An abstract test port name"""
		return self._get_value('name')

	@property
	def connected_test_port_id(self):
		"""str: The id of the connected test port.  Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-id')

	@property
	def connected_test_port_description(self):
		"""str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-description')

	@property
	def connection_state(self):
		""":str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port  
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
		self.YANG_MODULE = 'openhltest-session'
		self.YANG_CLASS = 'ports'
		self.YANG_KEY = 'name'
		super(SessionsStatisticEventsPorts, self).__init__(parent, yang_key_value)

	@property
	def name(self):
		"""str: An abstract test port name"""
		return self._get_value('name')

	@property
	def connected_test_port_id(self):
		"""str: The id of the connected test port.  Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-id')

	@property
	def connected_test_port_description(self):
		"""str: Free form vendor specific description of the connected test port. Can include details such as make/model/productId of the underlying hardware. Empty if the abstract port is not connected to a test port."""
		return self._get_value('connected-test-port-description')

	@property
	def connection_state(self):
		""":str:`enum`: The state of the connection to the physical hardware  test port or virtual machine test port  
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


