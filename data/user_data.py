from classes.user import User

userLoginFileName = "login-details.txt"
userDetailsFileName = "user-details.txt"


def writeUserDetails(user):
    f = open(userDetailsFileName, "a")
    details = [user.id, user.firstName, user.lastName, user.address, user.phoneNumber]
    f.write(",".join(details))
    f.write("\n")
    f.close()
    return True


def writeUserToFile(user):
    f = open(userLoginFileName, "a")
    userDetails = [user.id, user.userName, user.password, user.userType]
    f.write(",".join(userDetails))
    f.write("\n")
    f.close()
    return True


def getOtherUserDetails(userId):
    f = open(userDetailsFileName, "r")
    data = f.read()
    userData = data.strip().split("\n")
    for user in userData:
        user = user.strip()
        user = user.split(",")
        if user[0] == userId:
            return user
    return None


def getAllUsers():
    allUsers = []
    f = open(userLoginFileName, "r")
    data = f.read().strip()
    users = data.split("\n")
    if not users[0]:
        return None
    for userString in users:
        userString = userString.strip()
        temp = userString.split(",")
        user = User(temp[0], temp[1], temp[2], temp[3])
        otherDetails = getOtherUserDetails(user.id)
        if otherDetails:
            user.firstName = otherDetails[1]
            user.lastName = otherDetails[2]
            user.address = otherDetails[3]
            user.phoneNumber = otherDetails[4]
        allUsers.append(user)
    f.close()
    return allUsers


def getUserForUserId(userId):
    allUsers = getAllUsers()
    for user in allUsers:
        if user.id == userId:
            return user
    return False
