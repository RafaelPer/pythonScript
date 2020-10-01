# Escreva o seu código aqui :-)
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
magSensorpin = 17
GPIO.setup(magSensorpin, GPIO.IN)
print("Sensor Iniciado")
time.sleep(2)
print("Sensor Ativo")

print(GPIO.input(magSensorpin))

def MOTION(pin):
    if GPIO.input(pin)==GPIO.HIGH:
        print("Porta Aberta")
        print(pin)
    else:
        print("Porta Fechada")
        print(pin)

    #GPIO.remove_event_detect(pin)

#def DONTMOTION(pin):
#    print("Não Detectado")
#    print(pin)
    #GPIO.remove_event_detect(pin)

try:
    GPIO.add_event_detect(magSensorpin, GPIO.BOTH, callback=MOTION)
    #GPIO.add_event_detect(pir, GPIO.RISING, callback=MOTION)
    #GPIO.add_event_detect(pir, GPIO.FALLING, callback=DONTMOTION)
    while True:
        #print(GPIO.input(pir))
        #if GPIO.input(pir)==True:
        #if GPIO.input(pir)==GPIO.HIGH:
        #    MOTION(pir)
        #    print("Movimento Detectado")
        #    time.sleep(1)
        #else:
        #    DONTMOTION(pir)
        #    print("Não Detectado")
        #    time.sleep(1)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup();
    print("Programa Finalizado");
