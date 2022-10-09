import hashlib
import uuid
from getpass import getpass
from classes.drug import Drug
from classes.lab_test import LabTest
from classes.sick import Sick
from data.lab_test_prescription_data import writeLabTest, getLabTestsForUser, getAllLabTests
from data.prescription_data import writePrescription, writeDrugsToPrescription, getPrescriptionsForUser
from data.sick_data import writeSick, getAllSickData
from data.user_data import writeUserToFile, getAllUsers, writeUserDetails, getUserForUserId
from classes.user import User


# Method to hash the password of a user when registering
def createHash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


# Method to add the lab test for a user
# Only a doctor can execute this function
def addLabTest(user):
    labTestUser = None
    while True:
        labTestUser = input("Enter the patient username: ")
        if labTestUser:
            break
        else:
            print("Invalid input")
    allUsers = getAllUsers()
    patient = None
    matched = False
    for tempUser in allUsers:
        if tempUser.userName == labTestUser:
            patient = tempUser
            matched = True
    if not matched:
        print("No any respective user found")
    else:
        print("Enter the lab test details")
        type = input("Enter the type: ")
        description = input("Enter the description: ")
        test = LabTest(type, description, patient.id)
        writeLabTest(test)
        print("Lab test recorded successfully")


# Method to add prescription by the doctor
# This method can only executed from doctor's account
def addPrescription(user):
    prescriptionUser = input("Enter the patient username: ")
    allUsers = getAllUsers()
    patient = None
    matched = False
    for tempUser in allUsers:
        if tempUser.userName == prescriptionUser:
            patient = tempUser
            matched = True
    if not matched:
        print("No any respective user found")
    else:
        print("Enter the drugs for the prescription. After entering all the drug enter exit command")
        allDrugs = []
        prescriptionId = str(uuid.uuid4())
        writePrescription(patient.id, prescriptionId)
        while True:
            userInput = input("Enter drug: drug name, amount : ")
            if userInput == 'exit':
                break
            drugTemp = userInput.split(",")
            drug = Drug(drugTemp[0].strip(), drugTemp[1].strip())
            allDrugs.append(drug)
        writeDrugsToPrescription(prescriptionId, allDrugs)


# Method to add a sick details for a patient
def addSick(user):
    description = input("Enter sick description: ")
    sick = Sick(description, user.id)
    if writeSick(sick, user.id):
        print("Sickness details added succesfully !!")
    else:
        print("Error occured while adding sickness details !!")


# Method to shows the drugs of a user
def showUserDrugs(userDrugs):
    i = 1
    for drugs in userDrugs:
        print("Prescription : ", i)
        for drug in drugs:
            print("Drug Name: " + drug.drug + " amount: " + drug.amount)
        i += 1


# Method to show the lab tests of users
def showUserLabTests(userLabTest):
    i = 1
    for labTest in userLabTest:
        print("Lab test: ", i)
        print("Lab test type: ", labTest.type)
        print("Lab test description: ", labTest.description)
        print("")


# Method which shows the patient actions and get their inputs accordingly
def patientActions(user):
    print("Welcome to the system !!!")
    print("Enter 1 to add a sick details")
    print("Enter 2 to view your prescriptions")
    print("Enter 3 to view your lab tests")
    print("Enter 0 to logout")
    userInput = input()
    if userInput == '1':
        addSick(user)
    elif userInput == '2':
        userDrugs = getPrescriptionsForUser(user.id)
        showUserDrugs(userDrugs)
    elif userInput == '3':
        userLabTests = getLabTestsForUser(user.id)
        showUserLabTests(userLabTests)
    elif userInput == '0':
        return
    newInput = input("Enter 0 to exit and press any key to continue: ")
    if newInput == '0':
        return
    patientActions(user)


# Method which shows the sickness details of the patients
def showAllSickData(sickData):
    i = 1
    for sick in sickData:
        print("Sick details: ", i)
        user = getUserForUserId(sick.user)
        print("Username: ", user.userName)
        print("Sick description: ", sick.description)
        print("")
        i += 1


# Method which shows all the lab tests
def showAllLabTests(labTests):
    i = 1
    for labTest in labTests:
        user = getUserForUserId(labTest.userId)
        print("Username: ",user.userName)
        print("Lab test : ",i)
        print("Lab test type: ",labTest.type)
        print("Lab test description: ",labTest.description)
        print("")
        i += 1


# Method shows all the users in the system
def showAllUsers(allUsers):
    i = 1
    for user in allUsers:
        print("User: ",i)
        print("Username: ",user.userName)
        print("Firstname: ",user.firstName)
        print("Lastname: ",user.lastName)
        print("Address: ",user.address)
        print("Phone Number: ",user.phoneNumber)
        print(" ")
        i += 1


# Method which shows the action of the hospital staff
def staffActions(user):
    print("Welcome to the system !!!")
    print("Enter 0 to logout")
    print("Enter 1 to see the sick details of patients !!!")
    if user.userType == 'DOCTOR':
        print("Enter 2 to Give prescriptions for patients")
        print("Enter 3 to view all lab tests")
        print("Enter 5 to add lab test")
    if user.userType == 'NURSE':
        print("Enter 3 to view all lab tests")
    if user.userType == 'ADMIN':
        print("Enter 4 to view user details")
    userInput = input()
    if userInput == '1':
        sickData = getAllSickData()
        showAllSickData(sickData)
    elif userInput == '2' and user.userType == 'DOCTOR':
        addPrescription(user)
    elif userInput == '3' and (user.userType == 'DOCTOR' or user.userType == 'NURSE'):
        labTests = getAllLabTests()
        showAllLabTests(labTests)
    elif userInput == '4' and user.userType == 'ADMIN':
        allUsers = getAllUsers()
        showAllUsers(allUsers)
    elif userInput == '5' and user.userType == 'DOCTOR':
        addLabTest(user)
    elif userInput == '0':
        return
    newInput = input("Enter 0 to logout or press any key to proceed: ")
    if newInput == '0':
        return
    staffActions(user)


# Method of authenticate the user by username and password
def loginUser():
    while True:
        userName = input("Enter username: ")
        if userName:
            break
        else:
            print("Username is required !")
    while True:
        passWord = getpass("Enter password: ")
        if passWord:
            break
        else:
            print("Password is required !")
    allUsers = getAllUsers()
    matched = False
    for user in allUsers:
        if user.userName == userName:
            matched = True
            if user.password == createHash(passWord):
                if user.userType == "PATIENT":
                    patientActions(user)
                else:
                    staffActions(user)
            else:
                print("Invalid username or password")
    if not matched:
        print("Invalid username or password")


# Method to take other user details
def getUserOtherDetails(user):
    while True:
        user.firstName = input("Enter first name: ")
        if user.firstName:
            break
        else:
            print("User firstname is required !")
    while True:
        user.lastName = input("Enter last name: ")
        if user.lastName:
            break
        else:
            print("User lastname is required !")
    while True:
        user.address = input("Enter address (do not add , while entering): ")
        if user.address:
            break
        else:
            print("User address is required !")
    while True:
        user.phoneNumber = input("Enter phone number: ")
        if user.phoneNumber and len(user.phoneNumber) == 10:
            break
        else:
            print("Invalid input")
    if writeUserDetails(user):
        print("User details added succesfully!")
    else:
        print("Error occured while adding the details")


# Method of registering the user
def registerUser():
    userName = None
    passWord = None
    while True:
        userName = input("Enter username: ")
        allUsers = getAllUsers()
        foundOne = False
        if not allUsers:
            break
        for user in allUsers:
            if user.userName == userName:
                foundOne = True
        if foundOne:
            print("User already exists !!!")
            userName = None
        if userName:
            break
        else:
            print("Username is required !")
    while True:
        passWord = getpass("Enter password: ")
        if passWord:
            break
        else:
            print("Password is required !")
    userType = ""
    while True:
        print("Enter user type: ")
        print("1. Patient")
        print("2. Nurse")
        print("3. Doctor")
        print("4. Admin")
        userTypeInput = input()
        if userTypeInput == '1':
            userType = "PATIENT"
        elif userTypeInput == '2':
            userType = 'NURSE'
        elif userTypeInput == '3':
            userType = "DOCTOR"
        elif userTypeInput == '4':
            userType = 'ADMIN'
        if userType:
            break
        else:
            print("User type is required !")
    user = User(str(uuid.uuid4()), userName, createHash(passWord), userType)
    if writeUserToFile(user):
        print("User registration success!")
        getUserOtherDetails(user)
        loginUser()
    else:
        print("User registration failed")


# main method which takes user details and
# authenticate user
def getLoginOrRegister():
    print("Welcome !!!")
    print("Do you want to register or login?")
    print("Enter 1 to login")
    print("Enter 2 to register")
    print("Enter 0 to exit")
    inputType = input()
    if inputType == "2":
        registerUser()
    elif inputType == "1":
        loginUser()
    elif inputType == "0":
        return
    else:
        print("Invalid input")
    getLoginOrRegister()


if __name__ == '__main__':
    getLoginOrRegister()
