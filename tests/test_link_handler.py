import unittest

from sdx_datamodel.models.link import Link
from sdx_datamodel.parsing.exceptions import MissingAttributeException
from sdx_datamodel.parsing.linkhandler import LinkHandler

from . import TestData


class LinkHandlerTests(unittest.TestCase):
    def test_import_link(self):
        link = LinkHandler().import_link(TestData.LINK_FILE)
        print(f"Link: {link}")
        self.assertIsInstance(link, Link)

    def test_link_setters(self):
        link = LinkHandler().import_link(TestData.LINK_FILE)
        self.assertIsInstance(link, Link)

        with self.assertRaises(ValueError) as ex:
            link.name = None

        self.assertIn(
            "Invalid value for `name`, must not be `None`", ex.exception.args
        )

        with self.assertRaises(ValueError) as ex:
            link.id = None

        self.assertIn(
            "Invalid value for `id`, must not be `None`", ex.exception.args
        )

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
