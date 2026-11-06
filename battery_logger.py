import psutil
import csv
import time
import os
from datetime import datetime

initial_time = time.time()

os.makedirs("data", exist_ok=True)
filename = f"data/session_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv"

with open(filename, "w", newline="") as csvfile:
    fieldnames = ["minutes", "battery_pct"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while True:
        try:
            current_battery = psutil.sensors_battery()
            current_percent = current_battery.percent
            current_time = time.time()
            delta_minutes = (current_time - initial_time) / 60
            writer.writerow({"minutes": delta_minutes, "battery_pct": current_percent})
            csvfile.flush()
            time.sleep(60)

        except KeyboardInterrupt:
            break