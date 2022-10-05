import requests
from bs4 import BeautifulSoup

url = 'https:// www.linkedin.com/search/results/all /?keywords = python % 20developer'
result = requests.get(url.replace(' ', ''))
doc = BeautifulSoup(result.text, "html.parser")

x = doc.find_all("a", class_="app-aware-link")
print(x)
