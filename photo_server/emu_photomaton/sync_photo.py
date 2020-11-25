import hashlib
import os
from datetime import datetime, timezone

import requests


class BoothClient:
    def __init__(self, url, session_key=None):
        self.url = url
        if session_key != None : 
            self.session_key = session_key


    @staticmethod
    def _checksum(fp):
        hash = "sha1"
        pos = fp.tell()
        checksum = hashlib.new(hash, fp.read()).hexdigest()
        fp.seek(pos)
        return f"{hash}:{checksum}"


#revoir pour avoir la date de creation du fichier
    def _now(self,filename):
        
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