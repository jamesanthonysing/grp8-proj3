# MapQuest Pathfinder 2.0 | by Group 8 - 4ITI
from enum import auto
import urllib.parse
import requests
import colorama
from tkinter import *
from tkinter import messagebox
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Import MapQuest API
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "PJv71zxlt65ihzFpAKRuP6HQ3zaCJDQ9"

# GUI Settings
window = Tk()
window.title("MapQuest Pathfinder 2.0")
window.geometry("600x300")
window.resizable(False, False) 

global orig, dest
orig = StringVar()
dest = StringVar()

def getInput():
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig.get(), "to":dest.get()})
    # Get json data request
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    # Output if successful json route call
    if json_status == 0:
        print(Fore.GREEN + "API Status " + str(json_status) + " = Congratulations! A successful route call.\n")

        label_intro = Label(window, text="What would you like to know about \n"+ orig.get() +" to "+ dest.get() +"?")
        label_intro.grid(row=4, column=1, padx=5, pady=10)
       
        # Display buttons
        btn_choice1 = Button(window, text="General Info", command=choice1)
        btn_choice1.grid(row=5, column=1, sticky=W, padx=5, pady=10)
       
        btn_choice2 = Button(window, text="Restrictions", command=choice2)
        btn_choice2.grid(row=7, column=1, sticky=W, padx=5, pady=10)
       
        btn_choice3 = Button(window, text="Miscellaneous", command=choice3)
        btn_choice3.grid(row=5, column=2, sticky=W, padx=5, pady=10)

        btn_choice4 = Button(window, text="Directions", command=choice4)
        btn_choice4.grid(row=7, column=2, sticky=W, padx=5, pady=10)
    
    # Output if unsuccessful json route calls
    elif json_status == 402: # Invalid user input
        messagebox.showerror("Error", "Oops! We encountered an error.\n" + 
        "Status Code: " + str(json_status) + 
        "; \n Invalid user inputs for one or both locations.")

        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.\n")
    elif json_status == 611: # Missing entry
        messagebox.showerror("Error", "Oops! We encountered an error.\n" +
        "Status Code: " + str(json_status) + 
        "; \n Missing an entry for one or both locations.")

        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; Missing an entry for one or both locations.\n")
    elif json_status == 500: # Added status code 500
        messagebox.showerror("Error", "Oops! We encountered an error.\n" +
        "Status Code: " + str(json_status) +
        "; \n The server encountered an error and could not complete your request.")

        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; The server encountered an error and could not complete your request.\n")
    elif json_status == 404: # Added status code 404
        messagebox.showerror("Error", "Oops! We encountered an error.\n" +
        "Status Code: " + str(json_status) +
        "; \n The resource addressed by the request URL does not exist.")

        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "Status Code: " + str(json_status) + "; The resource addressed by the request URL does not exist.\n")
    else:
        messagebox.showerror("Error", "Oops! We encountered an error.\n" +
        "For Status Code: " + str(json_status) + "; \n Refer to:" +
        "https://developer.mapquest.com/documentation/directions-api/status-codes")

        print(Fore.RED + "Oops! We encountered an error.")
        print(Fore.RED + "For Status Code: " + str(json_status) + "; Refer to:")
        print(Fore.RED + "https://developer.mapquest.com/documentation/directions-api/status-codes\n")

    return json_data

# Choices
def choice1():
    json_data = getInput()

    distMi = (json_data["route"]["distance"])
    # Distance conversion
    distKm = (json_data["route"]["distance"])*1.61
    distM = (json_data["route"]["distance"])*1609.344

    top = Toplevel()
    top.title("General Info")
    top.geometry("200x100")
    top.resizable(False, False) 

    label_output = Label(top, 
    text="Trip Duration: " + str(json_data["route"]["formattedTime"]) + "\n" + 
    "Distance: \n" +
    "(in mi): " + str("{:.2f}".format(distMi)) + " m \n" +
    "(in km): " + str("{:.2f}".format(distKm)) + " km \n" +
    "(in m): " + str("{:.2f}".format(distM)) + " m \n")
    
    label_output.grid(row=9, column=1, padx=5, pady=10)

def choice2():
    json_data = getInput()

    top = Toplevel()
    top.title("Restrictions")
    top.geometry("200x100")
    top.resizable(False, False) 

    label_output = Label(top, text=
    "Timed restriction: " + str(json_data["route"]["hasSeasonalClosure"]) + "\n" +
    "Seasonal closure: " + str(json_data["route"]["hasSeasonalClosure"]) + "\n" +
    "Country cross: " + str(json_data["route"]["hasCountryCross"]) + "\n")

    label_output.grid(row=9, column=1, padx=5, pady=10)

def choice3():
    json_data = getInput()

    top = Toplevel()
    top.title("Miscellaneous")
    top.geometry("400x100")
    top.resizable(False, False) 

    label_output = Label(top, text=
    "Has toll road: " + str(json_data["route"]["hasTollRoad"]) + "\n" +
    "Has tunnel: " + str(json_data["route"]["hasTunnel"]) + "\n" +
    "Has highway: " + str(json_data["route"]["hasHighway"]) + "\n" +
    # Geo Quality Code
    "Geo Quality Code of " + orig.get() + ": " + (json_data["route"]["locations"][0]["geocodeQualityCode"]) + "\n" +
    "Geo Quality Code of " + dest.get() + ": " + (json_data["route"]["locations"][1]["geocodeQualityCode"]))
    
    label_output.grid(row=9, column=1, padx=5, pady=10)

def choice4():
    json_data = getInput()

    top = Toplevel()
    top.title("Directions")
    top.geometry("200x100")
    top.resizable(False, False) 

    for each in json_data["route"]["legs"][0]["maneuvers"]:
        label_output = Label(top, text=((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)")))
        label_output.grid(row=9, column=1, padx=5, pady=10)

def reset():
    orig.set("")
    dest.set("")
   
# GUI Design
label_orig = Label(window, text="Starting Location: ")
label_orig.grid(row=0, column=0, padx=5, pady=10)

label_dest = Label(window, text="Destination: ")
label_dest.grid(row=1, column=0, padx=5, pady=10)

txtbox_orig = Entry(window, textvariable=orig)
txtbox_orig.grid(row=0, column=1)

txtbox_dest = Entry(window, textvariable=dest)
txtbox_dest.grid(row=1, column=1)

btn_find = Button(window, command=getInput, text="Find")
btn_find.grid(row=2, column=1, sticky=W)

btn_reset = Button(window, command=reset, text="Reset")
btn_reset.grid(row=2, column=2, sticky=W)

window.mainloop()