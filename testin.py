import requests 
response = requests.get("https://api.nasa.gov/mars-photos/api/v1/manifests/Opportunity?api_key=bkBdrf86b939njkxnSw3kN1Qk6hb8rhgLKLpnT7C")
data = response.json()
print(response.json())