# Will interact with the API
import requests
import eel
import rover_build as rb 

eel.init('web')

@eel.expose     
def set_rover(rover_name):
   rb.build_rover_r(rover_name)

@eel.expose 
def set_camera(camera):
   rb.build_rover_c(camera)
   
@eel.expose 
def query(value):
   rb.build_rover_q(value)

rb.default_rover()

eel.start("index.html", size=(800, 800))

