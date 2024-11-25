import multiprocessing
import time
import mqtt
import processing 

def run_mqtt():
        mqtt.main()  # Assuming mqtt.py has a main function to run the loop

def run_processing():
    while True:
        processing.main()  # Assuming processing.py has a main function to process data
        time.sleep(3)

if __name__ == "__main__":
    mqtt_process = multiprocessing.Process(target=run_mqtt)
    processing_process = multiprocessing.Process(target=run_processing)

    mqtt_process.start()
    processing_process.start()

    mqtt_process.join()
    processing_process.join()