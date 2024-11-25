import paho.mqtt.client as mqtt
import numpy as np
from collections import deque
from database import store_in_database

# Median- und Durchschnittspuffer initialisieren
median_window = deque(maxlen=5)  # Medianfilter-Fenster
average_window = deque(maxlen=3)  # Floating Average-Fenster

# Medianfilter
def median_filter(new_value):
    median_window.append(new_value)
    return np.median(median_window)

# Floating Average
def floating_average(new_value):
    average_window.append(new_value)
    return sum(average_window) / len(average_window)

# Kombinierte Glättung
def process_sensor_data(sensor_value):
    median_value = median_filter(sensor_value)
    smoothed_value = floating_average(median_value)
    return smoothed_value

# MQTT-Callback-Funktionen
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT-Broker")
    client.subscribe("esp32/sensor")

def on_message(client, userdata, msg):
    try:
        # Sensordaten empfangen und verarbeiten
        sensor_value = int(msg.payload.decode())  # 12-Bit-Wert empfangen
        smoothed_value = round(process_sensor_data(sensor_value))  # Glätten
        print(f"Geglätteter Wert: {smoothed_value}")
        
        # Daten in der Datenbank speichern
        store_in_database(smoothed_value, 'sensor_data.db')
    except Exception as e:
        print(f"Fehler: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()