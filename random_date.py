import zmq 
import random
from datetime import datetime
import time 

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def random_date(start_date = datetime(1958, 7, 29), end_date = datetime(2023, 7, 29)):
    """
    Generates a random date between the day NASA was founded 
    up to July of the most recent year.  
    """
    date_range = end_date - start_date
    random_date = start_date + (date_range) * random.random()
    random_date = random_date.date()
    return str(random_date)

while True:
    print("Listening for request...")
    message = socket.recv_string()
    time.sleep(1)
    print(f"Request received: {message}")

    if message == "random":
        time.sleep(1)
        print("Generating random date...")
        date = random_date()
        socket.send_string(date)
        time.sleep(1)
        print(date)
    else:
        print("Input error. Please review input or requesting function.")
        socket.send_string("Invalid Request")
