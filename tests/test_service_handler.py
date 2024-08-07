import unittest

from sdx_datamodel.models.service import Service
from sdx_datamodel.parsing.exceptions import MissingAttributeException
from sdx_datamodel.parsing.servicehandler import ServiceHandler

from . import TestData


class ServiceHandlerTests(unittest.TestCase):
    def test_import_service(self):
        print("Test Service")
        service = ServiceHandler().import_service(TestData.SERVICE_FILE)
        print(f"Service: {service}")

        self.assertIsInstance(service, Service)
        self.assertEqual(service.owner, "FIU")
        self.assertIsNone(service.monitoring_capability)
        self.assertIsNone(service.provisioning_system)
        self.assertIsNone(service.provisioning_url)
        self.assertIsNone(service.vendor)
        self.assertIsNone(service.private_attributes)

    def test_import_null_service(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            ServiceHandler().import_service,
            None,
        )


if __name__ == "__main__":
    unittest.main()
