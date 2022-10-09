from classes.lab_test import LabTest

labTestPrescriptionFileName = "lab-test-data.txt"


def writeLabTest(labTest):
    f = open(labTestPrescriptionFileName, "a")
    data = [labTest.userId, labTest.type, labTest.description]
    f.write(",".join(data))
    f.write("\n")
    f.close()
    return True


def getAllLabTests():
    f = open(labTestPrescriptionFileName, "r")
    fileData = f.read()
    data = fileData.strip().split("\n")
    labTests = []
    for testString in data:
        labTestData = testString.strip()
        labTestData = labTestData.split(",")
        labTests.append(LabTest(labTestData[1], labTestData[2], labTestData[0]))
    f.close()
    return labTests


def getLabTestsForUser(userId):
    userLabTests = []
    labTests = getAllLabTests()
    for labTest in labTests:
        if labTest.userId == userId:
            userLabTests.append(labTest)
    return userLabTests
