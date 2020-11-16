import requests
import hashlib
import os
def calculate_checksum(filenames):
    hash = hashlib.md5()
    for fn in filenames:
        if os.path.isfile(fn):
            hash.update(open(fn, "rb").read())
    return hash.hexdigest()

files = ['photo1.jpg','photo2.jpg','photo3.jpg']
crchash = calculate_checksum(files)
print(crchash)
url = 'http://127.0.0.1:8000/photo_sync/'
values = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'IDpm': '007', 'crcfiles': crchash}
multiple_files = [(os.path.splitext(image)[0], ( image , open(image, 'rb'), 'image/jpeg')) for image in files]

r = requests.post(url,data = values, files=multiple_files)
print(r.status_code)