import pathlib
import requests

import tkinter as tk

from datetime import datetime

WEATHER_API  = "4364fd06bebdc8e063ae488a20cd79cd"
WEATHER_CITY = 'Calgary'

FONT = ("Times New Roman", 12)

ALL_IMG_PATHS = list(pathlib.Path("pictures").glob("*.png"))

# Function to update the time

root = tk.Tk()
root.title("Tkinter Canvas App")
root.geometry("900x1200")
# root.config(bg="")

canvas = tk.Canvas(root,  height=900, width=1200)

time_label = tk.Label(root, text="Time", font=FONT, bg="white", fg="black")
time_label.pack(pady=20, anchor="nw")

def update_time():
    time_now_str = datetime.now().strftime("%H:%M:%S %p")
    time_label.config(text=time_now_str)
    time_label.after(1000, update_time)



# Create a label for weather
weather_label = tk.Label(root, font=('calibri', 15), background='white', foreground='black')
weather_label.pack(pady=10)

def update_weather():
    
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API}&units=metric')
        weather_data = response.json()
        # print(weather_data)
        temperature = weather_data['main']['temp']
        weather_label.config(text=f"Weather in {WEATHER_CITY}: {temperature} °C")
    except Exception as e:
        print(e.__traceback__)
        weather_label.config(text="Error fetching weather")
    
    root.after(600000, update_weather)  # Update every 10 minutes


update_time()
update_weather()
# canvas.pack(pady=20)  # Add padding for aesthetics

root.mainloop()
