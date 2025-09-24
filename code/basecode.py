import os
import glob
import time
import paho.mqtt.client as mqtt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    try:
        f = open(device_file, 'r')
        lines = f.readlines()
    except:
        lines = "fel"
    finally:
        f.close()
        return lines


def read_wind_raw():
    try:
        with open("/dev/ttyACM0", "r") as k:
            ex = k.readline().strip() 
            if ex.find('.'):    
                value = ex             
                rounded_val = round(value, 1) 
            else:
                rounded_val = -1
    except:
        rounded_val = "fel"               
    return rounded_val                     

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        rounded_val = round(temp_c, 1)
        return rounded_val
    


def mqtt_sensor(sens1, sens2):
    # Skapa en MQTT-klient
    client = mqtt.Client()

    # Anslut till brokern
    client.username_pw_set("elektronik", "elektronik")
    client.connect("100.82.0.4", 1883, 60)

    # Starta loop för att hålla anslutningen igång
    client.loop_start()

    # Skicka ett meddelande till specificerad topic
    result = client.publish("pi10/sensor/1", sens1)
    result = client.publish("pi10/sensor/2", sens2)

    # Vänta tills meddelandet är skickat
    result.wait_for_publish()

    # Avsluta MQTT-klienten
    client.loop_stop()
    client.disconnect()

while True:
    
    wind = read_wind_raw()
    temp = read_temp()

    #mqtt_sensor(wind, temp)

    #time.sleep(10)

    print(f'vindhastighet: {wind}m/s')

    print(f'Rummet är {temp}c')
    time.sleep(0.1)
