# game will get two random locations.
# one is revealed (temperature).
# guess if the second location is warmer or colder.
# if correct another random location and compare to locatiion two.

import requests
import os
import random
from dotenv import load_dotenv
from tkinter import *
from tkinter import ttk

root = Tk()
root.resizable(width=False, height=False)
frm = ttk.Frame(root, padding=20)
frm.grid()

countriesToCompare = []

#define class for storing class variables
class countryClass:
    def __init__(self, name, temperature):
        self.name = name
        self.temperature = temperature
    
#get coordinates for OpenWeatherMap API.
def getNameAndTemp(country):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={os.getenv('google_api')}"
    rs = requests.get(url)
    data = rs.json()

    cName = data['results'][0]['address_components'][0]['long_name']
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid={os.getenv('weather_api')}"
    rs = requests.get(url)
    data = rs.json()
    
    temp = data['main']['temp']
    
    c = countryClass(cName, temp)
    return c
     
#get a random country from external txt file.
def randomCountry():
    rnd = random.randint(0,195)
    return file[rnd]   

file = open("PROGRAM/countries.txt").readlines()
load_dotenv()

c1 = getNameAndTemp(randomCountry())
c2 = getNameAndTemp(randomCountry())

countriesToCompare.append(c1)
countriesToCompare.append(c2)

countryOne = Frame(frm, width=150, height=150, borderwidth=2, relief=RIDGE, bg="white")
countryTwo = Frame(frm, width=200, height=200, borderwidth=2, relief=RIDGE, bg="white")
quitButton = Button(frm, text="Quit",height=40, command=root.destroy)


buttons = Frame(frm,width=200, height=40, bg="red")

countryOne.grid(column=0, row=0, padx=5)
countryTwo.grid(column=1, row=0, padx=5)
quitButton.grid(column=0, row=1)
buttons.grid(column=1, row=1, pady=5)

    
    
frm.mainloop()


        



