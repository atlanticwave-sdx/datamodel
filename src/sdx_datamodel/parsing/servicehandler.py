import json

from sdx_datamodel.models.service import Service

from .exceptions import MissingAttributeException


class ServiceHandler:
    """
    Handler for parsing service data.
    """

    def import_service_data(self, data) -> Service:
        try:
            l2vpn_ptp = (None,)
            l2vpn_ptmp = (None,)
            owner = data["owner"]

            # Optional attributes -- set to None if not present.
            monitoring_capability = data.get("monitoring_capability")
            provisioning_system = data.get("provisioning_system")
            provisioning_url = data.get("provisioning_url")
            vendor = data.get("vendor")
            private_attributes = data.get("private_attributes")
        except Exception as e:
            # raise MissingAttributeException(data, e.args[0])
            for item in data:
                if item == "l2vpn-ptp":
                    l2vpn_ptp = item
                elif item == "l2vpn-ptmp":
                    l2vpn_ptmp = item
            monitoring_capability = None
            owner = None
            private_attributes = None
            provisioning_system = None
            provisioning_url = None
            vendor = None

        return Service(
            l2vpn_ptp=l2vpn_ptp,
            l2vpn_ptmp=l2vpn_ptmp,
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
