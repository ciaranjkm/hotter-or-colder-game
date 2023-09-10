# game will get two random locations.
# one is revealed (temperature).
# guess if the second location is warmer or colder.
# if correct another random location and compare to locatiion two.

import requests
import os
import random
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
from io import BytesIO
from tkinter import *
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageOps

#global
file = open("PROGRAM/countries.txt").readlines()
c1Image = ImageTk.PhotoImage
turn = 0
countriesToCompare = []
load_dotenv()

#functions and classes
#define class for storing class variables
class countryClass:
    location = ""
    temperature = 0
    shortLocation = ""
    isLeft = False
    
    def __init__(self, location, temperature, shortLocation):
        self.location = location
        self.temperature = temperature
        self.shortLocation = shortLocation
    
#get coordinates for OpenWeatherMap API.
def getRandomCountry():
    country = file[random.randint(0,195)]
    
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={country}&key={os.getenv('google_api')}"
    rs = requests.get(url)
    data = rs.json()

    location = data['results'][0]['address_components'][0]['long_name']
    shortLocation = data['results'][0]['address_components'][0]['short_name']
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid={os.getenv('weather_api')}"
    rs = requests.get(url)
    data = rs.json()
    
    temp = data['main']['temp']
    
    c = countryClass(location, temp, shortLocation)
    return c

#populate button in parameters with name, image and (optional temperature)
def populateSetButton(c = countryClass, b = Canvas):
    location = c.location   
    temperature = c.temperature
    shortLocation = c.shortLocation
    
    textLeft = location + "\n" + str(temperature) + "c"
    textRight = location + "\n"
        
    gis = GoogleImagesSearch(os.getenv('google_api'), os.getenv('google_cx'))
    locationToSearch = c.location + "flag"
    searchParam = {
        'q' : locationToSearch,
        'num' : 1,
        'rights': 'cc_publicdomain',
        'fileType' : 'jpg'
    }

    gis.search(search_params=searchParam)
    my_bytes_io = BytesIO()
    
    image = gis.results()[0]
    my_bytes_io.seek(0)
    image.copy_to(my_bytes_io)
    temp = Image.open(my_bytes_io).resize((150,150))

    t1 = ImageTk.PhotoImage(temp)
    
    if c.isLeft == True:
        b.configure(image=t1, text=textLeft)
        b.photo = t1
    else:
        b.configure(image=t1, text=textRight)
        b.photo = t1
    
#initialise tkinter
root = Tk()
root.resizable(width=False, height=False)
frm = ttk.Frame(root, padding=20)
frm.grid(column=0, row=0, columnspan=2)
frm.grid(column=1, row=0, columnspan=2)
frm.grid(column=2, row=0, columnspan=2)

countryOneButtonText = StringVar()
countryTwoButtonText = StringVar()

countryOneButton = Button(frm, fg="white", width=200, height=200, bd=5, compound=TOP, disabledforeground="white", state=DISABLED)
countryTwoButton = Button(frm, fg="white", width=200, height=200, bd=5, compound=TOP, disabledforeground="white", state=DISABLED)

optionsButton = Button(frm, text="Options")
quitButton = Button(frm,text="Quit", command=root.destroy)

higherButton = Button(frm, text="Higher")
lowerButton = Button(frm, text="lower")

countryOneButton.grid(column=0, row=0, padx=5)
countryTwoButton.grid(column=1, row=0, padx=5)

optionsButton.grid(column=2, row=0)
quitButton.grid(column=2, row=0)    


#game logic
if turn == 0:
    c1 = getRandomCountry()
    c1.isLeft = True
    c2 = getRandomCountry()
        
    countriesToCompare.append(c1)
    countriesToCompare.append(c2)
    
    populateSetButton(countriesToCompare[0], countryOneButton)
    populateSetButton(countriesToCompare[1], countryTwoButton)
    
frm.mainloop()


     

    
    




        



