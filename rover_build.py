rover_obj = None 

class Rover:
    
    nasa_url = "https://api.nasa.gov/mars-photos/api/v1/rovers"
    api_key = "bkBdrf86b939njkxnSw3kN1Qk6hb8rhgLKLpnT7C"

    def __init__(self, rover_name) -> None:
      self._rover_name = rover_name
      self._camera_name = None 
      self._url = None 

    def print_name(self):
      return self._rover_name
   
    def current_camera(self, camera):
      self._current_camera = camera 
      return self._current_camera
   
    def build_url(self, date_or_sol):
      if "-" in date_or_sol:
          url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&sol={date_or_sol}&camera={self._camera_name}'
      else:
         url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&earth_date={date_or_sol}&camera={self._camera_name}'
      self._url = url
      return self._url

    def print_query(self, query):
       print(query)

def build_rover_r(rover):
  global rover_obj 
  rover_obj = Rover(rover)
  print(rover_obj)

def build_rover_c(camera):
   global rover_obj
   print(rover_obj.current_camera(camera))

def build_rover_q(query):
   print(rover_obj.print_query(query))


def default_rover():
   global rover_obj
   if rover_obj is None:
      rover_obj = Rover("Perseverance")
      rover_obj.current_camera("EDL_RUCAM")
   
  

