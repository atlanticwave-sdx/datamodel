import pathlib
import unittest

from sdx.datamodel.validation.connectionvalidator import ConnectionValidator
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler


class TestConnectionValidator(unittest.TestCase):
    def test_connection_validator(self):
        CONNECTION_P2P = pathlib.Path(__file__).parent.joinpath(
            "data", "p2p.json"
        )

        self.handler = ConnectionHandler()
        connection = self.handler.import_connection(CONNECTION_P2P)
        print(f"Imported Connection: {connection}")

        self.validator = ConnectionValidator()
        self.validator.set_connection(connection)
        self.assertTrue(self.validator.is_valid())


if __name__ == "__main__":
    unittest.main()
