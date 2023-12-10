# Will interact with the API
import eel
import rover_build as rb
import zmq  

eel.init("web")


# ----- Communication between Python backend and JavaScript frontend -----

@eel.expose     
def set_rover(rover_name):
   """
   Passes user selected rover name to rover_build.py.
   """
   rb.build_rover_r(rover_name)

@eel.expose 
def set_camera(camera):
   """
   Passes user selected camera name to rover_build.py.
   """
   rb.build_rover_c(camera)
   
@eel.expose 
def query(value):
   """
   Passes user query to rover_build.py. Begins building the actual
   data to be retrieved. 
   """
   rb.build_rover_q(value)
   receive_api_data()

@eel.expose
def random_query():
   """
   Sends message to microservice to receive a json with 
   the relevant data to generate a random query.
   """
   print("Loading....")
   context = zmq.Context()
   socket = context.socket(zmq.REQ)
   socket.connect("tcp://localhost:5555")
   socket.send(b"generate")
   response = socket.recv_json()
   rb.build_rover_r(response["rover"])
   rb.build_rover_c(response["camera"])
   rb.build_rover_q(str(response["date"]))
   print(response)
   receive_api_data()

def send_packaged_data(data):
   """
   Sends packaged data to JavaScript for final processing
   and display to the user.
   """
   eel.displayData(data)

# ----- Communication with other python modules and other necessary functions ----- 

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5554")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

def receive_api_data():
    """
    Receives relevant data to be served to the user 
    on the frontend.
    """
    message = socket.recv_json()
    send_packaged_data(message)
    print(message)

rb.default_rover()

eel.start("index.html", size=(800, 800))