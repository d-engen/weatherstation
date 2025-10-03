import os
import glob
import time
import paho.mqtt.client as mqtt

os.system('modprobe w1-gpio') # Aktivera GPIO för 1-wire
os.system('modprobe w1-therm') # Aktivera termometerdrivrutin för 1-wire

# Bas-katalog där temperaturgivare finns i filsystemet
base_dir = '/sys/bus/w1/devices/' 
# Hitta första enheten som börjar med "28" (DS18B20 sensor börjar med 28)
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave' # Fil där temperaturen läses från


# Funktion för att läsa rådata från temperatursensorn
# Öppnar filen för att läsa alla rader. Hanterar eventuella fel vid filöppning
# Returnerar en lista med rader från filen eller strängen "fel" vid fel

def read_temp_raw():
    """Läser rådata av temperaturen"""
    try:
        f = open(device_file, 'r')
        lines = f.readlines()
    except:
        lines = "fel"               
    finally:
        f.close()       
        return lines            

# Läser vindhastighet från en seriell enhet (/dev/ttyACM0)
# Läser en rad i taget och försöker konvertera till float.
# Felhantering om värdet är mindre än 0.4 m/s
# Om läsningen inte går att konvertera till float läser funktionen om det.

def read_wind_raw():
    while True:
        with open("/dev/ttyACM0", "r") as k:
            line = k.readline().strip()
        try:
            if float(line) < 0.4:
                return 0.0
            else:
                return float(line)
        except ValueError:
            continue                

# Tolkar rådata från temperaturfilen och extraherar temperaturvärdet.
# Kontrollerar att CRC-kontrollen i första raden är godkänd ("YES")
# Hämtar temperaturvärdet från adnra raden och konverterar till Celsius
# Returnerar temperaturvärdet avrundat till en decimal

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
    

# Skapar en MQTT-klient och ansluter till en broker med användarnamn
# och lösenord.
# Startar en loop för att hålla anslutningen aktiv
# Publicerar värdet från båda sensorerna (sens1 och sens2) på varsin MQTT-topic
# Väntar till meddelandena är skickade, stoppar loopen och kopplar från broker

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

# Huvudprogram som kör en evig loop 

while True:

    wind = read_wind_raw()
    temp = read_temp()

    mqtt_sensor(wind, temp)

    print(f'vindhastighet: {wind}m/s')

    print(f'Rummet är {temp}c')

    time.sleep(1)
