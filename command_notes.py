import datetime
import pickle

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

def take_note(text_spoke):
	try:
		note_content = find_note_content(text_spoke)
		note_name = note_content.split()[0]
		note_content = " ".join(note_content.split()[1:])
		print(note_name + ' ' + note_content)
		save_note(note_name, note_content)
	except Exception as e:
		print(str(e))
		return False

	return True