from pycricbuzz import Cricbuzz


map_to_cricbuzz_country_notation = {
	'india': 'IND',
	'pakistan': 'PAK',
	'australia': 'AUS',
	'england': 'ENG',
	'bangladesh': 'BAN',
	'south africa': 'SA',
	'sri lanka': 'SL'
}

def get_countries(text_spoke):
	is_cricket_tag_found = False
	countries = ''
	for word in text_spoke.split():
		if is_cricket_tag_found:
			if 'versus' not in word:
				countries = countries + word + ' ' 
		if 'cric' in word:
			is_cricket_tag_found = True


	return countries.split()[0], countries.split()[1]

# possible values for match state - preview, complete, inprogress, result


def get_score_live(text_spoke):
	first_team, second_team = get_countries(text_spoke)
	first_team = map_to_cricbuzz_country_notation[first_team]
	second_team = map_to_cricbuzz_country_notation[second_team]
	print(first_team + ' ' + second_team)

	c = Cricbuzz()
	match_id = -1
	for match in c.matches():
		if match['mchstate'] != 'nextlive' and first_team in match['mchdesc'] and second_team in match['mchdesc']:
			match_id = match['id']

	if match_id == -1:
		raise ValueError('Sorry the match you asked is not live or removed')
	else:
		pass

