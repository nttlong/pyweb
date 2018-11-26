from pymqr import settings
import pymongo
cnn = pymongo.MongoClient(
    host = "localhost",
    port =27017
)
db = cnn.get_database("db1")
db.authenticate("root","123456")
settings.setdb(db)
import libs.memberships as mb
# mb.create_user(
#     UserName="sys",
#     Password="sys",
#     Email="test"
# )
x=mb.validate_user(UserName="sys",Password="sys123")
print x