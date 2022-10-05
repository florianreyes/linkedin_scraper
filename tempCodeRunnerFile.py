url = 'https:// www.linkedin.com/search/results/all /?keywords = python % 20developer'
result = requests.get(url.replace(' ', ''))
doc = BeautifulSoup(result.text, "html.parser")
print(doc.prettify())

