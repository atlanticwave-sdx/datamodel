import pathlib
import unittest

from sdx.datamodel.validation.connectionvalidator import ConnectionValidator
from sdx.datamodel.parsing.connectionhandler import ConnectionHandler


class TestConnectionValidator(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    CONNECTION_P2P = TEST_DATA_DIR.joinpath("p2p.json")

    def test_connection_validator(self):
        connection = ConnectionHandler().import_connection(self.CONNECTION_P2P)
        print(f"Imported Connection: {connection}")

        validator = ConnectionValidator()
        validator.set_connection(connection)
        self.assertTrue(validator.is_valid())


if __name__ == "__main__":
    unittest.main()
