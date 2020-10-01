import requests
import sqlite3
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from requests import Request, Session
from threading import Thread
import json
import os
import glob

sensor = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BCM)
magSensorJnlPin = 27
magSensorPtaPin = 17
proxSensor = 22
tempSensorDHT22 = 23
GPIO.setup(proxSensor, GPIO.IN)
GPIO.setup(magSensorJnlPin, GPIO.IN)
GPIO.setup(magSensorPtaPin, GPIO.IN)
print("Sensor Iniciado")
time.sleep(2)
print("Sensor Ativo")
url = 'http://192.168.0.240:9999/api/'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def PORTA(pin, itns):
    for i in itns:
        print(i)
        if GPIO.input(pin)==GPIO.HIGH:
            print("Porta Aberta")
            print(pin)
            obj = {
                "statusPortaComodo": False
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)
        else:
            print("Porta Fechada")
            print(pin)
            obj = {
                "statusPortaComodo": True
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)


def JANELA(pin, itns):
    for i in itns:
        print(i)
        if GPIO.input(pin)==GPIO.HIGH:
            print("Janela Aberta")
            print(pin)
            obj = {
                "statusJanelaComodo": False
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)
        else:
            print("Janela Fechada")
            print(pin)
            obj = {
                "statusJanelaComodo": True
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)

def MOTION(pin, itns):
    for i in itns:
        print(i)
        if GPIO.input(pin)==GPIO.HIGH:
            print("Movimento Detectado")
            print(pin)
            obj = {
                "statusPresencaComodo": True
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)
        else:
            print("Não Detectado")
            print(pin)
            obj = {
                "statusPresencaComodo": False
            }
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)

def TEMPDHT22(s, tpsdht22, itns):
    umid, temp = Adafruit_DHT.read_retry(s, tpsdht22);
    temp_c = read_temp()
    #print("Te: " + str(temp_c))
    if umid is not None and temp is not None:
        print ("Umidade: " + str(round(umid, 2)) + "\nTemperatura: " + str(round(temp, 2)))
        print("Te: " + str(temp_c))
        t = (temp + temp_c) / 2
        print("T: " + str(round(t, 2)))
        for i in itns:
            #print ("Umidade: " + str(round(umid, 2)) + "\nTemperatura: " + str(round(temp, 2)))
            #print(i)
            obj = {
                "tempComodo": str(round(t, 2)),
                "umiComodoF": str(round(umid, 2))
            }
            print(obj)
            try:
                Thread(target=UPDATEMONGODB, args=(i[1], i[3], obj)).start()
                Thread(target=UPDATESQLITE, args=(i[1], i[3], obj)).start()
            except Exception as e:
                print(e)

    else:
        # Mensagem de erro de comunicacao com o sensor
        print("Falha ao ler dados do sensor !!!")


def UPDATESQLITE(idCom, token, obj):
    #r = requests.get(url=url+'getAllComodos')
    s = Session()
    #t = {
    #    "t": "ffff"
    #}
    #req = Request(method="PUT", url=url+'updateBYIDComodo/'+idCom, data=json.dumps(obj), headers={'x-access-token': token})
    req = Request(method="PUT", url=url+'updateBYIDMCSQLite/'+idCom, json=obj, headers={'x-access-token': token})
    prepped = req.prepare()
    print(prepped.body)
    print(prepped.headers)
    resp = s.send(prepped)
    print(resp.json())
    #respo = requests.put(url=url+'updateBYIDComodo/'+idCom, data=json.dumps(obj), headers={'x-access-token': token})
    #print(respo.history[-1])
    #print(respo.json())
    #s = requests.Session()
    #r = requests.Request(method='PUT', url=url+'updateBYIDComodo/'+idCom, headers={'x-access-token': token}, data=json.dumps(obj))
    #print("Body: " + r.prepare().body)
    #resp = s.send(r)
    #print()

def UPDATEMONGODB(idCom, token, obj):
    #print(idCom)
    #print(token)
    #print(obj)
    s = Session()
    #t = {
    #    "t": "ffff"
    #}
    #req = Request(method="PUT", url=url+'updateBYIDComodo/'+idCom, data=json.dumps(obj), headers={'x-access-token': token})
    req = Request(method="PUT", url=url+'updateBYIDComodo/'+idCom, json=obj, headers={'x-access-token': token})
    prepped = req.prepare()
    print(prepped.body)
    print(prepped.headers)
    resp = s.send(prepped)
    print(resp.json())
    #respo = requests.put(url=url+'updateBYIDComodo/'+idCom, data=json.dumps(obj), headers={'x-access-token': token})
    #print(respo.history[-1])
    #print(respo.json())
    #s = requests.Session()
    #r = requests.Request(method='PUT', url=url+'updateBYIDComodo/'+idCom, headers={'x-access-token': token}, data=json.dumps(obj))
    #print("Body: " + r.prepare().body)
    #resp = s.send(r)
    #print()

def GETCOMBYID(idCom, token):
    print(idCom)
    print(token)
    #respo = requests.put(url=url+'updateBYIDComodo/'+idCom, data=json.dumps(obj), headers={'x-access-token': token})
    #print(respo.history[-1])
    print(respo.json())

try:
    # conectando...
    #conn = sqlite3.connect('/home/pi/Desktop/projetoSmartHomeFema4BCC/SocketServer/dbParear.sqlite')
    conn = sqlite3.connect('../SocketServer/dbParear.sqlite')
    # definindo um cursor
    cursor = conn.cursor()

    # lendo os dados
    cursor.execute("SELECT * FROM smh_Com;")

    itens = cursor.fetchall()

    GPIO.add_event_detect(magSensorJnlPin, GPIO.BOTH, callback=lambda x: JANELA(magSensorJnlPin, itens))
    GPIO.add_event_detect(magSensorPtaPin, GPIO.BOTH, callback=lambda x: PORTA(magSensorPtaPin, itens))
    GPIO.add_event_detect(proxSensor, GPIO.BOTH, callback=lambda x: MOTION(proxSensor, itens))
    while True:
        TEMPDHT22(sensor, tempSensorDHT22, itens)
#        if itens != None:
#            for dbItem in itens:
#                print(dbItem)
#        else:
#            print("Nenhum Comodo Pareado")

        cursor.execute("SELECT * FROM smh_Com;")
        itens = cursor.fetchall()
        time.sleep(2)

    # if itens != None:
    #     for dbItem in itens:
    #         print(dbItem)
    # else:
    #     print("Nenhum Comodo Pareado")


    # r = requests.get(url=url+'getAllComodos')

    # print(r.text)
except KeyboardInterrupt:
    print("Encerrando Programa")
    conn.close()
    GPIO.cleanup();