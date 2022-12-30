from django.shortcuts import render

# Create your views here.
import requests
import json
from . import models

models1 = models.rooms()

def room_detail(request, pk):
    if request.method == 'POST':
        if request.POST.get('light') != None:
            if request.POST.get('light') == 'Включить свет':
                models1.led_on(pk)
            else:
                models1.led_off(pk)
        if request.POST.get('door') != None:
            if request.POST.get('door') == 'Открыть дверь':
                models1.door_on(pk)
            else:
                models1.door_off(pk)
        if request.POST.get('alarm') != None:
            if request.POST.get('alarm') == 'Включить сигнализацию':
                models1.alarm_on(pk)
            else:
                models1.alarm_off(pk)
    models1.get_state_now(pk)
    room = models1.get_dict_on_number(pk)
    print(room)
    return render(request, 'room/room.html', room)

