# class Session(object):
#     def __init__(self):
#         from  datetime import datetime
#         self.expiration = datetime
#         self.sid = str
# # class UserLogin (object):
# #     def __init__(self):
# #         import datetime
# #         self.Time = datetime.datetime, True
# #         self.TimeUtc = datetime.datetime, True
# #         self.SessionID = str, True
# #         self.Language = str, True
# # class UserSignOut (object):
# #     def __init__(self):
# #         import datetime
# #         self.Time = datetime.datetime, True
# #         self.TimeUtc = datetime.datetime, True
# #         self.SessionID = str, True
# # class UserProfile (object):
# #     def __init__(self):
# #         import datetime
# #         self.FirstName = str, True
# #         self.LastName = str, True
# #         self.BirthDate = datetime.datetime, True
# class User(object):
#
#     class Logins(object):pass
#     class Signouts(UserSignOut):pass
#     def __init__(self):
#         import datetime
#         self.UserName = str,True # type is text and require
#         self.Email = str,True #Email
#         self.HashPassword = str,True
#         self.PasswordSalt = str,True
#         self.CreatedOn = datetime.datetime,True
#         self.CreatedBy = str,True
#         self.IsSysAdmin =bool,True
#         self.Profile = UserProfile, True
#         self.IsActive = bool,True
#         self.ActivateOn = datetime
#         self.Logins = [UserLogin],True,[]
#         self.Signouts = [UserSignOut],True,[]
#         self.RoleCode = str,True
#         self.Description =str,True
# class Role(object):
#     def __init__(self):
#         self.Code=str,True
#         """Role code"""
#         self.Name = str,True
#         """Name of role"""
#         self.FName = str,True
#         self.Users=[str]
#         self.Description=str
# class AppMethodPrivilegesRequire(object):
#
#     def __init__(self):
#         self.Insert = bool,True,False
#         self.Update = bool, True, False
#         self.Delete = bool, True, False
#         self.View = bool, True, False
#         self.Copy =bool,True,False
#         self.Import = bool, True, False
#         self.Export = bool, True, False
#         self.Print = bool, True, False
#         self.Custom = str, True, ""
# class AppViewMethod(object):
#     def __init__(self):
#         from datetime import datetime
#         self.Name=str,True,None
#         self.Description=str,False,""
#         self.RegisteredOn=datetime,True,datetime.now
#         self.RegisteredOnUtc =datetime.utcnow
#         self.RegisteredBy = str,True
# class AppViewRole(object):
#     def __init__(self):
#         self.Role=str,True
#
# class AppView(object):
#     class Roles(AppViewRole):pass
#     class API(AppViewMethod):pass
#     def __init__(self):
#         self.ViewPath = str, True
#         """ViewPath hold value of controller template path"""
#         self.Url  =str,True
#
#         self.Roles = [AppViewRole],True,[]
#         self.API = [AppViewMethod],True,[]
#         self.Description = str
# class App(object):
#     class Views(AppView):pass
#     def __init__(self):
#         self.AppName=str,True
#         """Application name"""
#         self.Views =[AppView],True,[]
#         """Description of application"""
#         self.Description = str
