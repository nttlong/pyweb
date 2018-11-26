class UserIsExist(Exception):
    def __init__(self,Username):
        super(UserIsExist,self).__init__("'{0}' is existing".format(Username))