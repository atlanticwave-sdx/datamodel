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

    def test_connection_validator_null_input(self):
        # Expect the matched error message when input is null.
        self.assertRaisesRegex(
            ValueError,
            "The Validator must be passed a Connection object",
            ConnectionValidator().set_connection,
            None,
        )


if __name__ == "__main__":
    unittest.main()
