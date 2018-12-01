__lang_cache__ = None
import threading
lock = threading.Lock()
from . import settings
def get_lang_item(language,app_name,view_id,key,value = None):
    app_name = app_name.lstrip(" ").rstrip().lower()
    view_id = view_id.lstrip (" ").rstrip ().lower ()
    language = language.lower()
    if value == None:
        value = key.lstrip (" ").rstrip ()
        key =value
    key = key.lower()
    _k = "lang={0};app={1};view={2};key={3}".format(
        language,
        app_name,
        view_id,
        key
    )
    global __lang_cache__
    if __lang_cache__ == None:
        __lang_cache__ = {}
    if not  __lang_cache__.has_key(_k):
        lock.acquire()
        try:
            import pymqr
            from . import res_models
            qr=  pymqr.query(settings.db,res_models.Languages)
            item = qr.where(pymqr.funcs.expr(
                (res_models.Languages.key==key)&
                (res_models.Languages.language==language) &
                (res_models.Languages.app == app_name) &
                (res_models.Languages.view == view_id))).object
            if item.is_empty():
                ret,error,result = qr.insert({
                    res_models.Languages.language:language,
                    res_models.Languages.app:app_name,
                    res_models.Languages.key:key,
                    res_models.Languages.view:view_id,
                    res_models.Languages.value:value
                }).commit()
                __lang_cache__.update({
                    _k:value
                })
            else:
                __lang_cache__.update({
                    _k: item.value
                })
            lock.release()
        except Exception as ex:
            lock.release()
    return __lang_cache__[_k]



