# SMS Simulation

This project is a Python3-based SMS (Short Message Service) simulation that models the process of sending SMS messages. It includes various components such as producing messages, sending them, and monitoring the progress.

## Project Structure

- `sms_simulation.py`: The primary Python script containing the `SMSSimulation` class, which orchestrates the SMS simulation.
- `sms_simulation_test.py`: A test script containing unit tests for the `SMSSimulation` class.

## Getting Started

1. Clone the repository to your local machine.
2. Make sure you have Python3 installed.
3. To run the simulation, execute the following command:

```bash
python3 sms_simulation.py
```

## Configuration
You can customize the simulation's behavior by configuring the following parameters:

- **Number of Messages:** Specify the number of SMS messages to simulate (default is 1000).
- **Number of Sender Threads:** Determine the number of threads responsible for sending messages.
- **Mean Processing Time:** Define the mean processing time for each message in seconds.
- **Error Rate:** Set the probability of message transmission failure (0.0 to 1.0).
- **Progress Update Interval:** Control the interval for reporting progress updates.

## Usage

- Upon starting the simulation, it will prompt you to configure the simulation based on your requirements.

- The simulation will begin, and you will receive progress updates.

- Once the simulation is completed, you will have the option to start another simulation.


## Testing

The project includes a unit test suite in `sms_simulation_test.py`. You can run the tests using the following command:

```bash
python3 sms_simulation_test.py
```