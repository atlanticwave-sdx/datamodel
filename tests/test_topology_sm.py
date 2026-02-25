import unittest

from sdx_datamodel.topology_sm import TopologyStateMachine


class TestTopologyStateMachine(unittest.TestCase):
    def setUp(self):
        self.sm = TopologyStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.sm.state, self.sm.State.START)

    def test_transition_start_to_oxp_update(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.OXP_UPDATE)

    def test_transition_start_to_error(self):
        self.sm.transition(self.sm.State.ERROR)
        self.assertEqual(self.sm.state, self.sm.State.ERROR)

    def test_invalid_transition_start_to_up(self):
        with self.assertRaises(ValueError):
            self.sm.transition(self.sm.State.UP)

    def test_transition_oxp_update_to_up(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.assertEqual(self.sm.state, self.sm.State.UP)

    def test_transition_up_to_oxp_update(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.OXP_UPDATE)

    def test_transition_up_to_prov_update(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.PROV_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.PROV_UPDATE)

    def test_transition_prov_update_to_up(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.PROV_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.assertEqual(self.sm.state, self.sm.State.UP)

    def test_transition_up_to_error(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.ERROR)
        self.assertEqual(self.sm.state, self.sm.State.ERROR)

    def test_transition_error_to_oxp_update(self):
        self.sm.transition(self.sm.State.ERROR)
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.OXP_UPDATE)

    def test_transition_up_to_maintenance(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.MAINTENANCE)
        self.assertEqual(self.sm.state, self.sm.State.MAINTENANCE)

    def test_transition_maintenance_to_up(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.MAINTENANCE)
        self.sm.transition(self.sm.State.UP)
        self.assertEqual(self.sm.state, self.sm.State.UP)

    def test_transition_up_to_deleted(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.DELETED)
        self.assertEqual(self.sm.state, self.sm.State.DELETED)

    def test_transition_error_to_deleted(self):
        self.sm.transition(self.sm.State.ERROR)
        self.sm.transition(self.sm.State.DELETED)
        self.assertEqual(self.sm.state, self.sm.State.DELETED)

    def test_transition_maintenance_to_deleted(self):
        self.sm.transition(self.sm.State.OXP_UPDATE)
        self.sm.transition(self.sm.State.UP)
        self.sm.transition(self.sm.State.MAINTENANCE)
        self.sm.transition(self.sm.State.DELETED)
        self.assertEqual(self.sm.state, self.sm.State.DELETED)


if __name__ == "__main__":
    unittest.main()
