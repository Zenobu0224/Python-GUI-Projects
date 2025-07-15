from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk
from io import BytesIO

ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("PyTher-WeaThon")
        self.iconbitmap('WeatherApp/imgs/weather_icon.ico')
        self.resizable(False, False)
        self.configure(fg_color="#9db8e1")
        self.cur_date = ctk.StringVar()
        self.cur_time = ctk.StringVar()

        self.icon = PhotoImage(file='WeatherApp/imgs/icon.png')

        top_frame = ctk.CTkFrame(self, fg_color="#76a0df", corner_radius=0)
        top_frame.pack(fill="x", expand=True, anchor="n", pady=(0,0))

        inner_left_frame = ctk.CTkFrame(top_frame, fg_color="transparent", width=350, corner_radius=0)
        inner_left_frame.pack(side="left", padx=0)

        self.search_bar = ctk.CTkEntry(inner_left_frame, fg_color="#3a4b66", font=("Comic Sans MS", 18), width=300, border_width=2,
                                       placeholder_text="Search location here", placeholder_text_color="#cccccc", text_color="#ffffff", corner_radius=12)
        self.search_bar.pack(side="left", padx=(30,0), pady=5, ipadx=10, ipady=7)

        self.search_btn = ctk.CTkButton(inner_left_frame, text="🔍", font=("Comic Sans MS", 20), width=60, fg_color="#567189",
                                        text_color="#ffffff", hover_color="#435970", border_spacing=5, corner_radius=15, command=self.getWeather)
        self.search_btn.pack(side="right", padx=(0,20), pady=5)

        inner_right_frame = ctk.CTkFrame(top_frame, fg_color="transparent", height=100, width=350, corner_radius=0)
        inner_right_frame.pack(side="right", padx=0)

        ctk.CTkLabel(inner_right_frame, text="Tenki Forecast", font=("Comic Sans MS", 25), image=self.icon, compound="right", text_color="#000000").pack(padx=5, pady=5)

        self.weather = Tenki(self)
        self.weather.pack(side="left", padx=(30,0), pady=(0,25))

        self.weather_des = Tenki_Des(self)
        self.weather_des.pack(side="right", padx=(0,10), pady=(0,40))

        self.bind("<Return>", lambda event: self.getWeather())

    def getWeather(self):
        place = self.search_bar.get()

        if not place:
            print("Please enter a location.")
            return

        api_key = "b6beb79568fd6d61f9095295112e82ae"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(f"{data}")

            self.weather.display_weather(data)
            self.weather_des.display_location_time(place)
            self.weather_des.display_weather_des(data, place)

            if data["cod"] == 200:
                print("Location found!\n\n")
            else:
                print("Locaton not found!\n\n")

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 400:
                messagebox.showerror(title="400 Bad Request", message="The server could not understand the request due to invalid syntax.")
            elif response.status_code == 401:
                messagebox.showerror(title="401 Unauthorized", message="The request requires user authentication or the provided API key is invalid.")
            elif response.status_code == 403:
                messagebox.showerror(title="403 Forbidden", message="The server understood the request, but it refuses to authorize it.")
            elif response.status_code == 404:
                messagebox.showerror(title="404 Not Found", message="The requested resource could not be found on the server.")
            elif response.status_code == 500:
                messagebox.showerror(title="500 Internal Server Error", message="The server encountered an unexpected condition that prevented it from fulfilling the request.")
            elif response.status_code == 502:
                messagebox.showerror(title="502 Bad Gateway", message="The server, while acting as a gateway or proxy, received an invalid response from the upstream server.")
            elif response.status_code == 503:
                messagebox.showerror(title="503 Service Unavalable", message="The server is currently unable to handle the request due to temporary overloading or maintenance of the server.")
            elif response.status_code == 504:
                messagebox.showerror(title="504 Gateway Timeout", message="The server, while acting as a gateway or proxy, did not receive a timely response from the upstream server.")
            else:
                messagebox.showerror(title="HTTP Error", message=f"An HTTP error occurred: {http_err}")

        except requests.exceptions.ConnectionError:
            messagebox.showerror(title="Connection Error", message="Unable to connect to the server. Please check your internet connection.")

        except requests.exceptions.Timeout:
            messagebox.showerror(title="Timeout Error", message="The request timed out. Please try again later.")

        except requests.exceptions.TooManyRedirects:
            messagebox.showerror(title="Redirect Error", message="Too many redirects. The request exceeded the maximum number of redirects. Please check the URL")

        except requests.exception.RequestException as req_error:
            messagebox.showerror(title="Request Error", message=f"An error occurred while making the request: {req_error}")

class Tenki(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", height=420, width=350, **kwargs)

        self.cur_weather_description = ctk.StringVar(value="...")
        self.cur_temperature = ctk.StringVar(value="...")

        self.weather_img_lab = ctk.CTkLabel(self, image=None, text="")
        self.weather_img_lab.pack()

        self.celcius = ctk.CTkLabel(self, textvariable=self.cur_temperature, font=("Bahnschrift", 22), text_color="#000000", justify="left")
        self.celcius.pack(padx=10,pady=(5,5), anchor="w")

        self.description = ctk.CTkLabel(self, textvariable=self.cur_weather_description, font=("Bahnschrift", 22), text_color="#000000", justify="left")
        self.description.pack(padx=10,pady=(5, 30), anchor="w")

    def display_weather(self, weather_data):
        weather_img_icon = weather_data["weather"][0]["icon"]
        weather_img_url = f"https://openweathermap.org/img/wn/{weather_img_icon}@2x.png"

        try:
            response = requests.get(weather_img_url)
            response.raise_for_status()
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((350,350))
            self.weather_img = ImageTk.PhotoImage(img)
        except requests.exceptions.RequestException as e:
            messagebox.showerror(title="Image Fetch Error", message=f"Failed to fetch weather image: {e}")

        self.weather_img_lab.configure(image=self.weather_img)
        self.weather_img_lab.image = self.weather_img

        temperature = weather_data["main"]["temp"] - 273.15
        temp_round_off = round(temperature)
        self.cur_temperature.set(f"Temperature: {temp_round_off} °C")

        description = weather_data["weather"][0]["description"].capitalize()
        self.cur_weather_description.set(f"Weather: {description}")

class Tenki_Des(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#527177", height=420, width=350, corner_radius=15, **kwargs)

        self.humidity_icon = PhotoImage(file='WeatherApp/imgs/shitsudo.png')
        self.wind_icon = PhotoImage(file='WeatherApp/imgs/kaze.png')
        self.pressure_icon = PhotoImage(file='WeatherApp/imgs/atsuryoku.png')

        self.cur_loc = ctk.StringVar(value="...")
        self.cur_time = ctk.StringVar(value="...")
        self.cur_humidity = ctk.StringVar(value="...")
        self.cur_wind = ctk.StringVar(value="...")
        self.cur_pressure = ctk.StringVar(value="...")

        loc_time_frame = ctk.CTkFrame(self, height=150, width=330, fg_color="transparent")
        loc_time_frame.pack(side="top", pady=(5,20), padx=5, anchor="w")

        ctk.CTkLabel(loc_time_frame, textvariable=self.cur_loc, text_color="#f0f2f5", font=("Comic Sans MS", 25)).pack(padx=8,pady=5, anchor="w")
        ctk.CTkLabel(loc_time_frame, textvariable=self.cur_time, text_color="#dddddd", font=("Bahnschrift", 20)).pack(padx=8,pady=(5,0), anchor="w")

        tenki_essen = ctk.CTkScrollableFrame(self, height=140, width=300, orientation="horizontal", fg_color="#4e6368", scrollbar_button_color="#6e7e85")
        tenki_essen.pack(side="bottom", padx=10, pady=(60,20))

        hum_con = ctk.CTkFrame(tenki_essen, fg_color="#7A9F95")
        hum_con.pack(padx=5, pady=5, side="left")

        hum_header = ctk.CTkFrame(hum_con, corner_radius=10, fg_color="#A3C4BC")
        hum_header.pack(padx=10, pady=5)

        ctk.CTkLabel(hum_header, text="Humidity", font=("Comic Sans MS", 20, "bold"), text_color="#000000", image=self.humidity_icon, compound="left", padx=10).pack(padx=15, pady=5)
        humidity = ctk.CTkLabel(hum_con, textvariable=self.cur_humidity, font=("Comic Sans MS", 20), text_color="#f0f2f5")
        humidity.pack(padx=10,pady=10)

        kaze_con = ctk.CTkFrame(tenki_essen, fg_color="#7A9F95")
        kaze_con.pack(padx=5, pady=5, side="left")

        wind_header = ctk.CTkFrame(kaze_con, corner_radius=10, fg_color="#A3C4BC")
        wind_header.pack(padx=10, pady=5)

        ctk.CTkLabel(wind_header, text="Wind", font=("Comic Sans MS", 20, "bold"), text_color="#000000", image=self.wind_icon, compound="left", padx=10).pack(padx=25, pady=5)
        self.wind = ctk.CTkLabel(kaze_con, textvariable=self.cur_wind, font=("Comic Sans MS", 20), text_color="#f0f2f5")
        self.wind.pack(padx=10,pady=10)

        pressure_con = ctk.CTkFrame(tenki_essen, fg_color="#7A9F95")
        pressure_con.pack(padx=5, pady=5, side="left")

        pressure_header = ctk.CTkFrame(pressure_con, corner_radius=10, fg_color="#A3C4BC")
        pressure_header.pack(padx=10, pady=5)

        ctk.CTkLabel(pressure_header, text="Pressure", font=("Comic Sans MS", 20, "bold"), text_color="#000000",image=self.pressure_icon, compound="left", padx=10).pack(padx=15, pady=5)
        pressure = ctk.CTkLabel(pressure_con, textvariable=self.cur_pressure, font=("Comic Sans MS", 20), text_color="#f0f2f5")
        pressure.pack(padx=10,pady=10)

    def display_location_time(self, searched_location):
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(searched_location)
        if location:
            tf = TimezoneFinder()
            timezonefr = tf.timezone_at(lat=location.latitude, lng=location.longitude)
            if timezonefr:
                self.timezone = pytz.timezone(timezonefr)
                self.update_time()

    def update_time(self):
        if hasattr(self, 'timezone'):
            local_time = datetime.now(self.timezone).strftime("%I:%M:%S%p")
            self.cur_time.set(local_time)
        self.after(1000, self.update_time)

    def display_weather_des(self, weather_data, searched_location):
        self.cur_loc.set(f"{searched_location.capitalize()}, {weather_data['sys']['country']}")

        humidity = weather_data['main']['humidity']
        self.cur_humidity.set(f"{humidity}%")

        wind_speed = weather_data["wind"]["speed"] * 3.6
        wind_speed = round(wind_speed, 2)
        self.cur_wind.set(f"{wind_speed} km/h")

        pressure = weather_data['main']['pressure']
        self.cur_pressure.set(f"{pressure} hPa")
