import datetime
import pickle

# Currently deprecated, as a new input sanitiser is written, which returns a keyword list 
# containing name and content of note
# This method chucks the string before the name tag specified through speech
def find_note_content(text_spoke):
	is_name_tag_found = False
	content = ''
	for word in text_spoke.split():
		if is_name_tag_found:
			content = content + word + ' '
		if 'name' in word:
			is_name_tag_found = True

	return content

def save_note(note_name, note_content):
	note_dict = {'content_type':'note',
					 'name':note_name, 'content':note_content,
					 'timestamp':str(datetime.datetime.now()) }
	with open('notes/'+ note_name + '_' + str(datetime.datetime.now()) + '.pickle', 'wb') as f:
		pickle.dump(note_dict, f)

def take_note(keywords):
	note_name = keywords[0]
	note_content = " ".join(keywords[1:])
	print(note_name + ' ' + note_content)
	save_note(note_name, note_content)

	return 'Note taken'