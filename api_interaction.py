# Will interact with the API
import requests
import eel

eel.init('web')

#nasa_url = "https://api.nasa.gov/mars-photos/"
#api_key = "bkBdrf86b939njkxnSw3kN1Qk6hb8rhgLKLpnT7C"

class Rover:

   nasa_url = "https://api.nasa.gov/mars-photos/api/v1/rovers"
   api_key = "bkBdrf86b939njkxnSw3kN1Qk6hb8rhgLKLpnT7C"

   def __init__(self, rover_name) -> None:
      self._rover_name = rover_name

   def print_name(self):
      return self._rover_name
   
   def current_camera(self, camera):
      self._current_camera = camera 
      return self._current_camera
   
   def build_url(self, date_or_sol, camera):
      if "-" in date_or_sol:
          url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&sol={date_or_sol}&camera={camera}'
      else:
         url = f'{self.nasa_url}{self._rover_name.lower()}/photos?api_key={self.api_key}&earth_date={date_or_sol}&camera={camera}'

@eel.expose     
def set_rover(rover_name):
   rover = Rover(rover_name)
   print(rover.print_name())

def set_camera():
   """TODO"""
   pass

def date_query():
   """TODO"""
   pass

eel.start("index.html", size=(800, 800))

