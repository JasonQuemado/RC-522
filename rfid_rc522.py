import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#import time

class Rfid:
    
    def __init__(self):
        GPIO.setwarnings(False) # Desactiva warnings de GPIO
        GPIO.setmode(GPIO.BOARD)
        self.reader = SimpleMFRC522()

    def read_uid(self):
        #duration = 30
        #pause = 2
        #startTime = time.time()
        try:
            print("Waiting for a tag...")
            print("")
            #while duration > time.time() - startTime:
            uid, _ = self.reader.read()
            uid = f"{uid:08X}" 
            print(f"card ID: {uid}")
            print("")
            break()
            #time.sleep(pause)
            #return uid
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    rf = Rfid()
    uid = rf.read_uid()

