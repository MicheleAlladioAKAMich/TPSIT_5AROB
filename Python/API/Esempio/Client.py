import requests

r = requests.get('http://localhost:5000/api/v1/resources/books/all')
print(r.json())