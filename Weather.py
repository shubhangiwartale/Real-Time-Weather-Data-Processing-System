import requests
import tkinter as tk
from tkinter import messagebox
import statistics

# OpenWeatherMap API key and list of cities
API_KEY = 'd452b627ab3da0b13ff6e2498da7ddcf'  # Replace with your actual API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Hyderabad']

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to fetch weather forecast data
def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(temp): 
    return temp - 273.15

# Function to process weather data and display in GUI
def display_weather(city):
    data = get_weather_data(city)
    temp = kelvin_to_celsius(data['main']['temp'])
    condition = data['weather'][0]['main']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Display the current weather details
    result_label.config(text=f"Current Weather in {city}:\n"
                             f"Temperature: {temp:.2f}°C\n"
                             f"Condition: {condition}\n"
                             f"Humidity: {humidity}%\n"
                             f"Wind Speed: {wind_speed} m/s")

# Function to process forecast data and display in GUI
def display_forecast(city):
    forecast_data = get_forecast_data(city)
    forecast_temps = []
    forecast_conditions = []

    for forecast in forecast_data['list']:
        temp = kelvin_to_celsius(forecast['main']['temp'])
        condition = forecast['weather'][0]['main']
        forecast_temps.append(temp)
        forecast_conditions.append(condition)

    avg_temp = statistics.mean(forecast_temps)
    dominant_condition = max(set(forecast_conditions), key=forecast_conditions.count)

    # Display the forecast details
    result_label.config(text=f"Weather Forecast for {city}:\n"
                             f"Avg Forecast Temp: {avg_temp:.2f}°C\n"
                             f"Dominant Condition: {dominant_condition}")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")
root.config(bg="#f0f0f5")  # Light grey background

# Custom styling for labels and buttons
button_style = {"font": ("Arial", 12, "bold"), "bg": "#007acc", "fg": "white", "relief": "groove"}
label_style = {"bg": "#f0f0f5", "font": ("Arial", 12)}

# Create dropdown menu for city selection
city_var = tk.StringVar(root)
city_var.set(CITIES[0])  # Default value

city_menu = tk.OptionMenu(root, city_var, *CITIES)
city_menu.config(font=("Arial", 12), bg="#cce7ff", fg="black", width=15)
city_menu.pack(pady=15)

# Create buttons for fetching current weather and forecast
weather_button = tk.Button(root, text="Get Current Weather", command=lambda: display_weather(city_var.get()), **button_style)
weather_button.pack(pady=10, ipadx=10, ipady=5)

forecast_button = tk.Button(root, text="Get Weather Forecast", command=lambda: display_forecast(city_var.get()), **button_style)
forecast_button.pack(pady=10, ipadx=10, ipady=5)

# Create a frame for the result label to make it more visually distinct
result_frame = tk.Frame(root, bg="white", bd=2, relief="sunken", padx=10, pady=10)
result_frame.pack(pady=20, fill="both", expand=True)

# Label to display results inside the result frame
result_label = tk.Label(result_frame, text="", font=("Helvetica", 12), justify="left", bg="white", anchor="nw")
result_label.pack(fill="both", expand=True)

# Run the tkinter event loop
root.mainloop()
