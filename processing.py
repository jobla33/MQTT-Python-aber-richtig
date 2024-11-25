from database import get_latest_value, store_in_database

def ph(value):
    cal7 = 2053
    cal4 = 2458
    # Extract the numeric value from the tuple
    numeric_value = value[1] if isinstance(value, tuple) else value
    return 7.0 - (cal7 - numeric_value) / ((cal7 - cal4) / 3.0)

def main():
    value = get_latest_value('sensor_data.db')
    print(f"Sensorwert aus sensor_data entnommen: {value}")
    store_in_database(ph(value),'ph_data.db')
    print(f"pH-Wert in ph_data gespeichert: {ph(value)}")
