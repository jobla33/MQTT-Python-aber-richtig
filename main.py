import multiprocessing
import time
import mqtt
import processing 

def run_mqtt():
    while True:
        mqtt.main()
        time.sleep(1)

def run_processing():
    while True:
        processing.main()
        time.sleep(1)

if __name__ == "__main__":
    mqtt_process = multiprocessing.Process(target=run_mqtt)
    processing_process = multiprocessing.Process(target=run_processing)

    mqtt_process.start()
    processing_process.start()

    mqtt_process.join()
    processing_process.join()