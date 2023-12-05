import zmq 
import requests
from data_processing import receive_send_data
import random  

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5554")

rover_obj = None 

class Rover:
    
    nasa_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
    api_key = "bkBdrf86b939njkxnSw3kN1Qk6hb8rhgLKLpnT7C"

    def __init__(self, rover_name) -> None:
      self._rover_name = rover_name
      self._camera_name = None 
      self._url = None 
      self._data = None 

    def set_camera(self, camera):
      """
      Sets camera name.
      """
      self._camera_name = camera 
   
    def build_url(self, date_or_sol):
      """
      Generates the url for the API call.
      """
      if "-" in date_or_sol:
          url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&earht_date={date_or_sol}&camera={self._camera_name}'
      else:
         url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&sol={date_or_sol}&camera={self._camera_name}'
      self._url = url

    def api_call(self):
      """
      Makes call to API and returns the data.
      """
      response = requests.get(self._url)
      if response.status_code == 200:
         data = response.json()
         return data 
    
    def get_rover_name(self):
      """
      Returns rover name.
      """
      return self._rover_name

    def get_camera_name(self):
       """
       Returns name of current camera.
       """
       return self._camera_name



# ----- Necessary functions outside of Rover class. Communicates with -----
# ----- other modules and with eel_interaction.py via ZeroMQ.         -----


def build_rover_r(rover):
  """
  Initializes a new rover object and passes rover
  name to rover class.
  """
  global rover_obj 
  rover_obj = Rover(rover)
  print(rover_obj.get_rover_name())

def build_rover_c(camera):
   """
   Passes camera name to rover object.
   """
   global rover_obj
   rover_obj.set_camera(camera)
   print(rover_obj.get_camera_name())

def build_rover_q(query):
   """
   Passes user query to rover object. Gathers
   data from API to be processed. 
   """
   global rover_obj 
   rover_obj.build_url(query)
   data = rover_obj.api_call()
   
   if data == None or data["photos"] == []:
      new_query = probe_valid_query(query)
      build_rover_q(new_query)
   else:
      send_api_data(data)
  
def probe_valid_query(old_query):
# Try a while loop and timing how long this takes. If more than 15 seconds 
# default to latest photo. See if this can be done more efficiently maybe
# within the rover class call this external function and loop until something
# valid is found.
   old_query = int(old_query)
   if old_query >= 400:
      new_query = old_query - 6 * (random.randint(5, 10) ** 2)
      print(new_query)
      return str(new_query)
   elif 0 <= old_query < 400:
      new_query = old_query + 2 * (random.randint(1, 5) ** 2)
      print(new_query)
      return str(new_query)
   elif old_query < 0:
      return "0" 
  
       
def send_api_data(data):
   """
   Passes data to be parsed to data_processing
   """
   processed_data = receive_send_data(data)
   socket.send_json(processed_data)

def default_rover():
   """
   Establishes a default Rover upon launch of 
   the application.
   """
   global rover_obj
   if rover_obj is None:
      rover_obj = Rover("Perseverance")
      rover_obj.set_camera("EDL_RUCAM")
   
  

