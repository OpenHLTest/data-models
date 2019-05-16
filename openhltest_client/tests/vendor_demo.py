'''The script does the following:
	- loads a vendor binary configuration
	- connects abstract ports to test ports
	- starts protocols
	- starts traffic
	- waits until traffic is complete
	- prints out port and traffic statistics

Vendor configuration details:
	- Ports:
		- 2 ethernet ports at a line speed of 1G
	- Protocols:
		- each port will have ethernet + ipv4 + bgpv4
	- Traffic:
		- one traffic item
		- traffic mesh of one to one, port1 -> port2
		- fixed frame size of 128 byte
		- 1,000,000 frames sent over 10 seconds at a rate of 100,000
'''
import time
from openhltest_client.httptransport import HttpTransport


OPENHLTEST_SERVER = '127.0.0.1:443'
VENDOR_CONFIG_FILE = 'c:/users/anbalogh/downloads/openhltest.ixncfg'

transport = HttpTransport(OPENHLTEST_SERVER)

transport.info("get an instance of the OpenHlTest module class")
openhltest = transport.OpenHlTest

transport.info("get a list of Sessions")
sessions = openhltest.Sessions.read()
transport.info(sessions)

transport.info("get an instance of the Config class")
config = sessions.Config

transport.info("load a vendor specific binary configuration")
config.Load({'mode': 'VENDOR_BINARY', 'file-name': VENDOR_CONFIG_FILE})

transport.info("connect the abstract ports to test ports")
config.PortControl({"mode": "CONNECT", "targets": []})

transport.info("start the device-groups")
config.DeviceGroupsControl({"mode": "START", "targets": []})

transport.info("start the device-traffic")
config.TrafficControl({"mode": "START", "targets": []})

time.sleep(15)

transport.info("port statistics")
for port in sessions.Statistics.Port.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (port.Name, port.TxFrames, port.RxFrames))

transport.info("device-traffic statistics")
for device_traffic in sessions.Statistics.DeviceTraffic.read():
	transport.info('%s tx-frames:%s rx-frames:%s' % (device_traffic.Name, device_traffic.TxFrames, device_traffic.RxFrames))
