import datetime
import webbrowser
import requests
from utilities.websearch import search_for,youtube,checkconn
from utilities.speech_functions import *
from utilities.email_ import *
from utilities.powerOptions import *
from utilities.confirm import *
from utilities.capture import *
from utilities.conversational_util import *

gender = ['Female', 'Male']
addressee = ['Sir', 'Miss', 'Boss']

def greet(addressee):
    
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak(f'Good Morning {addressee}')
    elif hour >= 12 and hour < 18:
        speak(f'Good Afternoon {addressee}')
    else:
        speak(f'Good Evening {addressee}')

greet(addressee[2])
history = False

while True:
    
    statement = listen()
    
    if statement == None:
        continue

    if "hello edith" in statement or 'hey' in statement or 'hello' in statement:
        speak('Oh Hello sir')

    elif 'time' in statement:
        strTime = datetime.datetime.now().strftime("%I:%M:%p")
        print(f"It\'s {strTime} right now")
        speak(f"It\'s {strTime} right now")

    elif 'email' in statement:
        if checkconn():
            sendEmail()
    
    elif 'search' in statement:
        if checkconn():
            param = statement.replace("search", "")
            search_for(param)

    elif 'snapshot' in statement or 'snip' in statement or 'snap' in statement or 'screenshot' in statement:
        snapshot()

    elif 'picture' in statement or 'capture' in statement:
        camera()
    
    elif 'log off' in statement:
        if confirm():
            execute("shutdown /l")
    
    elif 'shutdown' in statement:
        if confirm():
            execute("shutdown /s")
    
    elif 'sleep' in statement:
        if confirm():
            execute("rundll32.exe powrprof.dll,SetSuspendState Sleep")

    elif 'open youtube' in statement:
        if checkconn():
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Youtube is open now")
    
    elif 'play on youtube' in statement:
        if checkconn():
            param = statement.replace("play on youtube ", "")
            youtube(param)

    elif "weather" in statement:
        if checkconn():
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("Which city sir?")
            city_name = listen()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                temperature = y["temp"] - 273.15
                temperature = round(temperature)
                humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"].capitalize()
                print(f'Temperature = {temperature} C \nHumidity = {humidity}% \nDescription: {weather_description}')
                speak(f'It\'s {temperature} degree celsius and {weather_description} \n Humidity is {humidity}%')

            else:
                speak("Sorry City Not Found!")

    elif 'bye' in statement or 'quit' in statement or 'goodbye' in statement:
        speak('See you soon Sir!')
        break

    else:
        if not history:
            output, chat_history = converse(statement)
            history = True
            print(output)
            speak(output)
            continue
        
        output, chat_history = converse(statement, chat_history)
        print(output)
        speak(output)