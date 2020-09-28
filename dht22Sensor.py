# Carrega as bibliotecas
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
# Define o tipo de sensor
# sensor = Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BCM)
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 23
# Informacoes iniciais
print ("Aguardando Temperatura...");
while(1):
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
    # Caso leitura esteja ok, mostra os valores na tela
    if umid is not None and temp is not None:
        print ("Umidade: " + str(round(umid, 2)) + "\nTemperatura: " + str(round(temp, 2)))

    else:
        # Mensagem de erro de comunicacao com o sensor
        print("Falha ao ler dados do sensor !!!")

    time.sleep(2)