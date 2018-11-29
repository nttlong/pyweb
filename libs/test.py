import  datetime
x=dict(
    m=123,
    v=[dict(
        k=datetime.datetime.now()
    )]
)
import pyjson
v=pyjson.to_json(x)
print  v