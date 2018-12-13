import models.categories as cat
import pymongo
cnn = pymongo.MongoClient(
    host="localhost",
    port=27017
)
db=cnn.get_database("db1")
db.authenticate("root","123456")
import pymqr
qr =  pymqr.query(db,cat.JobWrk)
x=list(qr.items)
print x