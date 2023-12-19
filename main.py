import pathlib
import random
import cv2
import requests

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime

WIDTH = 900
HEIGHT = 1200

IMG_UPDATE_TIME = 3_000
WEATHER_UPDATE_TIME = 60_000

WEATHER_API  = "4364fd06bebdc8e063ae488a20cd79cd"
WEATHER_CITY = 'Calgary'

ALL_IMG_PATHS = list(pathlib.Path("pictures").glob("*.jpg"))
random.shuffle(ALL_IMG_PATHS)  # Shuffle the images

ALL_DOGE_PATHS = list(pathlib.Path("dog_pics").glob("*"))

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

def resize_image(image):
    new_height = int(image.height * (WIDTH / image.width))
    return image.resize( (WIDTH, new_height) ) # preserve width

# Start with the first image in the shuffled list
img_index = 0
img_path  = ALL_IMG_PATHS[img_index]
bg_image  = load_image(img_path)
bg_photo  = ImageTk.PhotoImage(image=bg_image)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

def update_image():
    global img_index, img_path, bg_photo, canvas_bg

    # Update the image index
    if img_index == len(ALL_IMG_PATHS) - 1:
        random.shuffle(ALL_IMG_PATHS)  # Shuffle the images
        img_index = 0
    else:
        img_index += 1

    img_path = ALL_IMG_PATHS[img_index]
    
    # Resize and show
    bg_image      = load_image(img_path)
    resized_image = resize_image(bg_image)
    bg_photo      = ImageTk.PhotoImage(image=resized_image)

    canvas.itemconfig(canvas_bg, image=bg_photo)
    canvas.coords(canvas_bg, 0, ( HEIGHT -  resized_image.height) // 2) # center

    root.after(IMG_UPDATE_TIME, update_image)

update_image()


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
        response     = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API}&units=metric')
        weather_data = response.json()
        temperature  = weather_data['main']['temp']
        weather_str  = f"Weather in {WEATHER_CITY}: {temperature} °C"
    except Exception as e:
        print(e)
        weather_str = "Error fetching weather"

    return weather_str

def update_weather():
    global weather_image_ref
    
    weather_img = create_display_image(call_weather_api())
    weather_image_ref = ImageTk.PhotoImage(image=weather_img)

    canvas.itemconfig(weather_image_id, image=weather_image_ref)
    root.after(WEATHER_UPDATE_TIME, update_weather)  # Update every 10 minutes

# initialize the weather display
weather_img       = create_display_image(call_weather_api())
weather_image_ref = ImageTk.PhotoImage(image=weather_img)
weather_image_id  = canvas.create_image(WIDTH//2, HEIGHT//3, anchor="nw", image=weather_image_ref)

update_weather()


# * Dog Image * #
def show_dog_image():
    global dog_image_ref

    dog_img_path = random.choice(ALL_DOGE_PATHS)
    dog_image    = Image.open(dog_img_path)

    resized_dog_image = resize_image(dog_image)
    dog_image_ref = ImageTk.PhotoImage(resized_dog_image)

    # Create a Toplevel window
    top = tk.Toplevel(root)
    top.geometry(f"{WIDTH}x{HEIGHT}+{root.winfo_x()}+{root.winfo_y()}")  # Adjust size and position

    label = tk.Label(top, image=dog_image_ref)
    label.pack(expand=True)

    top.after(IMG_UPDATE_TIME, top.destroy)

button = tk.Button(root, text="DOGE", command=show_dog_image, font=("Arial", 20), borderwidth=2, relief="raised")
button.pack(side="bottom", anchor="se", padx=10, pady=10)

# * Run * #
root.mainloop()
