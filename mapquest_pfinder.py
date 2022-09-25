# import needed libraries
import urllib.parse
import requests

# Menu definition
def menu():
    print("----------------------------------------")
    print("What would you like to know about \n"+ orig +" to "+ dest +"?")
    print("[1] General Info | [2] Restrictions")
    print("[3] Miscellaneous | [4] Routes")
    print("[0] Exit Menu")
    print("----------------------------------------")

# Import MapQuest API
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "PJv71zxlt65ihzFpAKRuP6HQ3zaCJDQ9"

print("========================================")
print("MapQuest Pathfinder")
print("Improved by Group#8 - 4-ITI")
print("========================================")

while True:
    # Ask user for input regarding starting location & destination
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        print("========================================")
        print("Thank you for using MapQuest Pathfinder!")
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        print("========================================")
        print("Thank you for using MapQuest Pathfinder!")
        break
    
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})

    # Get json data request
    json_data = requests.get(url).json()

    print("----------------------------------------")
    print("URL " + (url))
    print("----------------------------------------")

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    # Output if successful json route call
    if json_status == 0:
        print("API Status " + str(json_status) + " = Congratulations! A successful route call.\n")
        # Options
        menu()
        loop = 1
    
        while loop == 1:
            # Ask user for option number from menu
            option = int(input("Please enter your option: "))

            if option == 1:
                print("SELECTED: General Info")
                print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
                print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
                print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
                
                menu()
            elif option == 2:
                print("SELECTED: Restrictions")
                print("Access restriction: " + str(json_data["route"]["hasAccessRestriction"]))
                print("Timed restriction: " + str(json_data["route"]["hasSeasonalClosure"]))
                print("Seasonal closure: " + str(json_data["route"]["hasSeasonalClosure"]))
                print("Country cross: " + str(json_data["route"]["hasCountryCross"]))
                
                menu()
            elif option == 3:
                print("SELECTED: Miscellaneous")
                print("Has toll road: " + str(json_data["route"]["hasTollRoad"]))
                print("Has tunnel: " + str(json_data["route"]["hasTunnel"]))
                print("Has highway: " + str(json_data["route"]["hasHighway"]))
                
                # Geo Quality Code
                print("Geo Quality Code of " + orig + ": " + (json_data["route"]["locations"][0]["geocodeQualityCode"]))
                print("Geo Quality Code of "+ dest + ": " + (json_data["route"]["locations"][1]["geocodeQualityCode"]))

                menu()
            elif option == 4:
                print("SELECTED: Routes")
                for each in json_data["route"]["legs"][0]["maneuvers"]:
                    print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
                
                menu()
            elif option == 0:
                loop = 0
                print("Thank you for using the menu.")
                print("----------------------------------------")
            else:
                print("Oops! Invalid option. Please choose a number from the menu.")
                menu()

    # Output if unsuccessful json route calls
    elif json_status == 402:
        print("****************************************")
        print("Oops! We encountered an error.")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("****************************************")
    elif json_status == 611:
        print("****************************************")
        print("Oops! We encountered an error.")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("****************************************")
    elif json_status == 500: # Added status code 500
        print("****************************************")
        print("Oops! We encountered an error.")
        print("Status Code: " + str(json_status) + "; The server encountered an error and could not complete your request.")
        print("****************************************")
    elif json_status == 404: # Added status code 404
        print("****************************************")
        print("Oops! We encountered an error.")
        print("Status Code: " + str(json_status) + "; The resource addressed by the request URL does not exist.")
        print("****************************************")
    else:
        print("****************************************")
        print("Oops! We encountered an error.")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("****************************************\n")
