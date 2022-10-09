class User:
    def __init__(self,id, userName, password, userType):
        self.phoneNumber = None
        self.firstName = None
        self.lastName = None
        self.address = None
        self.id = id
        self.userName = userName
        self.password = password
        self.userType = userType

    def setUserDetails(self,firstName,lastName,address,phoneNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.phoneNumber = phoneNumber
