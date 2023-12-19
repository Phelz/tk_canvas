import pathlib
import random
import cv2
import requests

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime

WIDTH = 900
HEIGHT = 1200

WEATHER_API  = "4364fd06bebdc8e063ae488a20cd79cd"
WEATHER_CITY = 'Calgary'

ALL_IMG_PATHS = list(pathlib.Path("pictures").glob("*.jpg"))
# random.shuffle(ALL_IMG_PATHS)  # Shuffle the images


root = tk.Tk()
root.title("Tkinter Canvas App")
root.geometry(f"{WIDTH}x{HEIGHT}")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# * Images * #

def load_image(path):
    img = cv2.imread(str(path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def resize_and_center_bg(event):
    global bg_photo, canvas_bg
    img = load_image(img_path)

    # Calculate new height to preserve aspect ratio
    new_height = int(img.height * (WIDTH / img.width))
    resized_image = img.resize((WIDTH, new_height))

    bg_photo = ImageTk.PhotoImage(image=resized_image)
    canvas.itemconfig(canvas_bg, image=bg_photo)
    canvas.coords(canvas_bg, 0, (HEIGHT - new_height) // 2)

# Start with the first image in the shuffled list
img_index = 0
img_path = ALL_IMG_PATHS[img_index]
bg_image = load_image(img_path)
bg_photo = ImageTk.PhotoImage(image=bg_image)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=bg_photo)



# * Time Display * #

def create_display_image(text, font=ImageFont.truetype("arialbd.ttf", 20), width=500, height=250):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0)) # Transparent background
    draw = ImageDraw.Draw(img)
    
    draw.text((0, 0), text, fill="white", font=font)

    return img

def update_time():
    global time_image_ref  
    time_img = create_display_image(datetime.now().strftime("%H:%M:%S %p"), width=400, height=200)
    time_image_ref = ImageTk.PhotoImage(image=time_img)

    canvas.itemconfig(time_image_id, image=time_image_ref)
    root.after(1000, update_time)

# initialize the time display
time_image     = create_display_image(datetime.now().strftime("%H:%M:%S %p"), width=400, height=200)
time_image_ref = ImageTk.PhotoImage(image=time_image)
time_image_id  = canvas.create_image(WIDTH//2, HEIGHT//2, anchor="nw", image=time_image_ref)

update_time()


# * Weather Display * #

def call_weather_api():
    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API}&units=metric')
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        weather_str = f"Weather in {WEATHER_CITY}: {temperature} °C"
    except Exception as e:
        print(e)
        weather_str = "Error fetching weather"

    return weather_str

def update_weather():
    global weather_image_ref
    weather_img = create_display_image(call_weather_api())
    weather_image_ref = ImageTk.PhotoImage(image=weather_img)

    canvas.itemconfig(weather_image_id, image=weather_image_ref)
    root.after(60_000, update_weather)  # Update every 10 minutes

# initialize the weather display
weather_img       = create_display_image(call_weather_api())
weather_image_ref = ImageTk.PhotoImage(image=weather_img)
weather_image_id  = canvas.create_image(WIDTH//2, HEIGHT//3, anchor="nw", image=weather_image_ref)

update_weather()

# * Event Binds * #
root.bind("<Configure>", resize_and_center_bg)
root.mainloop()
