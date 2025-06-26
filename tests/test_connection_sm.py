import unittest

from src.sdx_datamodel.connection_sm import (
    ConnectionSMException,
    ConnectionStateMachine,
)


class TestConnectionStateMachine(unittest.TestCase):

    def setUp(self):
        self.sm = ConnectionStateMachine()
        self.State = ConnectionStateMachine.State

    def test_initial_state(self):
        self.assertEqual(self.sm.get_state(), self.State.REQUESTED)

    def test_valid_transition(self):
        self.sm.set_state(self.State.REQUESTED)
        self.sm.transition(self.State.UNDER_PROVISIONING)
        self.assertEqual(self.sm.get_state(), self.State.UNDER_PROVISIONING)

    def test_invalid_transition(self):
        self.sm.set_state(self.State.REQUESTED)
        with self.assertRaises(ConnectionSMException):
            self.sm.transition(self.State.UP)

    def test_reset(self):
        self.sm.set_state(self.State.UP)
        self.sm.reset()
        self.assertEqual(self.sm.get_state(), self.State.REQUESTED)

    def test_provision_success(self):
        self.sm.set_state(self.State.UNDER_PROVISIONING)
        self.sm.transition(self.State.UP)
        self.assertEqual(self.sm.get_state(), self.State.UP)

    def test_provision_fail(self):
        self.sm.set_state(self.State.UNDER_PROVISIONING)
        self.sm.transition(self.State.DOWN)
        self.assertEqual(self.sm.get_state(), self.State.DOWN)

    def test_modify_success(self):
        self.sm.set_state(self.State.UP)
        self.sm.transition(self.State.MODIFYING)
        self.sm.transition(self.State.UNDER_PROVISIONING)
        self.assertEqual(self.sm.get_state(), self.State.UNDER_PROVISIONING)

    def test_modify_fail(self):
        self.sm.set_state(self.State.UP)
        self.sm.transition(self.State.MODIFYING)
        self.sm.transition(self.State.DOWN)
        self.assertEqual(self.sm.get_state(), self.State.DOWN)

    def test_fail_and_recover(self):
        self.sm.set_state(self.State.UP)
        self.sm.transition(self.State.ERROR)
        self.assertEqual(self.sm.get_state(), self.State.ERROR)
        self.sm.transition(self.State.RECOVERING)
        self.sm.transition(self.State.UNDER_PROVISIONING)
        self.sm.transition(self.State.UP)
        self.assertEqual(self.sm.get_state(), self.State.UP)

    def test_delete(self):
        self.sm.set_state(self.State.UP)
        self.sm.transition(self.State.DELETED)
        self.assertEqual(self.sm.get_state(), self.State.DELETED)


if __name__ == "__main__":
    unittest.main()
