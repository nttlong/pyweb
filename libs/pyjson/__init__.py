import datetime
def __fix_date__(obj_dict):
    if isinstance(obj_dict,dict):
        for k,v in obj_dict.items():
            if isinstance(v,datetime.datetime):
                obj_dict.update({
                    k:datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
                })
            elif isinstance(v,dict):
                obj_dict.update({
                    k:__fix_date__(v)
                })
        return obj_dict
    else:
        raise Exception("Invalid params {0}".format(type(obj_dict)))

def to_json(obj):
    import json
    if isinstance(obj,dict):
        return json.dumps(__fix_date__(obj))
    elif hasattr(obj,"to_dict"):
        return json.dumps (__fix_date__ (obj.to_dict()))
    elif hasattr(obj,"__dict__"):
        return json.dumps (__fix_date__ (obj.__dict__))






