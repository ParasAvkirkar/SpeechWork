from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome


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



def search_wiki(text_spoke):
	try:
		keyword_list = get_list_of_keywords(text_spoke)
		default_url = 'https://en.wikipedia.org/w/index.php?search='
		search_params = '+'.join(keyword_list)

		# Chrome option of detach is set to True,
		# so that browser does not closes after script terminates
		opts = ChromeOptions()
		opts.add_experimental_option("detach", True)
		driver = Chrome(chrome_options=opts)
		
		print('Launched chrome driver. Searching: ' + default_url + search_params)
		driver.get(default_url + search_params)
		
		return True
	except Exception as e:
		print(str(e))
		return False