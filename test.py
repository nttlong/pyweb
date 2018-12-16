# import models.categories as cat
import pymongo
cnn = pymongo.MongoClient(
    host="localhost",
    port=27017
)
db=cnn.get_database("db1")
db.authenticate("root","123456")
import pymqr
# qr =  pymqr.query(db,cat.JobWrk)
#
# x=list(qr.items)
# x=cat.jobwrk.JobWrk.CombineProcess<<{}
@pymqr.documents.Collection("x.xx")
class X(object):
    @pymqr.documents.EmbededDocument()
    class Y(object):
        @pymqr.documents.EmbededDocument()
        class Z(object):
            def __init__(self):
                self.Name=str,True,"XXX"
                pass
        def __init__(self):
            pymqr.documents.EmbeddedField(self,"Z",True,None)
            self.Name=str,True,None
# x=X.Y<<{}
fx=pymqr.docs.X.Y
y=fx<<{}
x=X.Y.Z<<{
    "XXX":123
}
print x