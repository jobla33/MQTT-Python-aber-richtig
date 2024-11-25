import numpy as np
import time
import sqlite3
from database import get_latest_value, store_in_database

def ph(value):
    cal7 = 2053
    cal4 = 2458
    return 7.0 + (cal7 - value) / ((cal7 - cal4) / 3.0)

def calculate_scaled_response(setpoint, measured_value, factor):
    # Abweichung berechnen
    deviation = abs(setpoint - measured_value)
    
    # Skalierten Wert berechnen
    scaled_value = factor * deviation
    
    # Begrenzen auf den Bereich 0 bis 100
    return max(0, min(scaled_value, 100))

value = get_latest_value('sensor_data.db')
store_in_database(ph(value),'ph_data.db')
