import unittest

from src.sdx_datamodel.connection_sm import ConnectionStateMachine

class TestConnectionStateMachine(unittest.TestCase):

    def setUp(self):
        self.sm = ConnectionStateMachine()
        self.State = ConnectionStateMachine.State

    def test_initial_state(self):
        self.assertEqual(self.sm.get_state(), self.State.REQUESTED)

    def test_valid_transition(self):
        self.sm.set_state(self.State.REQUESTED)
        self.sm.transition(self.State.PROVISIONING)
        self.assertEqual(self.sm.get_state(), self.State.PROVISIONING)

    def test_invalid_transition(self):
        self.sm.set_state(self.State.REQUESTED)
        with self.assertRaises(ValueError):
            self.sm.transition(self.State.PROVISIONED)

    def test_reset(self):
        self.sm.set_state(self.State.PROVISIONING)
        self.sm.reset()
        self.assertEqual(self.sm.get_state(), self.State.REQUESTED)

    def test_provision_success(self):
        self.sm.set_state(self.State.PROVISIONING)
        self.sm.transition(self.State.PROVISIONED)
        self.assertEqual(self.sm.get_state(), self.State.PROVISIONED)

    def test_provision_fail(self):
        self.sm.set_state(self.State.PROVISIONING)
        self.sm.transition(self.State.PROVISION_FAILED)
        self.assertEqual(self.sm.get_state(), self.State.PROVISION_FAILED)

    def test_modify_success(self):
        self.sm.set_state(self.State.PROVISIONED)
        self.sm.transition(self.State.MODIFYING)
        self.sm.transition(self.State.PROVISIONED)
        self.assertEqual(self.sm.get_state(), self.State.PROVISIONED)

    def test_modify_fail(self):
        self.sm.set_state(self.State.PROVISIONED)
        self.sm.transition(self.State.MODIFYING)
        self.sm.transition(self.State.PROVISION_FAILED)
        self.assertEqual(self.sm.get_state(), self.State.PROVISION_FAILED)

    def test_fail_and_recover(self):
        self.sm.set_state(self.State.PROVISIONED)
        self.sm.transition(self.State.FAILED)
        self.assertEqual(self.sm.get_state(), self.State.FAILED)
        self.sm.transition(self.State.RECOVERING)
        self.sm.transition(self.State.PROVISIONED)
        self.assertEqual(self.sm.get_state(), self.State.PROVISIONED)

    def test_delete(self):
        self.sm.set_state(self.State.PROVISIONED)
        self.sm.transition(self.State.DELETED)
        self.assertEqual(self.sm.get_state(), self.State.DELETED)

if __name__ == '__main__':
    unittest.main()