import requests


resp = requests.get(f"http://127.0.0.1:6677/stream_chat/Hi there",stream=True)

