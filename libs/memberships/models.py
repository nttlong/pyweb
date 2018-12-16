# import pymqr
# import objects
# @pymqr.documents.EmbededDocument()
# class UserLogin (objects.UserLogin):pass
# @pymqr.documents.EmbededDocument()
# class UserSignOut (objects.UserSignOut):pass
# @pymqr.documents.EmbededDocument()
# class UserProfileProfile (objects.UserProfile):pass
# @pymqr.documents.Collection("users")
# @pymqr.documents.UniqueIndex([
#     "UserName"
# ],["Email"])
# class User(objects.User):pass
# @pymqr.documents.EmbededDocument()
# class UserLogin(objects.UserLogin):pass
# @pymqr.documents.EmbededDocument()
# class UserSignOut(objects.UserSignOut):pass
# @pymqr.documents.Collection("roles")
# @pymqr.documents.UniqueIndex([
#     "Code"
# ])
# class Role(objects.Role):pass
# @pymqr.documents.Collection("apps")
# class App(objects.App):pass
# @pymqr.documents.Collection("sessions")
# class Session(objects.Session):pass