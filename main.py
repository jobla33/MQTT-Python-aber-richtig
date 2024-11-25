import paho.mqtt.client as mqtt
from collections import deque
import sqlite3
import numpy as np
import time  # Für die Endlosschleife

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

def ph(value):
    cal7 = 2053
    cal4 = 2458
    return 7.0 + (cal7 - value) / ((cal7 - cal4) / 3.0)


# Speicherung in der Datenbank
def store_in_database(value):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (timestamp DATETIME, value REAL)''')
    c.execute("INSERT INTO sensor_data (timestamp, value) VALUES (datetime('now'), ?)", (value,))
    conn.commit()
    conn.close()

# MQTT-Callback-Funktionen
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT-Broker")
    client.subscribe("esp32/sensor")

def calculate_scaled_response(setpoint, measured_value, factor):
    # Abweichung berechnen
    deviation = abs(setpoint - measured_value)
    
    # Skalierten Wert berechnen
    scaled_value = factor * deviation
    
    # Begrenzen auf den Bereich 0 bis 100
    return max(0, min(scaled_value, 100))

# Globale Variable für Zeitsteuerung
last_response_time = 0  # Zeitpunkt der letzten Antwort
response_interval = 10  # Intervall in Sekunden für das Senden von Antworten

def on_message(client, userdata, msg):
    global last_response_time
    try:
        # Sensordaten empfangen und verarbeiten
        sensor_value = int(msg.payload.decode())  # 12-Bit-Wert empfangen
        smoothed_value = round(process_sensor_data(sensor_value))  # Glätten
        print(f"Geglätteter Wert: {smoothed_value}")
        print(f"pH-Wert: {ph(smoothed_value)}")
        
        # Daten in der Datenbank speichern
        store_in_database(ph(smoothed_value))
        
        # Antwort basierend auf den geglätteten Daten
        current_time = time.time()
        if current_time - last_response_time >= response_interval:
            response = calculate_response(ph(smoothed_value))
            client.publish("esp32/response", response)  # Antwort senden
            last_response_time = current_time
    except Exception as e:
        print(f"Fehler: {e}")

# Berechnung der Antwort
def calculate_response(value):
    max_ph = 6.0
    min_ph = 5.0
    factor = 10
    if value > max_ph:
        if value - max_ph < 0.5:
            return f"p1,v,{calculate_scaled_response(max_ph,value,factor/10)},10"
        return f"p1,v,100,{calculate_scaled_response(max_ph,value,factor)}"
    elif value < min_ph:
        if min_ph - value < 0.5:
            return f"p2,v,{calculate_scaled_response(max_ph,value,factor/10)},10"
        return f"p2,v,100,{calculate_scaled_response(max_ph,value,factor)}"
    return "No action"

# MQTT-Client einrichten
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()  # Startet die Hintergrundschleife für MQTT

# Endlosschleife hinzufügen
try:
    print("Skript läuft... Drücke STRG+C, um zu beenden.")
    while True:
        time.sleep(1)  # Halte das Skript aktiv, ohne CPU zu belasten
except KeyboardInterrupt:
    print("Beende Skript...")
    client.loop_stop()  # Stoppe die MQTT-Schleife
    client.disconnect()  # Trenne die Verbindung zum Broker
