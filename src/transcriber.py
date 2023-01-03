import os
import time

import requests


class Transcriber:
    def __init__(self, url: str, key: str = ""):
        self.__url = url
        self.__key = key

    def predict(self, file: str) -> str:
        try:
            _id = self.upload(file)
            finished = False
            while not finished:
                finished = self.is_finished(_id)
                if not finished:
                    time.sleep(1)
            res = self.get_result(_id)
        except BaseException as err:
            raise err
        return res

    def upload(self, file):
        with open(file, 'rb') as f:
            files = {'file': (os.path.basename(file), f.read())}
        values = {'recognizer': 'ben', 'numberOfSpeakers': '1'}
        url = "%s/ausis/transcriber/upload" % self.__url
        headers = {}
        if self.__key:
            headers = {"Authorization": "Key " + self.__key}
        r = requests.post(url, files=files, data=values, timeout=20, headers=headers)
        if r.status_code != 200:
            raise Exception("Can't upload '{}'".format(r.text))
        return r.json()["id"]

    def is_finished(self, _id):
        url = "%s/ausis/status.service/status/%s" % (self.__url, _id)
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise Exception("Can't get status '{}'".format(r.text))
        st = r.json()
        if st.get("error", ""):
            raise Exception(st["error"])
        return st["status"] == "COMPLETED"

    def get_result(self, _id):
        url = "%s/ausis/result.service/result/%s/resultFinal.txt" % (self.__url, _id)
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise Exception("Can't get result '{}'".format(r.text))
        return r.text
