import json
import psutil

try:
    with open("model.json", "r") as file:
        battery = psutil.sensors_battery()
        percent = battery.percent
        data = json.load(file)
        w = data["w"]
        b = data["b"]

        hours = (percent - b) / w
        decimal_hours = hours - int(hours)
        minutes = int(decimal_hours * 60)
        print(f"The model predicts you have {int(hours)} hour(s) and {minutes} minute(s) left of usage.")

        windows_secsLeft = battery.secsleft
        windows_hoursleft = windows_secsLeft / 3600
        windows_decimal_hoursleft = windows_hoursleft - int(windows_hoursleft)
        windows_minsleft = int(windows_decimal_hoursleft * 60)
        print(f"Windows predicts you have {int(windows_hoursleft)} hour(s) and {windows_minsleft} minute(s) left of usage.")
        
except FileNotFoundError:
    print("You haven't trained the model yet!")