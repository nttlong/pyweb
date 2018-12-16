import pymqr
@pymqr.documents.Collection("xx")
class Test(object):
    @pymqr.documents.EmbededDocument()
    class A(object):
        class C(object):
            def __init__(self):
                self.Test=str,True,None
        def __init__(self):
            self.Y=int,True,0
            pymqr.documents.EmbeddedField(self,"C",True,None)
    def __init__(self):
        pymqr.documents.EmbeddedFieldArray(self,"A",True)
