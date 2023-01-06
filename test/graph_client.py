import requests

english_text = (
    "It was the best of times, it was the worst of times, it was the age "
    "of wisdom, it was the age of foolishness, it was the epoch of belief"
)
print(f"English text:\n{english_text}\n")

response = requests.post("http://127.0.0.1:8000/", json=english_text)
french_text = response.text
print(f"French text (summarized and translated):\n{french_text}")