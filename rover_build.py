import zmq 
import requests
import time
from datetime import datetime, timedelta, date   

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
      if date_or_sol == "latest_photos":
         url = f"{self.nasa_url}{self._rover_name.lower()}/latest_photos?api_key={self.api_key}"
      elif "-" in date_or_sol:
          url = f"{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&earht_date={date_or_sol}&camera={self._camera_name}"
      else:
         url = f"{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&sol={date_or_sol}&camera={self._camera_name}"
      self._url = url

    def api_call(self):
      """
      Makes call to API and returns the data.
      """
      response = requests.get(self._url)
      if response.status_code == 200:
         data = response.json()
         if "latest_photos" in data:
            data["photos"] = data.pop("latest_photos")
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
      probe_valid_query(query, data)
   else:
      data_extraction(data)
  
def probe_valid_query(initial_query, initial_data):
    print("Probing...")
    start_time = time.time()
    new_data = initial_data
    pos_counter = 1
    neg_counter = 1

    while new_data is None or new_data["photos"] == []:
        elapsed_time = time.time() - start_time

        if elapsed_time <= 10:
            if "-" not in initial_query:
                new_query = int(initial_query) + pos_counter
            else:
                new_query = datetime.strptime(initial_query, "%Y-%m-%d") + timedelta(days=pos_counter)
                new_query = new_query.strftime("%Y-%m-%d")
            rover_obj.build_url(str(new_query))
            new_data = rover_obj.api_call()
            pos_counter += 1
       
        elif 15 < elapsed_time <= 20:
            if "-" not in initial_query:
                new_query = int(initial_query) - neg_counter
            else:
                new_query = datetime.strptime(initial_query, "%Y-%m-%d") - timedelta(days=neg_counter)
                new_query = new_query.strftime("%Y-%m-%d")
            rover_obj.build_url(str(new_query))
            new_data = rover_obj.api_call()
            neg_counter += 1
        
        elif elapsed_time > 20:
            rover_obj.build_url("latest_photos")
            new_data = rover_obj.api_call()
    data_extraction(new_data)

def data_extraction(data):
    data_dict = {}
    if data["photos"] != []:
        data_dict["sol"] = data["photos"][0]["sol"]
        data_dict["earth_date"] = data["photos"][0]["earth_date"]
        data_dict["rover"] = data["photos"][0]["rover"]["name"]
        data_dict["camera"] = data["photos"][0]["camera"]["full_name"]
        data_dict["img_link"] = data["photos"][0]["img_src"]
        time_since_photo(data_dict)

def time_since_photo(data):
   photo_date = data["earth_date"]
   time_since_photo = datetime.strptime(str(date.today()), "%Y-%m-%d") - datetime.strptime(photo_date, "%Y-%m-%d")
   data["elapsed_days"] = str(time_since_photo.days)
   socket.send_json(data)

def default_rover():
   """
   Establishes a default Rover upon launch of 
   the application.
   """
   global rover_obj
   if rover_obj is None:
      rover_obj = Rover("Perseverance")
      rover_obj.set_camera("EDL_RUCAM")
   
  

