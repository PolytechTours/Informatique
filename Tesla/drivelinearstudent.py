import argparse
import base64
from datetime import datetime
import os
import shutil

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO

sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None
DIM_VEC_Image=67200#67200#160*320*3

class SimplePIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.set_point = 0.
        self.error = 0.
        self.integral = 0.

    def set_desired(self, desired):
        self.set_point = desired

    def update(self, measurement):
        # proportional error
        self.error = self.set_point - measurement

        # integral error
        self.integral += self.error

        return self.Kp * self.error + self.Ki * self.integral


controller = SimplePIController(0.1, 0.002)

set_speed = 10 #20 is ok too
controller.set_desired(set_speed)

##################
# fonction telemetry
# à modifier par les étudiants
###########################
@sio.on('telemetry')
def telemetry(sid, data):
    global x,W
    if data:
        # The current steering angle of the car
        steering_angle = data["steering_angle"]
        # The current throttle of the car
        throttle = data["throttle"]
        #print("throttle", throttle)
        # The current speed of the car
        speed = data["speed"]
        # The current image from the center camera of the car
        imgString = data["image"]
        image = Image.open(BytesIO(base64.b64decode(imgString)))
        image_array = np.asarray(image)
        image_array=image_array[65:160-25,0:320-0]
        image_array=(image_array/127.5)-1
        
        x[0,0]=1
        x[0,1:DIM_VEC_Image+1]=image_array.reshape(DIM_VEC_Image)
		
		##########################################
		# Ici il faut prédire la valeur de l'angle
		# Et la sauvegarder dans la variable angle
		##########################################
        
		########        
        steering_angle=float(angle)

        throttle = controller.update(float(speed))

        print(steering_angle, throttle)
        send_control(steering_angle, throttle)


    else:
        # NOTE: DON'T EDIT THIS.
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
   
    #Chargement des W à partir du fichier texte 
    W=np.loadtxt("modelW.txt")
    # x vide pour une image dont on veut prédire l'angle
    x = np.zeros((1,DIM_VEC_Image+1))
    
    print(W.shape)
    
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
