import json

from sdx_datamodel.models.service import Service

from .exceptions import MissingAttributeException


class ServiceHandler:
    """
    Handler for parsing service data.
    """

    def import_service_data(self, data) -> Service:
        try:
            owner = data["owner"]

            # Optional attributes -- set to None if not present.
            monitoring_capability = data.get("monitoring_capability")
            provisioning_system = data.get("provisioning_system")
            provisioning_url = data.get("provisioning_url")
            vendor = data.get("vendor")
            private_attributes = data.get("private_attributes")
        except Error as e:
            # raise MissingAttributeException(data, e.args[0])
            service = data
            monitoring_capability = None
            owner = None
            private_attributes = None
            provisioning_system = None
            provisioning_url = None
            vendor = None

        return Service(
            monitoring_capability=monitoring_capability,
            owner=owner,
            private_attributes=private_attributes,
            provisioning_system=provisioning_system,
            provisioning_url=provisioning_url,
            vendor=vendor,
        )

    def import_service(self, path) -> Service:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_service_data(data)
