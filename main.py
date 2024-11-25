import multiprocessing
import time
import mqtt
import processing 
import response

def run_mqtt(message_queue):
    while True:
        mqtt.main(message_queue)
        time.sleep(1)

def run_processing():
    while True:
        processing.main()
        time.sleep(1)

def run_response(message_queue):
    while True:
        message_queue.put(response.main())
        time.sleep(10)

if __name__ == "__main__":
    message_queue = multiprocessing.Queue()

    mqtt_process = multiprocessing.Process(target=run_mqtt, args=(message_queue,))
    processing_process = multiprocessing.Process(target=run_processing)
    response_process = multiprocessing.Process(target=run_response, args=(message_queue,))

    mqtt_process.start()
    processing_process.start()
    response_process.start()

    try:
        mqtt_process.join()
        processing_process.join()
        response_process.join()
    except KeyboardInterrupt:
        print("Beenden erkannt, Prozesse stoppen...")
        mqtt_process.terminate()
        processing_process.terminate()
        response_process.terminate()

        mqtt_process.join()
        processing_process.join()
        response_process.join()