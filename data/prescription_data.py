from classes.drug import Drug

prescriptionFileName = "prescription-details.txt"


def writePrescription(userId, prescriptionId):
    f = open(prescriptionFileName, "a")
    details = [userId, prescriptionId]
    f.write(",".join(details))
    f.write("\n")
    f.close()
    return True


def writeDrugsToPrescription(prescriptionName, drugs):
    f = open("prescriptions/" + prescriptionName + ".txt", "w")
    for drug in drugs:
        data = [drug.drug, drug.amount]
        f.write(",".join(data))
        f.write("\n")
    f.close()
    return True


def getPrescriptionsForUser(userId):
    f = open(prescriptionFileName,"r")
    data = f.read()
    data = data.strip().split("\n")
    userPrescriptions = []
    for prescriptionString in data:
        prescriptionString = prescriptionString.strip().split(",")
        if prescriptionString[0] == userId:
            userPrescriptions.append(prescriptionString[1])
    returnData = []
    if len(userPrescriptions):
        for prescription in userPrescriptions:
            userDrugs = []
            file = open("prescriptions/" + prescription + ".txt", "r")
            data = file.read()
            data = data.strip().split("\n")
            for temp in data:
                drug = temp.strip().split(",")
                userDrugs.append(Drug(drug[0],drug[1]))
            returnData.append(userDrugs)
    return returnData


