from bs4 import BeautifulSoup
import requests
import json
import time

categories = {"Name", "Real Name", "Current Alias", "Aliases", "Identity", "Alignment", "Affiliation", "Relatives", "Gender", 
"Height", "Weight", "Eyes", "Hair", "Marital Status", "Origin", "Creators", "First appearance"}

def get_character_info(url_to_character_page):
	html = requests.get(url_to_character_page).text
	soup = BeautifulSoup(html, 'html5lib')
	character = {}
	try:
		character_info=soup.find('aside')
		character["Name"] = character_info.h2.text.strip()
		items = character_info.findAll('div',"pi-item pi-data pi-item-spacing pi-border-color")
		for item in items:
			key = item.find('h3').text
			if key in categories:
				character[key] = item.find('div', "pi-data-value pi-font").text		
	except:
		print("couldn't scrape: {}".format(url_to_character_page))

	try:
		#First appearance is located in a differently formated section of the aside, so this is used to extract that data
		first_appear_key = 	character_info.find('th', "pi-horizontal-group-item pi-data-label pi-secondary-font pi-border-color pi-item-spacing").text
		first_appear_val = character_info.find('td', "pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing")
		if first_appear_key in categories:
			character[first_appear_key] = first_appear_val.find('div').text
	except:
		print("Missing first appearance info for {}".format(url_to_character_page))
	return character

#get_character_info("https://darkhorse.fandom.com/wiki/Aayla_Secura")

def get_character_pages(character_list_url):
	characters = []
	html = requests.get(character_list_url).text
	soup = BeautifulSoup(html, 'html5lib')
	a_tags = soup.findAll('a', "category-page__member-link", href=True)
	for tg in a_tags:
		if "Category" not in tg["href"]:
			characters.append("https://darkhorse.fandom.com" + tg["href"])
	return characters

def get_all_character_pages():
	characters = get_character_pages("https://darkhorse.fandom.com/wiki/Category:Characters")
	characters2 = get_character_pages("https://darkhorse.fandom.com/wiki/Category:Characters?from=Rufferto")
	for character in characters2:
		characters.append(character)
	return characters


if __name__ == "__main__":
	characters = []
	urls_to_characters = get_all_character_pages()		
	for url in urls_to_characters:
		char_data = get_character_info(url)
		if not char_data: continue
		else:
			characters.append(char_data)
			time.sleep(5)
	with open('dh_chars.json', 'w') as jsonfile:
		json.dump(characters, jsonfile)








