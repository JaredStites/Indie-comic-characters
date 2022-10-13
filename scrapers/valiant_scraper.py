from bs4 import BeautifulSoup
import requests
import json
import time

categories = {"Name", "Full name", "Aliases", "Universe", "Alignment", "Affiliations", "Family", "Gender", 
"Creators", "First appearance"}

def get_character_info(url_to_character_page):
	print("scraping {}".format(url_to_character_page))
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
	return character

#get_character_info("https://valiant.fandom.com/wiki/Livewire_(Valiant_Entertainment)")

def get_character_pages(character_list_url):
	characters = []
	html = requests.get(character_list_url).text
	soup = BeautifulSoup(html, 'html5lib')
	a_tags = soup.findAll('a', "category-page__member-link", href=True)
	for tg in a_tags:
		if "Category" not in tg["href"]:
			characters.append("https://valiant.fandom.com" + tg["href"])
	return characters

def get_all_character_pages():
	all_characters = []	
	numbers_and_symbols = ['0','1','8','@','¡']
	for letter in range(ord("A"), ord("Z")+1):
		characters_in_letter = get_character_pages("https://valiant.fandom.com/wiki/Category:Characters?from=" + chr(letter))
		for character in characters_in_letter:
			all_characters.append(character)
	for value in numbers_and_symbols:
		characters_with_special_char = get_character_pages("https://valiant.fandom.com/wiki/Category:Characters?from=" + value) 
		for character in characters_with_special_char:
			all_characters.append(character)			
	return all_characters

if __name__ == "__main__":
	characters = []
	urls_to_characters = get_all_character_pages()	
	for url in urls_to_characters:
		char_data = get_character_info(url)
		if not char_data: continue
		else:
			characters.append(char_data)
			time.sleep(2)
	with open('valiant_chars.json', 'w') as jsonfile:
		json.dump(characters, jsonfile)







