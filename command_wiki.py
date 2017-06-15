from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome

# Currently deprecated, as a new input sanitiser is written, which returns a keyword list 
# containing topic which is to be searched from wikipedia
# wikipedia or wiki is a tag word after which search keywords follows
def get_list_of_keywords(text_spoke):
	is_wiki_tag_found = False
	keyword_list = []
	for word in text_spoke.split():
		if is_wiki_tag_found:
			keyword_list.append(word)
		if 'wiki' in word:
			is_wiki_tag_found = True

	return keyword_list



def search_wiki(keywords):
	default_url = 'https://en.wikipedia.org/w/index.php?search='
	search_params = '+'.join(keywords)

	# Chrome option of detach is set to True,
	# so that browser does not closes after script terminates
	opts = ChromeOptions()
	opts.add_experimental_option("detach", True)
	driver = Chrome(chrome_options=opts)
	
	print('Launched chrome driver. Searching: ' + default_url + search_params)
	driver.get(default_url + search_params)

	return 'Wiki search made. Please be patient for the page to load!'

		
