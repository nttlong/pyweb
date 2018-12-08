from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from pymongo import MongoClient
from pymongo import database
__session_cache__ = None

class MongoSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False


class MongoSessionInterface(SessionInterface):

    def __init__(self, db, collection='sessions'):
        if isinstance(db,database.Database):
            self.store = db.get_collection(collection)

    def open_session(self, app, request):
        global __session_cache__
        if __session_cache__ == None:
            __session_cache__ = {}
        __session_cache__ = {}
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            if __session_cache__.has_key(sid):
                return __session_cache__[sid]
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    __session_cache__.update({
                        sid:MongoSession(initial=stored_session['data'],sid=stored_session['sid'])
                    })
                    return __session_cache__[sid]
        sid = str(uuid4())
        __session_cache__.update({
            sid: MongoSession(sid=sid)
        })
        return __session_cache__[sid]

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(hours=1)
        import threading
        def update_session_to_store():
            cth = threading.current_thread()
            cth.store.update({
                'sid':cth.sid
            },{
                'sid':cth.sid,
                'data': cth.data,
                'expiration': cth.expiration
            },True)

        th = threading.Thread(target=update_session_to_store)
        setattr(th,"sid",session.sid)
        setattr (th, "data", session)
        setattr (th, "expiration", expiration)
        setattr (th, "store", self.store)
        th.start()
        # self.store.update({'sid': session.sid},
        #                   {'sid': session.sid,
        #                    'data': session,
        #                    'expiration': expiration}, True)
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=self.get_expiration_time(app, session),
                            httponly=True, domain=domain)