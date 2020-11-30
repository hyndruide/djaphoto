import hashlib
import os
from datetime import datetime, timezone
import time
import json
import requests


class BoothClient:
    def __init__(self, url='http://127.0.0.1:8000'):
        self.url = url
        self.session_key = None

    @staticmethod
    def _checksum(fp):
        hash = "sha1"
        pos = fp.tell()
        checksum = hashlib.new(hash, fp.read()).hexdigest()
        fp.seek(pos)
        return f"{hash}:{checksum}"

    def _now(self, filename):
        dt = os.path.getctime(filename)
        dt = datetime.utcfromtimestamp(dt)
        dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def upload(self, filename):
        with open(filename, "rb") as fp:
            data = {
                "name": os.path.basename(filename),
                "checksum": self._checksum(fp),
                "created_at": self._now(filename).isoformat(),
            }
            headers = {
                "Authorization": f"bearer {self.session_key}",
            }

            url = f"{self.url}/photo/upload"

            files = [("file", fp)]
            with requests.post(url, data=data, files=files, headers=headers) as r:
                if not r.ok:
                    raise ValueError(r.text)
                return r.json()

    def _first_connect(self):
        url = f"{self.url}/connexion/new"
        with requests.get(url) as r:
            if not r.ok:
                raise ValueError(r.text)
            return r.json()

    def wait_first_connect(self, connect_code):
        url = f"{self.url}/connexion/wait"
        headers = {
                "Authorization": f"bearer {connect_code}",
            }
        with requests.post(url, headers=headers) as r:
            if not r.ok:
                return True
            if r.json()['is_valid'] is True:
                self.store_key(r.json()['session_key'])
                return False

    def connect(self):
        if self.update_session_key() is False:
            return False
        url = f"{self.url}/connexion"
        headers = {
            "Authorization": f"bearer {self.session_key}",
        }

        with requests.post(url, headers=headers) as r:
            if not r.ok:
                raise ValueError(r.text)
            return r.json()

    def store_key(self, key):
        session_key = {"key": key}
        with open('keyfile', 'w') as f1:
            json.dump(session_key, f1)
        self.update_session_key()

    def _get_key(self):
        if os.path.isfile('keyfile'):
            with open('keyfile', 'r') as key:
                return json.load(key)['key']
        else:
            return None

    def update_session_key(self):
        session_key = self._get_key()
        if session_key is None:
            return False
        self.session_key = session_key


if __name__ == "__main__":
    photo = BoothClient()
    r = photo._first_connect()
    print(r['code_connexion'])
    while photo.wait_first_connect(r['code_connexion']):
        time.sleep(3)
    print("photomaton validé")
