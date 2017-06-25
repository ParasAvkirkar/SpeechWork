from pycricbuzz import Cricbuzz
from speech_utilities import speak_sentences

import sys
import os
import traceback
import datetime

# possible values for match state from cricbuzz api
# :- preview, complete, inprogress, result, innings break

map_to_cricbuzz_country_notation = {
	'india': 'IND',
	'pakistan': 'PAK',
	'australia': 'AUS',
	'england': 'ENG',
	'bangladesh': 'BAN',
	'south africa': 'RSA',
	'sri lanka': 'SL',
	'west indies': 'WI',
	'WINDIES':'WI'
}

map_to_normal_notation = {
	'IND':'india',
	'PAK':'pakistan',
	'AUS':'australia',
	'ENG':'england',
	'BAN':'bangladesh',
	'RSA':'south africa',
	'SL':'sri lanka',
	'WI':'west indies',
	'WINDIES':'west indies'
}

map_cricbuzz_month_to_normal_notation = {
	'jan':'January',
	'feb':'February',
	'mar':'March',
	'apr':'April',
	'may':'May',
	'jun':'June',
	'jul':'July',
	'aug':'August',
	'sep':'September',
	'oct':'October',
	'nov':'November',
	'dec':'December'
}

match_type_balls = {
	'ODI':300,
	'T20':120
}

class Team_Stat(object):

    def __init__(self, innings_data):
        self.runs = int(innings_data['runs'])
        self.wickets = int(innings_data['wickets'])
        self.team_name = map_to_normal_notation[innings_data['batteam']]
        self.overs = 0.0
        self.last_strike_batsmen = ''
        for stat in innings_data['batcard']:
        	if 'not out' in stat['dismissal']:
        		self.last_strike_batsmen = self.last_strike_batsmen + stat['name'] + '-'
        self.last_strike_batsmen = self.last_strike_batsmen.replace('*', '')
        self.last_strike_batsmen = self.last_strike_batsmen.replace('!', '')
        self.last_strike_batsmen = self.last_strike_batsmen[:-1]
        self.last_strike_batsmen = self.last_strike_batsmen.replace('-', ' and ')
        self.last_strike_batsmen = self.last_strike_batsmen.replace('(wk)', ' wicket-keeper ')
        self.last_strike_batsmen = self.last_strike_batsmen.replace('(c)', ' captain ')
        self.balls = 0
        for b in innings_data['bowlcard']:
        	self.balls += calculate_balls_from_overs_notation(float(b['overs']))
        self.overs = calculate_overs_notation_from_balls(self.balls)
        

    def __str__(self):
    	return 'Team:{0} Runs {1}, Wickets {2}, Overs use {3} Last Strike {4}  Balls {5}'.format(
    		self.team_name, self.runs, self.wickets, self.overs, self.last_strike_batsmen,
    		self.balls)



# The core handler which does following task by delegating subtasks to other modules:
# 1: Fetch the data from cricbuzz api and filter it into Team_Stat class
# 2: Builds the sentences
# 3: Feeds the sentences to be spoken to a sound device engine
def get_score_live(keywords):
	try:
		c = Cricbuzz()
		# match_basic_info only contains introductory information and not actual match information
		match_basic_info = get_match_basic_info(keywords=keywords, crickbuzz=c)
		
		sentences = []
		if 'inprogress' not in match_basic_info['mchstate'] or 'break' in match_basic_info['mchstate']:
			sentences = build_sentences(match_info=match_basic_info)
			speak_sentences(sentences=sentences)
			return

		match_id = match_basic_info['id']
		
		score_card = c.scorecard(match_id)
		# Actual scorecard dictionary is inside scorecard dictionary return by above API call
		# This happened because the original pycricbuzz API does not had proper naming standard
		match_info = score_card['matchinfo']
		score_card = score_card['scorecard'] 
		
		first_team_stat = None
		second_team_stat = None
		commentary = c.commentary(match_id)
		commentary = commentary['commentary']
		sentences.append(clean_commentary(commentary[0]))
		print(str(len(score_card)) + ' length of scorecard')
		if len(score_card) > 1:
			print('Second Innings started')
			first_team_stat = Team_Stat(score_card[1])
			print(str(first_team_stat))
			second_team_stat = Team_Stat(score_card[0])
			print(str(second_team_stat))
			
			sentences.extend(build_sentences(is_first_inning=False, first_team_stat=first_team_stat,
			 second_team_stat=second_team_stat, match_info=match_info))
		else:
			first_team_stat = Team_Stat(score_card[0])
			print(str(first_team_stat))
			sentences.extend(build_sentences(is_first_inning=True, first_team_stat=first_team_stat,
			 second_team_stat=second_team_stat, match_info=match_info))

		speak_sentences(sentences)
	except ValueError as v:
		speak_sentences([str(v)])
	except Exception as e:
		print(str(traceback.format_exc()))
		raise e



def clean_commentary(commentary):
	commentary = commentary.replace('!!', '!')
	if 'out' in commentary:
		commentary = commentary.split('.')[-1]
		commentary = commentary.replace(' c ' , ' caught by ')
		# commentary = commentary.replace(' ')
	return commentary



def get_match_basic_info(keywords, crickbuzz=None):
	first_team, second_team = get_countries_playing(' '.join(keywords))
	first_team = map_to_cricbuzz_country_notation[first_team]
	second_team = map_to_cricbuzz_country_notation[second_team]
	
	print(first_team + ' vs ' + second_team)

	match_basic_info = None
	for match_basic_info in crickbuzz.matches():
		if is_match_asked_live(match_basic_info, first_team, second_team):
			print(str(match_basic_info))	
			return match_basic_info

	raise ValueError('Sorry the match you asked is not currently live')



def is_match_asked_live(match_basic_info, first_team_asked, second_team_asked):
	return ('ODI' in match_basic_info['type'] or 'T20' in match_basic_info['type']) \
			and match_basic_info['mchstate'] != 'nextlive' \
		 	and first_team_asked in match_basic_info['mchdesc'] \
		 	and second_team_asked in match_basic_info['mchdesc']



# Parses for name of the countries
def get_countries_playing(text_spoke):
	first_team = ''
	second_team = ''
	for country_name in map_to_cricbuzz_country_notation:
		if country_name in text_spoke:
			if not first_team:
				first_team = country_name
			elif not second_team:
				second_team = country_name

	return first_team, second_team



# Build sentences basically creates sentences based on match conditions like
# whether match is complete or first or second innings currently played
def build_sentences(is_first_inning=False, first_team_stat=None, second_team_stat=None, match_info=None):
	sentences = []
	match_type = match_info['type']
	if 'preview' in match_info['mchstate']:
		sentences.append('Match not yet started.')
		sentence = match_info['status']
		sentence = sentence.lower()
		temp = sentence.split()
		for i in range(len(temp)):
			word = temp[i]
			for short_notation in map_cricbuzz_month_to_normal_notation:
				if short_notation in word:
					temp[i] = map_cricbuzz_month_to_normal_notation[short_notation]			

		sentences.append(' '.join(temp))
		return sentences
	
	if 'complete' in match_info['mchstate']:
			sentence = match_info['status']
			sentence = sentence.lower()
			sentence = sentence.replace('wkts', 'wickets')
			for short_notation in map_to_normal_notation:
				if short_notation.lower() in sentence:
					sentence = sentence.replace(short_notation.lower(), map_to_normal_notation[short_notation])

			sentences.append(sentence)
			return sentences

	if 'break' in match_info['mchstate']:
		sentences.append('Innings break is started. Match will start soon!')
		print('Innings break is started. Match will start soon!')
		return

	if is_first_inning:
		sentences.append('{0} made {1} runs with a fall of {2} wickets.'.format(
			first_team_stat.team_name, first_team_stat.runs, first_team_stat.wickets))
		if first_team_stat.wickets < 10 and first_team_stat.balls < match_type_balls[match_type]:
			overs_remaining = calculate_overs_notation_from_balls(match_type_balls[match_type] - first_team_stat.balls)
			
			sentences.append('{0} overs are remaining.'.format(overs_remaining))
			sentences.append('{0} are on crease.'.format(first_team_stat.last_strike_batsmen))

	else:
		print(str(is_first_inning))
		balls_remaining = match_type_balls[match_type] - second_team_stat.balls
		runs_remaining = first_team_stat.runs + 1 - second_team_stat.runs
		sentences.append('{0} needs {1} runs from {2} balls.'.format(second_team_stat.team_name
			, runs_remaining, balls_remaining))

		if second_team_stat.wickets < 10 and second_team_stat.balls < match_type_balls[match_type]:
			sentences.append('{0} wickets have fallen down'.format(second_team_stat.wickets))
			sentences.append('{0} are on crease.'.format(second_team_stat.last_strike_batsmen))

	return sentences



def calculate_balls_from_overs_notation(overs_notation):
	return int(overs_notation)*6 + int(overs_notation*10) % 10



def calculate_overs_notation_from_balls(balls):
	return float(balls//6) + float(balls%6)/10

