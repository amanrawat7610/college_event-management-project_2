import time
from plyer import notification

def water_reminder():
    while True:
        notification.notify(
            title="water reminder",
            message="this time to ship water mr.aman",
            timeout=10
        )
        time.sleep(3)
  

water_reminder()