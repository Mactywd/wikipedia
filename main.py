import json
import requests
import sys
import random


LANG = 'it'

main_url = f"https://{LANG}.wikipedia.org/wiki/"

random_url = f"https://{LANG}.wikipedia.org/api/rest_v1/page/random/summary"
search_url = f"https://{LANG}.wikipedia.org/w/api.php?action=query&srlimit=max&list=search&utf8=&format=json&srsearch="
extract_url = f"https://{LANG}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&formatversion=2&titles="
link_url = f"https://{LANG}.wikipedia.org/w/api.php?action=query&prop=links&format=json&pllimit=max&titles="

if len(sys.argv) > 1:
	query = '_'.join(sys.argv[1:])
else:
	query = requests.get(random_url).json()["titles"]["canonical"]

def print_page(idx, page):
	title = page["title"]
	print(f"{idx}: {title}: {main_url + title.replace(' ', '_')}")

i = 0
while True:
	i += 1
	search_result = requests.get(search_url + query).json()
	pages_found = search_result["query"]["search"]

	page = random.choice(pages_found)
	print_page(i, page)
	
	links_result = requests.get( link_url + query ).json()
	page_id = list(links_result["query"]["pages"].keys())[0]
	try:
		links = [link["title"].replace(' ', '_') for link in links_result["query"]["pages"][page_id]["links"] if not ':' in link["title"]]
	except KeyError:
		pass
		# Means the link doesn't exist
	query = random.choice(links)
