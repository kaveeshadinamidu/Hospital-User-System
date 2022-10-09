from classes.sick import Sick

sickFileName = "sick-details.txt"


def writeSick(sick, userId):
    f = open(sickFileName, "a")
    details = [userId, sick.description]
    f.write(",".join(details))
    f.write("\n")
    f.close()
    return True


def getAllSickData():
    f = open(sickFileName, "r")
    data = f.read().strip()
    sicks = data.split("\n")
    allSicks = []
    for sickString in sicks:
        sickString = sickString.strip()
        temp = sickString.split(",")
        allSicks.append(Sick(temp[1],temp[0]))
    return allSicks

