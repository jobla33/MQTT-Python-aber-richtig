import sqlite3

# Funktion zum Speichern eines Wertes in der Datenbank
def store_in_database(value, database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (timestamp DATETIME, value REAL)''')
    c.execute("INSERT INTO sensor_data (timestamp, value) VALUES (datetime('now'), ?)", (value,))
    conn.commit()
    conn.close()

# Funktion zum Abrufen des neuesten Wertes aus der Datenbank
def get_latest_value(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result  # Gibt (timestamp, value) zurück oder None, wenn die Tabelle leer ist