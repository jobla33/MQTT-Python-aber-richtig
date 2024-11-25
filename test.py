import time
import math
import random
import paho.mqtt.client as mqtt

# MQTT-Broker-Adresse (ersetzen, falls nötig)
BROKER = "localhost"
SENSOR_TOPIC = "esp32/sensor"
RESPONSE_TOPIC = "esp32/response"

# Parameter für die Werte
AMPLITUDE = 500  # Amplitude der Schwankung (2500-1500 -> 500)
BASE_VALUE = 2000  # Mittelwert der Schwankung
FREQUENCY = 0.1  # Frequenz der Sinuskurve

# Zufällige Phase (um den Startpunkt der Sinuskurve zu variieren)
phase = random.uniform(0, 2 * math.pi)

# MQTT-Callback-Funktion zum Empfangen der Antwort
def on_message(client, userdata, msg):
    print(f"Antwort empfangen auf {msg.topic}: {msg.payload.decode()}")

# MQTT-Client einrichten
client = mqtt.Client()
client.on_message = on_message

# Verbindung mit dem MQTT-Broker herstellen
client.connect(BROKER, 1883, 60)
client.loop_start()

# Abonniere das Antwort-Thema
client.subscribe(RESPONSE_TOPIC)

# Simuliere und sende Werte
try:
    while True:
        # Generiere einen schwankenden Wert (Sinuskurve mit Rauschen)
        current_time = time.time()
        sinus_value = math.sin(2 * math.pi * FREQUENCY * current_time + phase)
        sensor_value = int(BASE_VALUE + AMPLITUDE * sinus_value + random.uniform(-10, 10))  # Rauschen hinzufügen

        # Sende den Wert an den MQTT-Broker
        client.publish(SENSOR_TOPIC, sensor_value)
        print(f"Gesendeter Wert: {sensor_value}")

        # Warte 1 Sekunde
        time.sleep(1)
except KeyboardInterrupt:
    print("Beende Skript...")
    client.loop_stop()
    client.disconnect()
