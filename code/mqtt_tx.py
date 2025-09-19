import paho.mqtt.client as mqtt

# Skapa en MQTT-klient
client = mqtt.Client()

# Anslut till brokern
client.username_pw_set("elektronik", "elektronik")
client.connect("100.82.0.4", 1883, 60)

# Starta loop för att hålla anslutningen igång
client.loop_start()

# Skicka ett meddelande till specificerad topic
result = client.publish("pi10/sensor/1", 70)

# Vänta tills meddelandet är skickat
result.wait_for_publish()

# Avsluta MQTT-klienten
client.loop_stop()
client.disconnect()
