import zmq
import random

# List of available rovers
rovers = ["Curiosity", "Opportunity", "Spirit", "Perseverance"]

def generate_random_query():
    # Generate a random Martian date (integer)
    random_date = random.randint(1, 10000)

    # Randomly select a rover
    selected_rover = random.choice(rovers)

    return {
        "date": random_date,
        "rover": selected_rover,
    }

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Bind to port 5555

    print("Random Query Generator Microservice is ready to accept requests.")

    while True:
        message = socket.recv()
        print(f"Received request: {message}")

        if message == b"generate":
            random_query = generate_random_query()
            print(f"Sending response: {random_query}")
            socket.send_json(random_query)
        else:
            print("Invalid request")
            socket.send_string("Invalid request")

if __name__ == "__main__":
    main()
