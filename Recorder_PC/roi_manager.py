import requests

# Update ROI
update_url = "http://192.168.0.57:12345/update_roi"
update_data = {
    "roi": {
        "x": 100,
        "y": 100,
        "width": 230,
        "height": 200
    }
}
response = requests.post(update_url, json=update_data)
print(response.json())

# Fetch ROI
get_url = "http://192.168.0.57:12345/get_roi"
response = requests.get(get_url)
print(response.json())
