import json

from sdx.datamodel.models.location import Location

from .exceptions import MissingAttributeException


class LocationHandler:

    """
    Handler for parsing the connection request descritpion in JSON.
    """

    def __init__(self):
        super().__init__()

    def import_location_data(self, data) -> Location:
        address = data.get("address")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        return Location(
            address=address, longitude=longitude, latitude=latitude
        )

    def import_location(self, path) -> Location:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return self.import_location_data(data)
