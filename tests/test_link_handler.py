import pathlib
import unittest

from sdx.datamodel.models.link import Link
from sdx.datamodel.parsing.exceptions import MissingAttributeException
from sdx.datamodel.parsing.linkhandler import LinkHandler


class LinkHandlerTests(unittest.TestCase):
    TEST_DATA_DIR = pathlib.Path(__file__).parent.joinpath("data")
    LINK_FILE = TEST_DATA_DIR.joinpath("link.json")

    def test_import_link(self):
        link = LinkHandler().import_link(self.LINK_FILE)
        print(f"Link: {link}")
        self.assertIsInstance(link, Link)

    def test_import_empty_link(self):
        self.assertRaisesRegex(
            MissingAttributeException,
            "Missing required attribute 'id' while parsing <{}>",
            LinkHandler().import_link_data,
            {},
        )

    def test_import_null_link(self):
        self.assertRaisesRegex(
            TypeError,
            "expected str, bytes or os.PathLike object, not NoneType",
            LinkHandler().import_link,
            None,
        )


if __name__ == "__main__":
    unittest.main()
