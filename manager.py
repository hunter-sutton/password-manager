# Author: Hunter Sutton
# Date: 10/10/2019
# Description: This program is a password manager that stores passwords in an encrypted file.

import json

validCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=,./<>?;\':\"[]{}\|\`~"

# PRINT RESULT
# Parameters: a website that has already been determined to be the only website that the user wants to edit
# Returns: None
# Description: This function prints the login information for the website.
def printResult(website):
    f = open("loginInformation.json", "r")
    loginInformation = json.load(f)
    f.close()
    print("\n=====================================")
    print("Website: " + website)
    print("Username: " + loginInformation[website]["username"])
    print("Password: " + unencrypt(loginInformation[website]["password"]))
    print("=====================================\n")

# INTIATE FILE
# Parameters: None
# Returns: None
# Description: This function creates a file called loginInformation.json if there is not one already. If loginInformation.json already exists, but is empty, it will add a {} to the file.
def initiateFile():
    try:
        f = open("loginInformation.json", "r")
        if f.read() == "":
            f.close()
            f = open("loginInformation.json", "w")
            f.write("{}")
            f.close()
        f.close()
    except FileNotFoundError:
        f = open("loginInformation.json", "w")
        f.write("{}")
        f.close()

# ENCRYPT
# Parameters: string
# Returns: encrypted string
# Description: This function encrypts a string by adding 3 to the ASCII value of each character.
def encrypt(string):
    encryptedString = ""
    for i in range(len(string)):
        encryptedString += chr(ord(string[i]) + 3)
    return encryptedString

# UNENCRYPT
# Parameters: string
# Returns: unencrypted string
# Description: This function unencrypts a string by subtracting 3 from the ASCII value of each character.
def unencrypt(string):
    unencryptedString = ""
    for i in range(len(string)):
        unencryptedString += chr(ord(string[i]) - 3)
    return unencryptedString

# VALIDATE STRING
# Parameters: string
# Returns: True if the string is valid, False if the string is not valid
# Description: This function checks if the string contains characters that are not in validCharacters
def validateString(string):
    for i in range(len(string)):
        if string[i] not in validCharacters:
            return False
    return True

# ADD LOGIN
# Parameters: None
# Returns: returns control to introduction(), usually
# Description: This function adds a login to the loginInformation.json file.
def addLogin():
    f = open("loginInformation.json")
    loginInformation = json.load(f)
    f.close()

    website = input("Website: ")    # get the website from the user
    likelyWebsites = findResults(website)   # find all websites that contain the string that the user entered

    if website in likelyWebsites:   # if the website that the user entered is already in loginInformation.json
        print("Login information for this website already exists!")
        printResult(website)
        introduction();
    else:
        username = input("Username: ")
        if (validateString(username) == False):
            print("Invalid username!")
            introduction();
        
        password = input("Password: ")
        if (validateString(password) == False):
            print("Invalid password!")
            introduction();

        encryptedPassword = encrypt(password)

        loginInformation[website] = {"username": username, "password": encryptedPassword}
        f = open("loginInformation.json", "w")
        json.dump(loginInformation, f)
        f.close()
        print("Login information added!")
        introduction();

# FIND RESULTS
# Parameters: string, a website that the user wishes to find login inforamation for
# Returns: a list of websites that contain the string
# Description: This function returns an array of all websites that contain the string that the user entered.
def findResults(string):
    f = open("loginInformation.json", "r")
    loginInformation = json.load(f)
    f.close()
    websites = []
    for website in loginInformation:
        if string in website:
            websites.append(website)
    return websites

# RETRIEVE LOGIN
# Parameters: none
# Returns: none
# Description: This function retrieves login information for website(s) which contain the string that the user entered.
def retrieveLogin():
    websiteSearch = input("Enter a website to retrieve login information for: ")
    likelyWebsites = findResults(websiteSearch)

    # check if there are no results
    if len(likelyWebsites) == 0:
        print("\nNo results found!\n")
        introduction();

    # print the login information for each website in likelyWebsites
    for website in likelyWebsites:
        printResult(website)
    
    introduction();

# EDIT LOGIN
# Parameters: None
# Returns: returns control to introduction(), usually
# Descirption: This function asks the user for a website to edit login information for, and then asks the user for the new login information. The user can leave a field blank if they do not wish to change it.
def editLogin():
    website = ""
    websiteSearch = input("Enter a website to edit login information for: ")
    websites = findResults(websiteSearch)

    # print the websites and ask the user which one they want to edit, unless there is only one website
    if len(websites) > 1:
        for i in range(len(websites)):
            print(str(i + 1) + ". " + websites[i])
        websiteIndex = int(input("Enter the number of the website you want to edit: "))
        website = websites[websiteIndex - 1]
    elif len(websites) == 1:
        website = websites[0]
    elif len(websites) == 0:
        print("\nNo results found!\n")
        introduction();

    print("\nOriginal login information:")
    printResult(website)

    print("Enter the new login information. Leave a field blank if you do not wish to change it.")
    newUsername = input("Username: ")
    newPassword = input("Password: ")

    f = open("loginInformation.json", "r")
    loginInformation = json.load(f)
    f.close()

    if newUsername != "" and newUsername != loginInformation[website]["username"]:
        f = open("loginInformation.json")
        loginInformation = json.load(f)
        f.close()

        loginInformation[website]["username"] = newUsername

        print("Username changed!")
    
    if newPassword != "" and newPassword != loginInformation[website]["password"]:
        f = open("loginInformation.json")
        loginInformation = json.load(f)
        f.close()

        loginInformation[website]["password"] = encrypt(newPassword)

        print("Password changed!")

    # update the loginInformation.json file
    f = open("loginInformation.json", "w")
    json.dump(loginInformation, f)
    f.close()
    
    print("New login information:")
    printResult(website)
    introduction()

# DELETE LOGIN
# Parameters: None
# Returns: returns control to introduction(), usually
# Description: This function asks the user for a website to delete login information for, and then deletes the login information for that website.
def deleteLogin():
    website = ""
    websiteSearch = input("Enter a website to delete login information for: ")
    websites = findResults(websiteSearch)

    # print the websites and ask the user which one they want to delete, unless there is only one website
    if len(websites) > 1:
        for i in range(len(websites)):
            print(str(i + 1) + ". " + websites[i])
        websiteIndex = int(input("Enter the number of the website you want to delete: "))
        website = websites[websiteIndex - 1]
    elif len(websites) == 1:
        website = websites[0]
    elif len(websites) == 0:
        print("\nNo results found!\n")
        introduction();

    f = open("loginInformation.json", "r")
    loginInformation = json.load(f)
    f.close()

    # ask the user if they are sure they want to delete the login information
    sure = input("Are you sure you want to delete the login information for " + website + "? (y/n): ")
    if sure == "y":
        del loginInformation[website]
        print("Login information deleted!")

    f = open("loginInformation.json", "w")
    json.dump(loginInformation, f)
    f.close()

    introduction()

# INTRODUCTION
# Parameters: None
# Returns: None
# Description: This function prints the introduction to the program.
def introduction():
    print("Welcome to the password manager!")
    print("Please select an option:")
    print("1. Add a Username & Password")       #addLogin()
    print("2. Retrieve Login Information")      #retrieveLogin()
    print("3. Edit Login Information")          #editLogin()
    print("4. Delete Login Information")        #deleteLogin()
    print("5. Exit")                            #exit() 
    option = input("Option: ")
    if option == "1":
        addLogin();
    elif option == "2":
        retrieveLogin();
    elif option == "3":
        editLogin();
    elif option == "4":
        deleteLogin();
    elif option == "5":
        exit();
    else:
        print("Invalid option!")
        introduction();

def main():
    initiateFile()
    introduction()

if (__name__ == "__main__"):
    main()