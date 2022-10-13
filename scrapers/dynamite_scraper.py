from bs4 import BeautifulSoup
import requests
import json
import time

categories = {"Name", "Real Name", "Current Alias", "Aliases", "Identity", "Alignment", "Affiliation", "Relatives", "Gender", 
"Height", "Weight", "Eyes", "Hair", "Marital Status", "Origin", "Creators", "First appearance", "Universe"}

def get_character_info(url_to_character_page):
	html = requests.get(url_to_character_page).text
	soup = BeautifulSoup(html, 'html5lib')
	character = {}
	try:
		character_name=soup.select("#mw-content-text > div > div:nth-child(1) > div:nth-child(1)")[0].text.strip()
		character_name = character_name.partition('\n')[0] #Parse the first line only, otherwise it will include unwanted text
		character["Name"] = character_name
		character_info=soup.select("#mw-content-text > div > div:nth-child(1)")
		character_info = character_info[0]
		character_categories = character_info.select('div[style="color: #000; width:90px;float:left;text-align:left;"]')
		character_values = character_info.select('div[style="color: #000; width:160px;float:left;text-align:right;"]')
		items = tuple(zip(character_categories,character_values))
		for item in items:
			key = item[0].text.strip()
			if key in categories:
				character[key] = item[1].text.strip()		
	except:
		# A few pages had information boxes that followed a different format, this scrapes those.
		try:
			character_info=soup.find('aside')
			character["Name"] = character_info.h2.text.strip()
			items = character_info.findAll('div',"pi-item pi-data pi-item-spacing pi-border-color")
			for item in items:
				key = item.find('h3').text
				if key in categories:
					character[key] = item.find('div', "pi-data-value pi-font").text.strip()
				elif key == "First":
					character["First appearance"] = item.find('div', "pi-data-value pi-font").text.strip()	
		except:
			print("couldn't scrape: {}".format(url_to_character_page))

	try:
		#First appearance is located in a differently formated section of the aside, so this is used to extract that data
		first_appear_key = 	character_info.select('div[style="color: #000; width:125px;float:left;"]')[0].text.strip()
		first_appear_val = character_info.select('div[style="color: #000; width:125px;float:left;clear:left;border-top:1px solid #B5B7CF;"]')[0].text.strip()
		character[first_appear_key]=first_appear_val
	except:
		print("Non-standard or missing first appearance info for {}".format(url_to_character_page))
	return character
	

#get_character_info("https://dynamiteentertainment.fandom.com/wiki/Queen_Maeve_(Earth-UU011)")
#get_character_info("https://imagecomics.fandom.com/wiki/Rachel_Goldman")

def get_character_pages(character_list_url):
	characters = []
	html = requests.get(character_list_url).text
	soup = BeautifulSoup(html, 'html5lib')
	a_tags = soup.findAll('a', "category-page__member-link", href=True)
	for tg in a_tags:
		if "Category" not in tg["href"]:
			characters.append("https://dynamiteentertainment.fandom.com" + tg["href"])
	return characters

def get_all_character_pages():
	all_characters = []	
	for letter in range(ord("A"), ord("Z")+1):
		characters_in_letter = get_character_pages("https://dynamiteentertainment.fandom.com/wiki/Category:Characters?from=" + chr(letter))
		for character in characters_in_letter:
			all_characters.append(character)
	return all_characters

#get_character_pages("https://imagecomics.fandom.com/wiki/Category:Characters_by_Name_B")

if __name__ == "__main__":
	characters = []
	urls_to_characters = get_all_character_pages()		
	for url in urls_to_characters:
		char_data = get_character_info(url)
		if not char_data: continue
		else:
			characters.append(char_data)
			time.sleep(2)
	with open('dynamite_ent_chars.json', 'w') as jsonfile:
		json.dump(characters, jsonfile)







