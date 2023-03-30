import unittest

from sdx.datamodel.models.link_measurement_period import LinkMeasurementPeriod


class LinkMeasurementPeriodTests(unittest.TestCase):
    def test_link_measurement_period(self):
        o = LinkMeasurementPeriod()

        self.assertIsInstance(o, LinkMeasurementPeriod)

        self.assertIsInstance(o.to_dict(), dict)
        self.assertIsInstance(o.to_str(), str)

        self.assertIsNone(o.period)
        self.assertIsNone(o.time_unit)
