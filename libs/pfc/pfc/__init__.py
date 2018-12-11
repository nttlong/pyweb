VERSION = [0,0,1,3]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()
def get_user_name():
    import threading
    if hasattr(threading.current_thread(),"user_name"):
        return threading.current_thread().user_name
    else:
        return "application"
