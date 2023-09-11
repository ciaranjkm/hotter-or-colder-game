#add error checking for API requests
import requests
import os
import random
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
from io import BytesIO
from tkinter import *
from tkinter import ttk, font, messagebox
from PIL import Image, ImageTk, ImageOps

#global
file = open("PROGRAM/countries.txt").readlines()
c1Image = ImageTk.PhotoImage
turn = 0
countriesToCompare = [NONE]*2
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

    t1 = ImageTk.PhotoImage(Image.open(my_bytes_io).resize((150,150)))
    
    if c.isLeft == True:
        b.configure(image=t1, text=textLeft)
        b.photo = t1
    else:
        b.configure(image=t1, text=textRight)
        b.photo = t1
        
#onclick functions for game logic    
def onClickHigher():
    if countriesToCompare[0].temperature < countriesToCompare[1].temperature:
        print("onClickHigher...")
        
        countriesToCompare[0] = countriesToCompare[1]
        countriesToCompare[1] = getRandomCountry()
        countriesToCompare[0].isLeft = True
        
        populateSetButton(countriesToCompare[0], countryOneButton)
        populateSetButton(countriesToCompare[1], countryTwoButton)
               
        print("done")
        global turn 
        turn = turn + 1
        score.config(text="Score: " + str(turn))
    else:
        text = "Game Over! You scored " + str(turn) + "!\nPress 'OK' to restart."
        messagebox.showinfo("GAME OVER!", text)
        turn = 0
        start()
        
def onClickLower():
    if countriesToCompare[0].temperature > countriesToCompare[1].temperature:
        print("onClickLower...")
    
        countriesToCompare[0] = countriesToCompare[1]
        countriesToCompare[1] = getRandomCountry()
        countriesToCompare[0].isLeft = True
        
        populateSetButton(countriesToCompare[0], countryOneButton)
        populateSetButton(countriesToCompare[1], countryTwoButton)
               
        print("done")
        global turn 
        turn = turn + 1
        score.config(text="Score: " + str(turn))
    else:
        text = "Game Over! You scored " + str(turn) + "!\nPress 'OK' to restart."
        messagebox.showinfo("GAME OVER!", text)
        turn = 0
        start()
        
#function to restart game.
def start():
    countriesToCompare[0] = getRandomCountry()
    countriesToCompare[0].isLeft = True
    countriesToCompare[1] = getRandomCountry()
    
    populateSetButton(countriesToCompare[0], countryOneButton)
    populateSetButton(countriesToCompare[1], countryTwoButton)
    
    score.config(text="Score: " + str(turn))
      
        
#initialise tkinter
root = Tk()
root.resizable(width=False, height=False)
root.title("Hotter or Colder Game!")
frm = ttk.Frame(root, padding=5)

#row/column spans
frm.grid(column=0, row=0, rowspan=4)
frm.grid(column=1, row=0, rowspan=4)
frm.grid(column=0, row=0, columnspan=2)

#widgets topLeft -> bottomRight
title = Label(frm, text="Hotter or Colder!", font=('Arial', 24))
score = Label(frm, text=("Score: " + str(turn)), font=('Arial', 16))
#buttons lol
countryOneButton = Button(frm, fg="white", width=200, height=200, bd=5, compound=TOP, disabledforeground="white", state=DISABLED)
countryTwoButton = Button(frm, fg="white", width=200, height=200, bd=5, compound=TOP, disabledforeground="white", state=DISABLED)

higherButton = Button(frm, text="Warmer", command=onClickHigher)
lowerButton = Button(frm, text="Colder", command = onClickLower)
quitButton = Button(frm ,text="Quit", command=root.destroy)

#grid organisation
title.grid(column=0, row=0)
score.grid(column=2, row=0)

countryOneButton.grid(column=0, row=1, rowspan=4)
countryTwoButton.grid(column=1, row=1, rowspan=4)

higherButton.grid(column=2, row=1, pady=5, sticky=S)
lowerButton.grid(column=2, row=2, pady=5, sticky=N)
quitButton.grid(column=2, row=4, pady=5)    

start()
frm.mainloop()


     

    
    




        



