import unittest

from sdx_datamodel.topology_sm import TopologyStateMachine


class TestTopologyStateMachine(unittest.TestCase):
    def setUp(self):
        self.sm = TopologyStateMachine()

    def test_initial_state(self):
        self.assertEqual(self.sm.state, self.sm.State.START)

    def test_transition_start_to_db_update(self):
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.DB_UPDATE)

    def test_transition_start_to_orphaned(self):
        self.sm.transition(self.sm.State.ORPHANED)
        self.assertEqual(self.sm.state, self.sm.State.ORPHANED)

    def test_invalid_transition(self):
        with self.assertRaises(ValueError):
            self.sm.transition(self.sm.State.DELETED)

    def test_transition_db_update_to_db_update(self):
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.DB_UPDATE)

    def test_transition_db_update_to_orphaned(self):
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.sm.transition(self.sm.State.ORPHANED)
        self.assertEqual(self.sm.state, self.sm.State.ORPHANED)

    def test_transition_orphaned_to_db_update(self):
        self.sm.transition(self.sm.State.ORPHANED)
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.DB_UPDATE)

    def test_transition_db_update_to_deleted(self):
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.sm.transition(self.sm.State.DELETED)
        self.assertEqual(self.sm.state, self.sm.State.DELETED)

    def test_transition_orphaned_to_deleted(self):
        self.sm.transition(self.sm.State.ORPHANED)
        self.sm.transition(self.sm.State.DELETED)
        self.assertEqual(self.sm.state, self.sm.State.DELETED)

    def test_transition_db_update_to_maintenance(self):
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.sm.transition(self.sm.State.MAINTENANCE)
        self.assertEqual(self.sm.state, self.sm.State.MAINTENANCE)

    def test_transition_maintenance_to_db_update(self):
        self.sm.set_state(self.sm.State.DB_UPDATE)
        self.sm.transition(self.sm.State.MAINTENANCE)
        self.sm.transition(self.sm.State.DB_UPDATE)
        self.assertEqual(self.sm.state, self.sm.State.DB_UPDATE)


if __name__ == "__main__":
    unittest.main()
