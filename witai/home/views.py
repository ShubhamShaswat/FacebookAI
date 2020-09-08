from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
import json
from django.views import View

from wit import Wit
import cv2
import numpy as np
import base64

access_token = 'PFOUIZJHUCNPHTIUH4I3QC3U5LZDQCUN'


#function you need

#color dict

to_bgr = {'red' : (0,0,255),
            'black' : (0,0,0),
            'blue' : (255,0,0),
            'green' : (0,255,0)
        }


def draw_circle(color,radius=80,thickness=5):
    my_img = np.zeros((400, 400, 3), dtype = "uint8")
    my_img.fill(255)
    # creating circle
    frame = cv2.circle(my_img, (200, 200),radius, color, thickness)

    return frame



def draw_square(color):
    my_img = np.zeros((400, 400, 3), dtype = "uint8")
    my_img.fill(255)
    # creating a rectangle
    frame = cv2.rectangle(my_img, (200, 200), (300, 300), color, 5)
    return frame



#this will
def to_base64(frame):
     ret, frame_buff = cv2.imencode('.jpg', frame)
     frame_b64 = base64.b64encode(frame_buff)
     return frame_b64

def resolve_color(resp):

    if 'color:color' in resp['entities'] :
        if resp['entities']['color:color'] is not None:
            color = resp['entities']['color:color'][0]['value']
            return color

    return


#defaul home page
frame_b64 = to_base64(draw_circle(color=(0,0,0)))
context = {'text' : '','img': ('data:image/jpeg;base64, '+ frame_b64.decode("utf-8"))}

# Create your views here.


def home(request):


    if request.method == 'POST':
        #print(request.body)
        #f = open('./file.wav', 'wb')
        #f.write(request.body)
        #f.close()

        client = Wit(access_token)
        resp = None
        #with open('./file.wav', 'rb') as f:
        resp = client.speech(request.body, {'Content-Type': 'audio/wav'})


        print('Yay, got Wit.ai response: ' + str(resp))
        #print(resp['text'])

        #resolve intent
        intent = resp['intents'][0]['name']


        #resolve Color Entity

        color=(0,0,0)
        if resolve_color(resp) is not None:
            color = to_bgr[resolve_color(resp)]




        if intent == 'draw_square':
            frame_b64 = to_base64(draw_square(color=color))

        if intent == 'draw_circle':
            frame_b64 = to_base64(draw_circle(color=color))



        #context = {'text' : 'test','img': ('data:image/jpeg;base64, '+ frame_b64.decode("utf-8"))}
        context.update({'text': resp['text'],'img' :('data:image/jpeg;base64, '+ frame_b64.decode("utf-8"))})

        #return HttpResponseRedirect("/")
        #return JsonResponse(context)
        return redirect('/home')

    else:

        return render(request, 'home/home.html' ,context)
