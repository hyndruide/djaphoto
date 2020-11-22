import hashlib
import os
from datetime import datetime, timezone

import requests


class BoothClient:
    def __init__(self, url, session_key):
        self.url = url
        self.session_key = session_key

    @staticmethod
    def _checksum(fp):
        hash = "sha1"
        pos = fp.tell()
        checksum = hashlib.new(hash, fp.read()).hexdigest()
        fp.seek(pos)
        return f"{hash}:{checksum}"

    @staticmethod
    def _now():
        d = datetime.utcnow()
        d = d.replace(tzinfo=timezone.utc)
        return d

    def upload(self, filename):
        with open(filename, "rb") as fp:
            data = {
                "name": os.path.basename(filename),
                "checksum": self._checksum(fp),
                "created_at": self._now().isoformat(),
            }
            headers = {"Authorization": self.session_key}

            url = f"{self.url}/photo/upload"

            files = [("file", fp)]
            with requests.post(url, data=data, files=files, headers=headers) as r:
                if not r.ok:
                    raise ValueError(r.text)
                return r.json()
