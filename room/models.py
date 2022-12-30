import json

from django.db import models
import requests
# Create your models here.

class rooms(models.Model):
    room_id = models.IntegerField(primary_key=True)
    room_name = models.CharField(max_length=100)
    room_ip = models.CharField(max_length=100)
    ledState = models.BooleanField(default=False)
    doorState = models.BooleanField(default=False)
    alarmState = models.BooleanField(default=False)
    temperature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    bodySensor = models.BooleanField(default=False)

    def get_state_now(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        ip = room.room_ip
        s = requests.get(f'http://{ip}/')
        # формат полученных данных { "door": "0", "led": "1", "temperature": "23.90", "humidity": "19.00" "bodySensorPin": "1" "alarmState": "0" }
        s = s.text
        s = s.replace("\r", '').replace("\n", '')
        s = json.loads(s)
        # сохранение в базу данных
        room.ledState = True if s['led'] == '1' else False
        room.doorState = True if s['door'] == '1' else False
        room.temperature = float(s['temperature'])
        room.humidity = float(s['humidity'])
        room.bodySensor = True if s['bodySensorPin'] == "1" else False
        room.alarmState = True if s['alarmState'] == "1" else False
        room.save()
        return rooms.objects.get(room_id=room_id)

    def get_state_on_number(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        return room

    def get_ip_on_number(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        return room.room_ip

    def led_on(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.ledState = True
        room.save()
        requests.get(f'http://{room.room_ip}/led/on')

    def led_off(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.ledState = False
        room.save()
        requests.get(f'http://{room.room_ip}/led/off')

    def door_on(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.doorState = True
        room.save()
        requests.get(f'http://{room.room_ip}/door/on')

    def door_off(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.doorState = False
        room.save()
        requests.get(f'http://{room.room_ip}/door/off')

    def alarm_on(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.alarmState = True
        room.save()
        requests.get(f'http://{room.room_ip}/alarm/on')

    def alarm_off(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        room.alarmState = False
        room.save()
        requests.get(f'http://{room.room_ip}/alarm/off')

    def get_state(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        s = requests.get(f'http://{room.room_ip}/')
        # формат полученных данных { "door": "0", "led": "1", "temperature": "23.90", "humidity": "19.00" "bodySensorPin": "1" "alarmState": "0" }
        s = s.text
        s = json.loads(s)
        return s

    def get_state_all(self):
        rooms_list = rooms.objects.all()
        for room in rooms_list:
            s = requests.get(f'http://{room.room_ip}/')
            # формат полученных данных { "door": "0", "led": "1", "temperature": "23.90", "humidity": "19.00" "bodySensorPin": "1" "alarmState": "0" }
            s = s.text
            s = json.loads(s)
            room.ledState = s['led']
            room.doorState = s['door']
            room.temperature = s['temperature']
            room.humidity = s['humidity']
            room.bodySensor = s['bodySensorPin']
            room.alarmState = s['alarmState']
            room.save()

    def set_state_all(self):
        rooms_list = rooms.objects.all()
        for room in rooms_list:
            if room.ledState:
                requests.get(f'http://{room.room_ip}/led/on')
            else:
                requests.get(f'http://{room.room_ip}/led/off')
            if room.doorState:
                requests.get(f'http://{room.room_ip}/door/on')
            else:
                requests.get(f'http://{room.room_ip}/door/off')
            if room.alarmState:
                requests.get(f'http://{room.room_ip}/alarm/on')
            else:
                requests.get(f'http://{room.room_ip}/alarm/off')
    def get_dict_on_number(self, room_id):
        room = rooms.objects.get(room_id=room_id)
        return room.__dict__

