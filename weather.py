import requests
import regex
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image,ImageTk
import datetime

class Forecast:
    label : str
    highTemp : str
    lowTemp : str
    precip : str

class ForecastWidget(Canvas):
    forecast : Forecast
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>",self.on_resize)
        self.height=4
        self.width = 20

        self.label = Label(self,fg="white",bg="#121257",width=self.width,height=self.height//4,font=("Helvetica",15))
        self.highTemp = Label(self,fg="white",bg="#121257",width=self.width,height=self.height//4,font=("Helvetica",15))
        self.lowTemp = Label(self,fg="white",bg="#121257",width=self.width,height=self.height//4,font=("Helvetica",15))
        self.precip = Label(self,fg="white",bg="#121257",width=self.width,height=self.height//4,font=("Helvetica",15))

        self.label.grid(row=0,column=0,pady=3*heightScale)
        self.highTemp.grid(row=1,column=0,pady=3*heightScale)
        self.lowTemp.grid(row=2,column=0,pady=3*heightScale)
        self.precip.grid(row=3,column=0,pady=3*heightScale)

    def update(self):
        self.label.config(text=self.forecast.label)
        self.highTemp.config(text="High: " + str(self.forecast.highTemp))
        self.lowTemp.config(text="Low: " + str(self.forecast.lowTemp))
        self.precip.config(text="Precip: " + str(self.forecast.precip))
        self.label.after(24*60*1000,getForecasts)

    def on_resize(self,event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        self.config(width=self.width,height=self.height)

        self.scale("all",0,0,wscale,hscale)

    def get(self):
        return self.entry.get()
    
class ResizingCnavas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>",self.on_resize)
        self.height=self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        self.config(width=self.width,height=self.height)

        self.scale("all",0,0,wscale,hscale)

def getTime():
    time = datetime.datetime.now().strftime("%I : %M %p")
    timeLabel.config(text=time)
    timeLabel.after(60000,getTime)

def getDay():
    day = datetime.datetime.now().strftime("%d")
    dayLabel.config(text=day)
    dayLabel.after(24*60*1000,getDay)

def getMonth():
    month = datetime.datetime.now().strftime("%b")
    monthLabel.config(text=month)
    monthLabel.after(24*60*1000,getMonth)


def getForecasts(forecastWidgets):
    forecasts : [Forecast] = []
    url = "https://weather.com/weather/today/l/43.0733,-89.4012"
    req = requests.get(url)

    soup = BeautifulSoup(req.content,"html.parser")
    dailyWeathercard = soup.find("div",class_="DailyWeatherCard--TableWrapper--2bB37")
    items = dailyWeathercard.find_all("li",class_="Column--column--3tAuz")

    

    for item in items:
        forecast : Forecast = Forecast()
        forecast.label = item.find(class_=regex.compile("Column--label")).text
        forecast.highTemp = item.find(class_=regex.compile("Column--temp")).text
        forecast.lowTemp = item.find(class_=regex.compile("Column--tempLo")).text
        forecast.precip = item.find("span", class_=regex.compile("Column--precip")).contents[1]
        forecasts.append(forecast)
        forecastWidget = ForecastWidget(canvas,bg="#121257",bd=0,highlightthickness=0)
        forecastWidget.forecast = forecast
        forecastWidgets.append(forecastWidget)
    
    for forecastWidget in forecastWidgets:
        forecastWidget.update()
    return forecastWidgets
    
    

forecastWidgets : [ForecastWidget] = []
window = Tk();
window.attributes('-fullscreen',True)

canvas = ResizingCnavas(window)
canvas.pack(fill=BOTH,expand=True)
canvas.update()
bgImage = Image.open("bg.png")
imageSize = (window.winfo_width(),window.winfo_height())
bgImage = bgImage.resize(imageSize,Image.NEAREST)
bg = ImageTk.PhotoImage(bgImage)
canvas.create_image(0,0,image=bg,anchor="nw")

widthScale = canvas.winfo_width() // 160
heightScale = canvas.winfo_height() // 128

forecastWidgets = getForecasts(forecastWidgets)
for i in range(len(forecastWidgets)):    
    forecastWidgets[i].place(x=240 * i + 20 * widthScale + 5 * i * widthScale,y=79 * heightScale)



timeLabel = Label(canvas,font=("Helvetica",150),fg="white",bg="#121241")
monthLabel = Label(canvas,font=("Helvetica",120),fg="white",bg="#121241")
dayLabel = Label(canvas,font=("Helvetica",120),fg="white",bg="#121241")
dayLabel.place(y=35*heightScale,x=21*widthScale)
timeLabel.place(y=20*heightScale,x=58*widthScale)
monthLabel.place(y=15*heightScale,x=17*widthScale)

getTime()
getDay()
getMonth()

canvas.addtag_all(newtag="all")
window.mainloop()