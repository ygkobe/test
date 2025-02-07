# -*- coding:utf8 -*-
import requests

url = "http://127.0.0.1:8000/app01/aes/"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4Njc1NTQ4LCJpYXQiOjE3Mzg2NzUyNDgsImp0aSI6ImQ5MGFhNTIxZWQ0NTRmMmNhNjQxZjJhMWVkNGJkZTYzIiwidXNlcl9pZCI6Mn0.8Y-Ia6d9DDgGX9HVYB4jRduf3xmc5dtHqVsxWBXrfuY"

headers = {
    'Authorization': 'Bearer ' + token  # 包含 JWT 令牌
}

response = requests.get(url=url, headers=headers)

print(response.text)
