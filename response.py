from database import get_latest_value

def calculate_scaled_response(setpoint, measured_value, factor):
    # Abweichung berechnen
    deviation = abs(setpoint - measured_value)
    
    # Skalierten Wert berechnen
    scaled_value = factor * deviation
    
    # Begrenzen auf den Bereich 0 bis 100
    return max(0, min(scaled_value, 100))

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

def main():   
    ph = get_latest_value('ph_data.db')
    return calculate_response(float(ph[1]))