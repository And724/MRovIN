import zmq
import random

# List of available rovers
rovers = ["Curiosity", "Opportunity", "Spirit", "Perseverance"]

cameras = {
  "Perseverance" :   ['edl_rucam', 'edl_rdcam', 'edl_ddcam', 'edl_pucam1', 'edl_pucam2', 
                    'navcam_left', 'navcam_right', 'mcz_right', 'mcz_left', 'front_hazcam_left_a', 
                    'front_hazcam_right_a', 'rear_hazcam_left', 'rear_hazcam_right', 'skycam', 'sherloc_watson'],
  "Curiosity"    :   ['fhaz', 'rhaz', 'mast', 'chemcam', 'mahli', 'mardi', 'navcam'],
  "Opportunity"  :   ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites'],
  "Spirit"       :   ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites']
}

def generate_random_query():
    # Generate a random Martian date (integer)
    random_date = random.randint(1, 1000)

    # Randomly select a rover
    selected_rover = random.choice(rovers)

    #Randomly select a camera
    selected_camera = random.choice(cameras[selected_rover])

    return {
        "date": random_date,
        "rover": selected_rover,
        "camera": selected_camera,
    }

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

