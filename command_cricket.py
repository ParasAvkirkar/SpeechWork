from pycricbuzz import Cricbuzz
from utilities import get_voice_property

import pyttsx
import sys
import os
import datetime

map_to_cricbuzz_country_notation = {
	'india': 'IND',
	'pakistan': 'PAK',
	'australia': 'AUS',
	'england': 'ENG',
	'bangladesh': 'BAN',
	'south africa': 'SA',
	'sri lanka': 'SL'
}

map_to_normal_notation = {
	'IND':'india',
	'PAK':'pakistan',
	'AUS':'australia',
	'ENG':'england',
	'BAN':'bangladesh',
	'SA':'south africa',
	'SL':'sri lanka'
}


def get_countries(text_spoke):
	is_cricket_tag_found = False
	countries = ''
	for word in text_spoke.split():
		if is_cricket_tag_found:
			if 'versus' not in word and 'vs' not in word:
				countries = countries + word + ' ' 
		if 'cric' in word:
			is_cricket_tag_found = True


	return countries.split()[0], countries.split()[1]

# possible values for match state - preview, complete, inprogress, result, innings break


def get_score_live(text_spoke):
	first_team, second_team = get_countries(text_spoke)
	first_team = map_to_cricbuzz_country_notation[first_team]
	second_team = map_to_cricbuzz_country_notation[second_team]
	
	print(first_team + ' vs ' + second_team)

	c = Cricbuzz()
	match_id = -1
	for match in c.matches():
		if match['mchstate'] != 'nextlive' and first_team in match['mchdesc'] and second_team in match['mchdesc']:
			match_id = match['id']


	if match_id == -1:
		raise ValueError('Sorry the match you asked is not live or removed')
	else:
		print('Match Id: ' + match_id)
		score_card = c.scorecard(match_id)
		match_info = score_card['matchinfo']
		score_card = score_card['scorecard']

		first_team_stat = None
		second_team_stat = None
		sentences = []
		if len(score_card) > 1:
			print('Second Innings started')
			first_team_stat = Team_Stat(score_card[1])
			print(str(first_team_stat))
			second_team_stat = Team_Stat(score_card[0])
			print(str(second_team_stat))
			
			sentences.extend(build_sentences(False, first_team_stat, second_team_stat))
		else:
			first_team_stat = Team_Stat(score_card[0])
			sentences.extend(build_sentences(True, first_team_stat, second_team_stat))
			print(first_team_stat)

		say(sentences)

def say(sentences):
	engine = pyttsx.init()
	engine.setProperty('rate', 150)

	voice = get_voice_property(engine, age=10, gender='female')
	engine.setProperty('voice', voice.id)

	for s in sentences:
	    print(s)
	    engine.say(s)

	engine.runAndWait()



def build_sentences(is_first_inning, first_team_stat = None, second_team_stat = None):
	sentences = []
	if is_first_inning:
		sentences.append('{0} made {1} runs with a fall of {2} wickets.'.format(
			first_team_stat.team_name, first_team_stat.runs, first_team_stat.wickets))
		if first_team_stat.wickets < 10:
			sentences.append('{0} overs are remaining.'.format(calculate_overs_notation_from_balls(300 - 
				first_team_stat.balls)))
	else:
		sentences.append('{0} needs {1} runs from {2} balls.'.format(second_team_stat.team_name
			, first_team_stat.runs + 1 - second_team_stat.runs, 300 - second_team_stat.balls))

	return sentences

def calculate_balls_from_overs_notation(overs_notation):
	return int(overs_notation)*6 + int(overs_notation*10) % 10

def calculate_overs_notation_from_balls(balls):
	return float(balls//6) + float(balls%6)/10


class Team_Stat(object):

    def __init__(self, innings_data):
        self.runs = int(innings_data['runs'])
        self.wickets = int(innings_data['wickets'])
        self.team_name = map_to_normal_notation[innings_data['batteam']]
        self.overs = 0.0
        self.last_strike_batsmen = ''
        for stat in innings_data['batcard']:
        	if 'not out' in stat['dismissal']:
        		self.last_strike_batsmen = self.last_strike_batsmen + stat['name'] + ' '
        self.last_strike_batsmen = self.last_strike_batsmen.replace('*', '')
        self.balls = 0
        for b in innings_data['bowlcard']:
        	self.balls += calculate_balls_from_overs_notation(float(b['overs']))
        self.overs = calculate_overs_notation_from_balls(self.balls)
        

    def __str__(self):
    	return 'Team:{0} Runs {1}, Wickets {2}, Overs use {3} Last Strike {4}  Balls {5}'.format(
    		self.team_name, self.runs, self.wickets, self.overs, self.last_strike_batsmen,
    		self.balls)

