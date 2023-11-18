# Random Date Microservice 
The script, random.py, generates a random date after receiving input from the user. Communication between this microservice and the requesting program/script is done via ZeroMQ (https://zeromq.org/get-started/). Here the microservice is the server that will be reading a message from the requesting program, the client. The response from the server will then be sent to the client for processing.  

# Usage
The requesting program will need to have access to the ZeroMQ library. The microservice is written in Python so the appropriate library must be imported. Please see the link above to ZeroMQ documentation for other languages. 

If using python import the following for your requesting program and set up the socket: 
```
import zmq  
context = zmq.Context()    
socket = context.socket(zmq.REQ)  
socket.connect("tcp://localhost:5555")
``` 

To send a request, a message must be sent to the server. In the case of this microservice the message is "random":  
`socket.send(b"random")`  

After the microservice receives the request, it will generate a response. To receive the response do the following:  
`response = socket.recv_string()`

# Example Call
```
random_input = input("Please enter 'random' if you would like a random date generated: ")

if random_input.lower() == 'random':  
    socket.send(b"random")
    response = socket.recv_string()
    print(f"Date: {response}")
```

# UML Diagram 

![image](https://github.com/And724/MRovIN/assets/108034964/7f4a9171-042c-4149-b291-21fe72f2d3d3)






