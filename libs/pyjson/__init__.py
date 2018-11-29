import datetime
def __fix_date__(obj_dict):
    if isinstance(obj_dict,dict):
        for k,v in obj_dict.items():
            if isinstance(v,datetime.datetime):
                obj_dict.update({
                    k:v.strftime("%Y-%m-%dT%H:%M:%S")
                })

            elif isinstance(v,dict):
                obj_dict.update({
                    k:__fix_date__(v)
                })
            elif isinstance(v,list):
                for x in v:
                    __fix_date__ (x)
        return obj_dict
    elif isinstance (obj_dict, list):
        for x in obj_dict:
            __fix_date__ (x)
    else:
        return obj_dict

def to_json(obj):
    import json
    if isinstance(obj,dict):
        return json.dumps(__fix_date__(obj))
    elif isinstance(obj,list):
        for item in obj:
            __fix_date__(item)
        return json.dumps(obj)

    elif hasattr(obj,"to_dict"):
        return json.dumps (__fix_date__ (obj.to_dict()))
    elif hasattr(obj,"__dict__"):
        return json.dumps (__fix_date__ (obj.__dict__))






