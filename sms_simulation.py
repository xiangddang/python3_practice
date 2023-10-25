import threading
import time
import random
import numpy as np


class SMSSimulation:
    def __init__(self):
        self.progress_condition = None
        self.progress_lock = None
        self.message_lock = None
        # Set num_messages default 1000
        self.num_messages = 1000
        self.message_queue = []
        self.messages_sent = 0
        self.messages_failed = 0
        self.total_processing_time = 0
        self.std_dev = 0.05

    # Initialize simulation parameters and counters
    def initialize_simulation(self):
        self.num_messages = 1000
        self.message_queue = []
        self.messages_sent = 0
        self.messages_failed = 0
        self.total_processing_time = 0

    # Message Producer Function
    def producer(self):
        for i in range(self.num_messages):
            # Generate a random message consisting of alphanumeric characters
            message = ''.join(
                random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(100))
            with self.message_lock:
                # Use a threading lock to ensure thread safety when adding messages to the queue
                self.message_queue.append(message)

    # Message Sender Function
    def sender(self, mean_processing_time, error_rate):
        while True:
            with self.message_lock:
                if not self.message_queue:
                    if self.messages_sent == self.num_messages:
                        break  # Exit if the simulation is completed
                    continue  # Keep checking for new messages
                self.message_queue.pop(0)
            # Using normal distribution to achieve that
            # "sending messages by waiting a random period of time distributed around a configurable mean".
            processing_time = max(0, np.random.normal(mean_processing_time, self.std_dev))
            time.sleep(processing_time)
            if random.random() < error_rate:
                self.messages_failed += 1
            # Count the number of messages sent
            self.messages_sent += 1
            self.total_processing_time += processing_time

    # Progress Monitor Function
    def progress_monitor(self, progress_update_interval):
        print("Monitor: SMS simulation is running...")
        while True:
            time.sleep(progress_update_interval)
            with self.progress_condition:
                with self.progress_lock:
                    average_time_per_message = self.total_processing_time / self.messages_sent if self.messages_sent > 0 else 0
                    print(f"Messages Successfully Sent: {self.messages_sent - self.messages_failed}, "
                          f"Messages Failed: {self.messages_failed}, "
                          f"Average Time per Message: {average_time_per_message:.4f} seconds")
            if self.messages_sent == self.num_messages:
                break  # Exit if the simulation is completed

    # Helper method to check the validation of input (float)
    # Normal it is better to remove these two helper function from the class,
    # for the convenience of tests, I put it here.
    def get_float_input(self, message, min_value=0, max_value=None):
        while True:
            try:
                value = float(input(message))
                if max_value is not None:
                    if min_value <= value < max_value:
                        return value
                    else:
                        print(f"Value must be between {min_value} and {max_value}.")
                elif value >= min_value:
                    return value
                else:
                    print(f"Value must be greater than or equal to {min_value}.")
            except ValueError:
                print("Please enter a valid number.")

    # Helper method to check the validation of input (int)
    def get_positive_integer_input(self, message):
        while True:
            try:
                value = int(input(message))
                if value > 0:
                    return value
                else:
                    print("Value must be greater than 0.")
            except ValueError:
                print("Please enter a valid positive integer.")

    def get_configurations(self):
        # Get all configurations needed
        # The setting of num_message is a bit different from others.
        num_messages_input = input("Enter the number of messages (or press Enter for default 1000): ")
        if num_messages_input:
            if int(num_messages_input) > 0:
                self.num_messages = int(num_messages_input)
            else:
                print("Invalid input, the number of messages are set to default 1000.")
        num_senders = self.get_positive_integer_input("Enter the number of sender threads: ")
        mean_processing_time = self.get_float_input("Enter the mean processing time (seconds): ", min_value=0.01)
        error_rate = self.get_float_input("Enter the error rate (0.0 to 1.0): ", min_value=0.0, max_value=1.0)
        progress_update_interval = self.get_positive_integer_input("Enter the progress update interval (seconds): ")

        return num_senders, mean_processing_time, error_rate, progress_update_interval

    def run_simulation(self):
        print("Welcome to use this SMS Simulation system!")
        while True:
            self.initialize_simulation()
            # Configuration input and simulation setup
            print("Please set up your costumer system.")
            num_senders, mean_processing_time, error_rate, progress_update_interval = self.get_configurations()

            print("Congratulations! The SMS simulation starts working.")
            print("Monitor: ")

            # Create thread locks and conditions for synchronization.
            self.message_lock = threading.Lock()
            self.progress_lock = threading.Lock()
            self.progress_condition = threading.Condition()

            # Start a producer thread to populate the message queue.
            producer_thread = threading.Thread(target=self.producer)
            producer_thread.start()

            # Create and start sender threads based on the specified number of senders.
            sender_threads = []
            for i in range(num_senders):
                sender_thread = threading.Thread(target=self.sender, args=(mean_processing_time, error_rate))
                sender_threads.append(sender_thread)
                sender_thread.start()

            # Start a progress monitor thread to track the simulation's progress.
            progress_monitor_thread = threading.Thread(target=self.progress_monitor, args=(progress_update_interval,))
            progress_monitor_thread.start()

            # Wait for threads to complete their execution.
            producer_thread.join()
            for sender_thread in sender_threads:
                sender_thread.join()
            progress_monitor_thread.join()

            print("Congratulations! The SMS simulation has completed.")

            # Ask if the user wants to start another simulation
            while True:
                user_input = input("Do you want to start another simulation? (yes/no): ")
                if user_input.lower() == "yes":
                    break
                elif user_input.lower() == "no":
                    print("Thank you for using the SMS Simulation system. Goodbye!")
                    return  # Exit the program if the user doesn't want to start another simulation
                else:
                    print("Please enter 'yes' or 'no'.")


# Run the SMS Simulation
if __name__ == '__main__':
    sms_simulation = SMSSimulation()
    sms_simulation.run_simulation()
