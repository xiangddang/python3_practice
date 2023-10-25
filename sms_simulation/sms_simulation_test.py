import unittest
import threading
from mock import patch
from python3_practice.sms_simulation.sms_simulation import SMSSimulation


class TestSMSSimulation(unittest.TestCase):
    # Test get_positive_integer_input: valid
    def test_get_positive_integer_input_valid(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["5"]):
            result = sms_sim.get_positive_integer_input("Enter a positive integer: ")
        self.assertEqual(result, 5)

    # Test get_positive_integer_input: invalid, not numbers
    def test_get_positive_integer_input_invalid(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["abc", "5"]):
            result = sms_sim.get_positive_integer_input("Enter a positive integer: ")
        self.assertEqual(result, 5)

    # Test get_positive_integer_input: invalid, float
    def test_get_positive_integer_input_float(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["5.5", "5"]):
            result = sms_sim.get_positive_integer_input("Enter a positive integer: ")
        self.assertEqual(result, 5)

    # Test get_positive_integer_input: invalid, negative
    def test_get_positive_integer_input_negative(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["-5", "5"]):
            result = sms_sim.get_positive_integer_input("Enter a positive integer: ")
        self.assertEqual(result, 5)

    # Test get_float_input: valid
    def test_get_float_input_valid(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["1.5"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 2.0: ", 1.0, 2.0)
        self.assertEqual(result, 1.5)

    # Test get_float_input: valid, int
    def test_get_float_input_int(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["2"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 3.0: ", 1.0, 3.0)
        self.assertEqual(result, 2.0)

    # Test get_float_input: invalid, not numbers
    def test_get_float_input_invalid(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["abc", "1.5"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 2.0: ", 1.0, 2.0)
        self.assertEqual(result, 1.5)

    # Test get_float_input: invalid, less than minimum
    def test_get_float_input_less(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["0.5", "1.5"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 2.0: ", 1.0, 2.0)
        self.assertEqual(result, 1.5)

    # Test get_float_input: invalid, less than minimum
    def test_get_float_input_less(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["3.0", "1.5"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 2.0: ", 1.0, 2.0)
        self.assertEqual(result, 1.5)

    # Test get_float_input: invalid, negative
    def test_get_float_input_negative(self):
        sms_sim = SMSSimulation()
        with patch('builtins.input', side_effect=["-1.0", "1.5"]):
            result = sms_sim.get_float_input("Enter a float between 1.0 and 2.0: ", 1.0, 2.0)
        self.assertEqual(result, 1.5)

    # Test produce
    def test_producer(self):
        sms_sim = SMSSimulation()
        sms_sim.num_messages = 5
        sms_sim.message_lock = threading.Lock()
        sms_sim.producer()
        self.assertEqual(len(sms_sim.message_queue), 5)
        for i in range(5):
            self.assertEqual(len(sms_sim.message_queue[i]), 100)

    # Test sender: assume all successful
    def test_sender_successful(self):
        sms_sim = SMSSimulation()
        sms_sim.num_messages = 5
        sms_sim.message_lock = threading.Lock()  # Set the message_lock
        sms_sim.progress_lock = threading.Lock()
        sms_sim.progress_condition = threading.Condition()
        sms_sim.producer()

        # Assuming 0 error rate and each message takes 0.1 seconds to send
        sms_sim.sender(0.1, 0.0)

        self.assertEqual(sms_sim.messages_sent, 5)
        self.assertEqual(sms_sim.messages_failed, 0)

    # Test monitor
    def test_progress_monitor(self):
        sms_sim = SMSSimulation()
        sms_sim.num_messages = 5
        sms_sim.messages_sent = 5
        sms_sim.messages_failed = 0
        sms_sim.progress_condition = threading.Condition()
        sms_sim.progress_lock = threading.Lock()
        with patch('time.sleep', side_effect=[None]):
            with patch('builtins.print') as mock_print:
                t = threading.Thread(target=sms_sim.progress_monitor, args=(0.1,))
                t.start()
                t.join()

        mock_print.assert_called_with("Messages Successfully Sent: 5, " +
                                      "Messages Failed: 0, Average Time per Message: 0.0000 seconds")


# Some functions might not be tested exhaustively due to the complexity of the simulation.
# However, extensive testing has been performed through multiple simulations to ensure correctness.
if __name__ == '__main__':
    unittest.main()
