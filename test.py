import requests

TOKEN = "8753803503:AAFrgbdiJqWVzizGHfCtHME--sNMNJLgFs8"
CHAT_ID = "7668258413"

url = f"https://api.telegram.org/bot{"8753803503:AAFrgbdiJqWVzizGHfCtHME--sNMNJLgFs8"}/sendMessage"

res = requests.post(url, data={
    "chat_id": 7668258413,
    "text": "TEST OK 🔥"
})

print(res.text)