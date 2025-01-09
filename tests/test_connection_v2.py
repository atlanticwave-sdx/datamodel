import datetime
import unittest

from sdx_datamodel.models.connection_qos_metrics import ConnectionQosMetrics
from sdx_datamodel.models.connection_scheduling import ConnectionScheduling
from sdx_datamodel.models.connection_v2 import Connection
from sdx_datamodel.models.link import Link
from sdx_datamodel.models.port import Port
from sdx_datamodel.parsing.connectionhandler import ConnectionHandler
from sdx_datamodel.validation.connectionvalidator import ConnectionValidator


class TestConnection(unittest.TestCase):

    def _get_validator(self, data):
        """
        Return a validator for the given file.
        """
        handler = ConnectionHandler()
        connection = handler.import_connection_data(data)
        return ConnectionValidator(connection)

    def test_connection(self):
        # Create test data
        endpoints = [Port(id="port1"), Port(id="port2")]
        scheduling = ConnectionScheduling(
            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now() + datetime.timedelta(hours=1),
        )
        qos_metrics = ConnectionQosMetrics(
            min_bw=100, max_delay=10, max_number_oxps=2
        )
        paths = ["path1", "path2"]
        exclusive_links = [Link(id="link1"), Link(id="link2")]

        # Create a Connection instance
        connection = Connection(
            id="connection1",
            name="Test Connection",
            endpoints=endpoints,
            description="Test Description",
            scheduling=scheduling,
            qos_metrics=qos_metrics,
            paths=paths,
            exclusive_links=exclusive_links,
        )

        # Perform assertions
        self.assertEqual(connection.id, "connection1")
        self.assertEqual(connection.name, "Test Connection")
        self.assertEqual(connection.endpoints, endpoints)
        self.assertEqual(connection.description, "Test Description")
        self.assertEqual(connection.scheduling, scheduling)
        self.assertEqual(connection.qos_metrics, qos_metrics)
        self.assertEqual(connection.paths, paths)
        self.assertEqual(connection.exclusive_links, exclusive_links)

        """
        Validate a JSON document descibing a connection.
        """

    def test_connection_invalida_qos_metrics(self):
        connection_request = {
            "name": "VLAN between AMPATH/2010 and TENET/2010",
            "endpoints": [
                {
                    "port_id": "urn:sdx:port:ampath.net:Ampath3:50",
                    "vlan": "2010",
                },
                {
                    "port_id": "urn:sdx:port:tenet.ac.za:Tenet03:50",
                    "vlan": "2010",
                },
            ],
            "qos_metrics": {
                "max_delay": {"value": 1001},
                "max_number_oxps": {"value": 101},
            },
        }

        validator = self._get_validator(connection_request)
        self.assertTrue(validator.is_valid())


if __name__ == "__main__":
    unittest.main()
