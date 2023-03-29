import pathlib
import unittest

from sdx.datamodel.models.service import Service
from sdx.datamodel.parsing.exceptions import MissingAttributeException
from sdx.datamodel.parsing.servicehandler import ServiceHandler


class ServiceHandlerTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    SERVICE_FILE = TEST_DATA_DIR.joinpath("service.json")

    def test_import_service(self):
        print("Test Service")
        service = ServiceHandler().import_service(self.SERVICE_FILE)
        print(f"Service: {service}")

        self.assertIsInstance(service, Service)
        self.assertEqual(service.owner, "FIU")
        self.assertIsNone(service.monitoring_capability)
        self.assertIsNone(service.provisioning_system)
        self.assertIsNone(service.provisioning_url)
        self.assertIsNone(service.vendor)
        self.assertIsNone(service.private_attributes)

    def test_import_empty_service(self):
        self.assertRaisesRegex(
            MissingAttributeException,
            "Missing required attribute 'owner' while parsing <{}>",
            ServiceHandler().import_service_data,
            {},
        )

    def test_import_null_service(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            ServiceHandler().import_service,
            None,
        )


if __name__ == "__main__":
    unittest.main()
