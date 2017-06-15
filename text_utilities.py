from command_notes import take_note
from command_wiki import search_wiki
from command_meaning import find_meaning
from command_cricket import get_score_live

from nltk.corpus import stopwords


possible_stopwords = stopwords.words('english')

dispatcher_based_on_keywords = [
	(['take','note'], take_note),
	(['wikipedia', 'wiki', 'vicky'], search_wiki),
	(['dict', 'meaning'], find_meaning),
	(['cric', 'versus', 'vs'], get_score_live)
]

def sanitize_input(text_spoke):
	words_to_be_removed = []
	dispatcher = None
	for keyword_list_dispatcher_pair in dispatcher_based_on_keywords:
		keyword_list = keyword_list_dispatcher_pair[0]
		is_dispatcher_found = False
		for keyword in keyword_list:
			# print(str(keyword))
			for word in text_spoke.split():
				if keyword in word:
					words_to_be_removed.append(word)
					is_dispatcher_found = True
		
		if is_dispatcher_found:
			dispatcher = keyword_list_dispatcher_pair[1]
			break

	for word in words_to_be_removed:
		if word in text_spoke:
			text_spoke = text_spoke.replace(word, '')

	new_text_list = text_spoke.split()
	for word in text_spoke.split():
		if word in possible_stopwords:
			new_text_list.remove(word)

	print(new_text_list)
	return (dispatcher, new_text_list)

if __name__ == '__main__':
	sanitize_input('take note name hello world')
	sanitize_input('india vs bangladesh')
	sanitize_input('india versus bangladesh')
	sanitize_input('dictionary calumny')
	sanitize_input('meaning of calumny')
	sanitize_input('cricket india versus bangladesh')
	sanitize_input('vicky batman')
	sanitize_input('wikipedia superman')

