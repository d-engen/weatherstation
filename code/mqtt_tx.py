import paho.mqtt.client as mqtt

# Skapa en MQTT-klient
client = mqtt.Client()

# Anslut till brokern
client.connect("test.mosquitto.org", 1883, 60)

# Starta loop för att hålla anslutningen igång
client.loop_start()

# Skicka ett meddelande till specificerad topic
result = client.publish("ei24/viktor", "san")

# Vänta tills meddelandet är skickat
result.wait_for_publish()

# Avsluta MQTT-klienten
client.loop_stop()
client.disconnect()
