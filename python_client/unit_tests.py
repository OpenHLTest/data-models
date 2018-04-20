import unittest
from OpenHlTest import *
from YangBase import *

class Tests(unittest.TestCase):
    def test_yang_output_decoder(self):
        input_dict = {
            'openhltest-session:output': {
                'errata': [
                    {
                        'name': 'aaaa',
                        'detail': 'bbbb',
                        'stack-trace': 'cccc'
                    }
                ]
            }
        }
        connect_ports_output = YangBase(None, None)._yang_output_decoder(input_dict, Config.ConnectPortsOutput())

        self.assertEqual(connect_ports_output.errata[0].name, input_dict['openhltest-session:output']['errata'][0]['name'])
        self.assertEqual(connect_ports_output.errata[0].detail, input_dict['openhltest-session:output']['errata'][0]['detail'])
        self.assertEqual(connect_ports_output.errata[0].stack_trace, input_dict['openhltest-session:output']['errata'][0]['stack-trace'])

if __name__ == '__main__':
    unittest.main()
