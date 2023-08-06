from hashlib import sha256
import zlib
import pickle
import time
from base64 import b64decode,b64encode
import logging
import requests
from .model import Key


MSG_DB = "~/.qqbot-tmp/msg-db.sql"

def data_fact(data, en=False, if_zip=True):
    if isinstance(data, str):
        data = data.encode('utf-8')

    if en:
        if if_zip:
            data = zlib.compress(data)
        mac = sha256(data).hexdigest()
        return data, if_zip, mac
    else:
        mac = sha256(data).hexdigest()
        if if_zip:
            data = zlib.decompress(data)
        return data, if_zip, mac


def obj2data(objs, if_zip=True):
    data = pickle.dumps(objs)
    en_data, if_zip, mac = data_fact(data, en=True, if_zip=if_zip)
    return en_data, if_zip, mac

def data2obj(data, if_zip=True):
    data,if_zip,mac = data_fact(data, if_zip=if_zip)
    return pickle.loads(data), if_zip, mac

def package(obj, if_zip=True):
    bdata, if_zip, mac = obj2data(obj, if_zip)
    bdata = b64encode(bdata).decode('utf-8')
    return {
        'data':bdata,
        'if_zip':if_zip,
        'mac':mac
    }

def unpackage(obj, if_zip=True):
    data = obj['data'].encode('utf-8')
    if_zip = obj['if_zip']
    mac = obj['mac']
    data = b64decode(data)
    objs, if_zip, lmac = data2obj(data, if_zip)
    if mac != lmac:
        logging.warn("Msg is check failed!")
    return objs


class MsgMan:
    d = []
    init_time = None

    def __init__(self, ti=5, api='http://localhost:14144/'):
        self._time = ti
        if not MsgMan.init_time :
            MsgMan.init_time  = time.time()

        self.api= api

    def save(self, msg):
        MsgMan.d.append(msg)

    def test(self):
        res = requests.get("http://localhost:14144/")
        if res.status_code == 200:
            return True
        return False

    def clear(self):
        MsgMan.d = []
        MsgMan.init_time = time.time()

    def syncs_msg(self, msg):
        n = time.time()
        l = MsgMan.init_time
        api = self.api
        q = self._time
        self.save(msg)
        if n - l > q:
            msgs = MsgMan.d
            data = package(msgs)
            # print("test ... res = requests.post(api, data=data).json()")
            print(data)
            res = requests.post(api, data=data).text
            print(res)
            self.clear()
        else:
            print('collect:', len(MsgMan.d))


