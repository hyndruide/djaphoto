import requests

url = 'http://127.0.0.1:8000/photo_sync/'
multiple_files = [('image1', ('photo1.jpg', open('photo1.jpg', 'rb'), 'image/jpeg')),
                      ('image2', ('photo2.jpg', open('photo2.jpg', 'rb'), 'image/jpeg'))]
r = requests.post(url, files=multiple_files)