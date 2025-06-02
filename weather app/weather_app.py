import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text
from PIL import Image, ImageTk
import requests
import datetime
import io

# --- API Config ---
API_KEY = "892ea90552023b3a5e1b7bde1f7ca923"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
HISTORY_FILE = "weather_history.txt"

# --- Save to history file ---
def save_to_history(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp}\n{data}\n" + "-"*40 + "\n")

def view_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history_content = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read history file:\n{e}")
        return

    history_win = tk.Toplevel(root)
    history_win.title("Weather History")
    history_win.geometry("400x400")

    text_area = tk.Text(history_win, wrap="word", font=("Arial", 10))
    text_area.insert("1.0", history_content)
    text_area.config(state="disabled")
    text_area.pack(expand=True, fill="both")




# --- Main Weather Function ---
def get_weather():
    city = city_entry.get()
    if city == "":
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data['weather'][0]['description']
            icon_id = data['weather'][0]['icon']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']

            # Change background color
            if "cloud" in weather:
                root.config(bg="#b0c4de")
            elif "rain" in weather:
                root.config(bg="#778899")
            elif "sun" in weather or "clear" in weather:
                root.config(bg="#f0e68c")
            else:
                root.config(bg="lightgray")

            # Icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            icon_data = requests.get(icon_url).content
            icon_img = ImageTk.PhotoImage(Image.open(io.BytesIO(icon_data)))

            result = (
                f"📍 {city.title()}\n"
                f"{weather.capitalize()}\n"
                f"🌡️ Temp: {temp}°C\n"
                f"🤒 Feels like: {feels_like}°C\n"
                f"💧 Humidity: {humidity}%"
            )
            result_label.config(text=result, bg=root['bg'], fg="black")
            weather_icon_label.config(image=icon_img)
            weather_icon_label.image = icon_img

            # Save to history
            save_to_history(result)

        else:
            result_label.config(text="❌ City not found. Try again.", bg=root['bg'])
            weather_icon_label.config(image="")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Weather App")
root.geometry("420x500")
root.config(bg="lightgray")

title_label = tk.Label(root, text="🌦️ Weather App", font=("Helvetica", 16, "bold"), bg="lightgray")
title_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=10)

get_btn = tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather)
get_btn.pack(pady=5)

weather_icon_label = tk.Label(root, bg="lightgray")
weather_icon_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 12), bg="lightgray", justify="center")
result_label.pack(pady=10)

history_btn = tk.Button(root, text="View History", font=("Arial", 11), command=view_history)
history_btn.pack(pady=5)

root.mainloop()
