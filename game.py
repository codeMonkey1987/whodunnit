# Python Detective Game - Case #1
# by Preston Maynard

import cmd
import textwrap
import sys
import os
import time 
import math

#### Player and Character Setup ####
class player: 
	def __init__(self):
		self.name = ''
		self.location = 'a1'
		self.game_over = False
myPlayer = player()



#### Title Screen ####
def title_screen_selections():
	option = input("> ")
	if option.lower() == ("play"):
		setup_game()
	elif option.lower() == ("help"):
		help_menu()
	elif option.lower() == ("quit"):
		sys.exit()
	while option.lower() not in ["play", "help", "quit"]:
		print("What would you like to do?")
		option = input("> ")
		if option.lower() == ("play"):
			setup_game()
		elif option.lower() == ("help"):
			help_menu()
		elif option.lower() == ("quit"):
			sys.exit()

def title_screen():
	os.system('clear')
	print('                        #################################')
	print('                        # Welcome to the Detective Game #')
	print('                        #################################')
	print('                        #           - Play -            #')
	print('                        #           - Help -            #')
	print('                        #           - Quit -            #')
	print('                        #################################')
	title_screen_selections()

def help_menu():
	print('                    #########################################')
	print('                    #     Welcome to the Detective Game     #')
	print('                    #########################################')
	print('                    # -  You will use a set of commands   - #')
	print('                    # -   Type your commands to do them   - #')
	print('                    # - Type "help" in game for more info - #')
	print('                    #########################################')
	title_screen_selections()


suspects = []
evidence = []
items_found = []
persons = ['liz rhodes', 'dave smith', 'tony jobs', 'steve perry']
discoveries = {'disc1': False, 'disc2': False, 'disc3': False, 'disc4': False,
				'disc5': False, 'disc6': False, 'disc7': False, 'disc8': False,
				'disc9': False,  'disc10': False, 'disc11': False, 'bRhodes': False, 
			}

zone_map = {
	'a1': dict(
		ZONENAME = "Jewelry Store",
		DESCRIPTION = 'Showroom',
		EXAMINATION = "You see a showroom full of glass cases, all of which have been cleaned out."
					"\nThere are also at least 3 security cameras in the room."
					"\nAt the entrance stands Officer Gibbs."
					"\nNear the showcases stands Liz Rhodes." 
					"\nNear the manager's office stands Dave Smith.",
		searched_objects = {
			'cases': False
		},
		object_desc = {
			'cases': 'You find nothing looking around the display cases.'
		},
		discov = {},
		items = {},

	),
	'a2': dict(
		ZONENAME = "Jewelry Store",
		DESCRIPTION = "Manager's Office",
		EXAMINATION = "You see a normal looking office. Tony Jobs sits at his desk."
					"\nThere is a laptop on the desk and a filing cabinet in the corner."
					"\nThe office is very clean, and smells of pinewood.",
		searched_objects = {
			'desk': False, 'filing cabinet': False, 'laptop': False,
		},
		object_desc = {
			'desk': 'You find a gun in the top drawer. It\'s not loaded.',
			'filing cabinet': 'You look through the files in the drawers, but you find nothing of interest.',
			'laptop': 'You find a spreadsheet of Tony Job\'s finances.\nHe seems to be in a great deal of debt.\
					\nYou also see emails to Steve Perry, warning him that leaving the store during \
					\nbusiness hours will result in disciplinary actions.'
		},
		discov = {
			'laptop': 'disc3'
		},
		items = {
			'laptop': 'spreadsheet', 'desk': 'empty gun'
		},
	),
	'a3': dict(
		ZONENAME = "Jewelry Store",
		DESCRIPTION = 'Closet',
		EXAMINATION = "You see some racks along the north wall and boxes stacked in the corner."
					"\nAlong the south wall are some dusty cabinets."
					"\nThe room smells of cleaning products and building materials.",
		searched_objects = {
			'racks': False, 'boxes': False, 'cabinets': False,
		},
		object_desc = {
			'racks': 'The racks are full of paint cans, rollers, and brushes.',
			'boxes': 'After looking around every box, you find nothing.',
			'cabinets': 'Looks like mostly cleaning supplies.',
		},
		discov = {
		
		},
		items = {},
		
	),
	'a4': dict(
		ZONENAME = "Jewelry Store",
		DESCRIPTION = 'Security Office',
		EXAMINATION = "You see a long table along the north wall with CCTV monitors."
					"\nThere is a computer at the end of the table."
					"\nA garbage can has been kicked over and spilled on the floor."
					"\nSteve Perry stands by the door.",
		searched_objects = {
			'cctv': False, 'computer': False, 'garbage can': False,
		},
		object_desc = {
			'garbage can': 'The garbage can has been knocked over, spilling empty coffee cups and wrappers \
							\non the floor. The coffee cups are from the coffee shop down the street.',
			'computer': 'Steve Perry\'s email is open, but there seems to be nothing in his inbox.',
			'cctv': 'The monitors show multiple angles of the showroom, Tony Job\'s office, security, \
					\nand the hallway leading to security.',
		},
		discov = {
		
		},
		items = {
			'garbage can': 'coffee cups'
		},
	),
	'b1': dict(
		ZONENAME = "Tony Jobs' Apartment",
		DESCRIPTION = 'Living Room',
		EXAMINATION = 'Everything in the living room is neat and orderly. The coffee'
					" table is covered\nin mail. A rustic fireplace along the west wall "
					"stands out along an otherwise\nmodern decor. "
					"An assisting officer stands by the exit.",
		searched_objects = {
			'coffee table': False, 'fireplace': False,
		},
		object_desc = {
			'coffee table': 'The coffee table is covered in letters from debt collectors and banks.',
			'fireplace': 'There are burned bits of paper in the fireplace. Possibly letters.',
		},
		discov = {
		
		},
		items = {},
		
	),
	'b2': dict(
		ZONENAME = "Tony Jobs' Apartment",
		DESCRIPTION = 'Dining Room',
		EXAMINATION = 'You look around and see nothing of interest.',
		searched_objects = {},
		object_desc = {},
		discov = {},
		items = {},
		
	),
	'b3': dict(
		ZONENAME = "Tony Jobs' Apartment",
		DESCRIPTION = 'Bedroom',
		EXAMINATION = 'You see a large blue bedroom with a king sized bed. Next to the '
					"bed is a\nnighstand, and a matching dresser to the right of the bed."
					"\nAn open closet is on your left.",
		searched_objects = {
			'nightstand': False, 'closet': False, 'dresser': False,
		},
		object_desc = {
			'nightstand': 'There is an empty bottle of wine with two glasses.',
			'closet': 'The closet it full of Tony\'s clothes, but there are also a woman\'s clothes.',
			'dresser': 'On the dresser is a picture frame. The picture is of Tony and Liz Rhodes, \
						\nlooking quite close, and a third person you don\'t recognize.',
		},
		discov = {
			'dresser': 'disc5'
		},
		items = {
			'dresser': 'picture', 'nightstand': 'empty wine'
		},
		
	),
	'b4': dict(
		ZONENAME = "Tony Jobs' Apartment",
		DESCRIPTION = 'Office',
		EXAMINATION = 'The office looks like a quiet study. The only thing that truly stands'
					' out is the\nlarge safe in the corner.',
		searched_objects = {
			'safe': False,
		},
		object_desc = {
			'safe': 'The safe is locked.'
		},
		discov = {},
		items = {},

	),
	'c1': dict(
		ZONENAME = "Barry Rhodes' Apartment",
		DESCRIPTION = 'Living Room',
		EXAMINATION = 'The living room is large and well furnished. A big flat screen tv is'
					' mounted on the east wall. On the west wall is a large bookcase.',
		searched_objects = {
			'bookcase': False
		},
		object_desc = {
			'bookcase': 'You find a lot of get-rich-quick books and a few on rare gems.'
		},
		discov = {},
		items = {
			'bookcase': 'strange books'
		},
		
	),
	'c2': dict(
		ZONENAME = "Barry Rhodes' Apartment",
		DESCRIPTION = 'Dining Room',
		EXAMINATION = 'The walls are covered with framed pictures. A large family portrait stands out'
					'\nalong the south wall, near the kitchen area.',
		searched_objects = {
			'family portrait': False
		},
		object_desc = {
			'family portrait': 'You see many pictures with Barry and Liz. Some of them from when they were'
							'\njust children.'
		},
		discov = {},
		items = {},
	),
	'c3': dict(
		ZONENAME = "Barry Rhodes' Apartment",
		DESCRIPTION = 'Bedroom',
		EXAMINATION = 'You see a small, dark room with a large wooden bed and matching armoire.',
		searched_objects = {
			'armoire': False
		},
		object_desc = {
			'armoire': 'Filled with Barry\'s clothes.'
		},
		discov = {},
		items = {},
	),
	'c4': dict(
		ZONENAME = "Barry Rhodes' Apartment",
		DESCRIPTION = 'Office',
		EXAMINATION = 'On the west wall is a large corkboard covered in papers. \nIn the center'
					' of the room is a table with papers and books on it.',
		searched_objects = {
			'corkboard': False, 'table': False
		},
		object_desc = {
			'corkboard': 'You see architectural sketches on papers of various sizes and colors'
						' and little notes written and pinned to the cork.',
			'table': 'On the table you notice some utilities bills with a familiar address. It\'s the'
					'\naddress of a building next door to the jewelry store.'
		},
		discov = {},
		items = {
			'table': 'utilities bills'
		},
	),
	'd1': dict(
		ZONENAME = 'Abandoned Building',
		DESCRIPTION = 'Interior',
		EXAMINATION = 'The inside of this abandoned building is mostly empty. \nYou make your way'
					' toward the back of the building, where you believe the other end of the'
					'\ntunnel may be. \n\nYou find the other end of the tunnel! \nRight next to'
					' the hole is a duffle bag.',
		searched_objects = {
			'duffle bag': False
		},
		object_desc = {
			'duffle bag': 'You open the duffel bag and find the missing jewelry!'
		},
		discov = {
			'duffle bag': 'disc11'
		},
		items = {},
	),
}

def final_clue():
		zone_map['a3']['EXAMINATION'] = "You take another look around the large closet. You notice that the racks\
		\non the north wall are a little uneven."
		zone_map['a3']['searched_objects']['tunnel'] = False
		zone_map['a3']['searched_objects']['racks'] = False
		zone_map['a3']['object_desc']['racks'] = 'You look closer at the racking and find that there is a cover\
		\nbehind it, hiding a large hole in the wall.\
		\n\nWhen you pull the cover off and look through the hole, you find that it is\
		\nreally a tunnel! It\'s heading north to the abandoned\
		\nbuilding next door!'
		zone_map['a3']['object_desc']['tunnel'] = 'The tunnel seems to have caved in on this side.'
		zone_map['a3']['discov'] = {'racks': 'disc10'}
		zone_map['a3']['items'] = {'tunnel': 'hidden tunnel'}


#### Game Interactivity ####
def print_location():
	print('\n' + ('#' * (4 + len(zone_map[myPlayer.location]["ZONENAME"]))))
	print('# ' + zone_map[myPlayer.location]["ZONENAME"].upper() + ' #')
	print('#' * (4 + len(zone_map[myPlayer.location]["ZONENAME"])))
	print('# ' + zone_map[myPlayer.location]["DESCRIPTION"] + ' #')
	print('#' * (4 + len(zone_map[myPlayer.location]["DESCRIPTION"])))


def prompt():
	print("\n" + "================================")
	print("What would you like to do?")
	print("(Type 'help' to see a list of commands)")
	action = input('> ')
	acceptable_actions = ['look', 'move', 'talk', 'quit', 'search', 'show map', 'show notes', 
						'show evidence', 'show suspects', 'add to suspects', 'add to evidence',
						'remove from suspects', 'remove from evidence', 'help']
	while action.lower() not in acceptable_actions:
		print("Unknown action, try again.\n")
		action = input('> ')
	if action.lower() == 'quit':
		sys.exit()
	elif action.lower() == 'move':
		player_move()
	elif action.lower() == 'look':
		player_examine()
	elif action.lower() == 'search':
		player_search()
	elif action.lower() == 'talk':
		player_talk()
	elif action.lower() == 'help':
		main_help_menu()
	elif action.lower() == 'show map':
		show_map()
	elif action.lower() == 'show notes':
		show_notes()
	elif action.lower() == 'show evidence':
		show_evidence()
	elif action.lower() == 'show suspects':
		show_suspects()
	elif action.lower() == 'add to evidence':
		add_evidence()
	elif action.lower() == 'add to suspects':
		add_suspect()
	elif action.lower() == 'remove from suspects':
		remove_suspect()
	elif action.lower() == 'remove from evidence':
		remove_evidence()

def player_move():
	if zone_map[myPlayer.location]["ZONENAME"] == 'Abandoned Building':
		print("Maybe you should talk to Officer Gibbs instead...")
	else:
		os.system('clear')
		ask = "Where would you like to move to?\n> "
		dest = input(ask)
		if dest.lower() not in ['showroom', 'mgr office', 'closet', 'security office']:
			print("Are you sure that is the room? Perhaps check your map.")
	if zone_map[myPlayer.location]["ZONENAME"] == "Jewelry Store":
		if dest.lower() == "showroom":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Showroom':
				print("\nYou're already in that room.")
			else:
				movement_handler('a1')
		elif dest.lower() == "mgr office":
			if zone_map[myPlayer.location]["DESCRIPTION"] == "Manager's Office":
				print("\nYou're already in that room.")
			else:
				movement_handler('a2')
		elif dest.lower() == "closet":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Closet':
				print("\nYou're already in that room.")
			else:
				movement_handler('a3')
		elif dest.lower() == "security office":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Security Office':
				print("\nYou're already in that room.")
			else:
				movement_handler('a4')
	if zone_map[myPlayer.location]["ZONENAME"] == "Tony Jobs' Apartment":
		if dest.lower() not in ['living room', 'dining room', 'bedroom', 'office']:
			print("Are you sure that is the room? Perhaps check your map.")
		if dest.lower() == "living room":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Living Room':
				print("\nYou're already in that room.")
			else:
				movement_handler('b1')
		elif dest.lower() == "dining room":
			if zone_map[myPlayer.location]["DESCRIPTION"] == "Dining Room":
				print("\nYou're already in that room.")
			else:
				movement_handler('b2')
		elif dest.lower() == "bedroom":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Bedroom':
				print("\nYou're already in that room.")
			else:
				movement_handler('b3')
		elif dest.lower() == "office":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Office':
				print("\nYou're already in that room.")
			else:
				movement_handler('b4')
	elif zone_map[myPlayer.location]["ZONENAME"] == "Barry Rhodes' Apartment":
		if dest.lower() not in ['living room', 'dining room', 'bedroom', 'office']:
			print("Are you sure that is the room? Perhaps check your map.")
		if dest.lower() == "living room":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Living Room':
				print("\nYou're already in that room.")
			else:
				movement_handler('c1')
		elif dest.lower() == "dining room":
			if zone_map[myPlayer.location]["DESCRIPTION"] == "Dining Room":
				print("\nYou're already in that room.")
			else:
				movement_handler('c2')
		elif dest.lower() == "bedroom":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Bedroom':
				print("\nYou're already in that room.")
			else:
				movement_handler('c3')
		elif dest.lower() == "office":
			if zone_map[myPlayer.location]["DESCRIPTION"] == 'Office':
				print("\nYou're already in that room.")
			else:
				movement_handler('c4')
		
def movement_handler(destination):
	os.system('clear')
	print("\nYou have moved to ")
	myPlayer.location = destination
	print_location()

def player_examine():
		os.system('clear')
		print(zone_map[myPlayer.location]['EXAMINATION'])

def player_search():
	os.system('clear')
	print('What would you like to search?\n(Type "back" to go back)\n\n')
	player_input = input("> ")
	if player_input.lower() not in zone_map[myPlayer.location]['searched_objects'] \
	and player_input.lower() != 'back':
		os.system('clear')
		print("Unknown action. Look around the room to find objects of interest.")
		prompt()
	if player_input.lower() in zone_map[myPlayer.location]['searched_objects']:
		if player_input.lower() == 'racks' and discoveries['disc9']:
			os.system('clear')
			print(zone_map[myPlayer.location]['object_desc'][player_input.lower()])
			if player_input.lower() in zone_map[myPlayer.location]['discov']:
				discoveries[zone_map[myPlayer.location]['discov'][player_input.lower()]] = True
			if player_input.lower() in zone_map[myPlayer.location]['items']:
				items_found.append(zone_map[myPlayer.location]['items'][player_input.lower()])
		elif zone_map[myPlayer.location]['searched_objects'][player_input.lower()]:
			os.system('clear')
			print("You've already searched that.")
		else:
			os.system('clear')
			print(zone_map[myPlayer.location]['object_desc'][player_input.lower()])
			zone_map[myPlayer.location]['searched_objects'][player_input.lower()] = True
			if player_input.lower() in zone_map[myPlayer.location]['discov']:
				discoveries[zone_map[myPlayer.location]['discov'][player_input.lower()]] = True
			if player_input.lower() in zone_map[myPlayer.location]['items']:
				items_found.append(zone_map[myPlayer.location]['items'][player_input.lower()])
	elif player_input.lower() == 'back':
		os.system('clear')

def player_talk():
	if myPlayer.location == 'a1':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Liz Rhodes")
		print("2- Dave Smith")
		print("3- Officer Gibbs")
		print("4- Cancel")
		choice = input("> ")
		while choice not in ['1', '2', '3', '4']:
			print("Please type '1', '2', '3', or '4'")
			choice = input("> ")
		if choice == '1':
			liz_rhodes_convo()
		elif choice == '2':
			dave_smith_convo()
		elif choice == '3':
			john_gibbs_convo()
		elif choice == '4':
			return
	elif myPlayer.location == 'a2':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Tony Jobs")
		print("2- Cancel")
		choice = input("> ")
		while choice not in ['1', '2']:
			print("Please type '1' or '2'")
			choice = input("> ")
		if choice == '1':
			tony_jobs_convo()
		elif choice == '2':
			return
	elif myPlayer.location == 'a4':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Steve Perry")
		print("2- Cancel")
		choice = input("> ")
		while choice not in ['1', '2']:
			print("Please type '1' or '2'")
			choice = input("> ")
		if choice == '1':
			steve_perry_convo()
		elif choice == '2':
			return
	elif myPlayer.location == 'b1':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Officer")
		print("2- Cancel")
		choice = input("> ")
		while choice not in ['1', '2']:
			print("Please type '1' or '2'")
			choice = input("> ")
		if choice == '1':
			assisting_officer_convo()
		elif choice == '2':
			return
	elif myPlayer.location == 'c1':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Barry Rhodes")
		print("2- Officer")
		print("3- Cancel")
		choice = input("> ")
		while choice not in ['1', '2', '3']:
			print("Please type '1', '2', or '3'")
			choice = input("> ")
		if choice == '1':
			barry_rhodes_convo()
		elif choice == '2':
			assisting_officer_convo()
		elif choice == '3':
			return
	elif myPlayer.location == 'd1':
		os.system('clear')
		print("Who would you like to talk to?")
		print("\n1- Officer Gibbs")
		print("2- Cancel")
		choice = input("> ")
		while choice not in ['1', '2']:
			print("Please type '1' or '2'")
			choice = input("> ")
		if choice == '1':
			john_gibbs_convo()
		elif choice == '2':
			return
	else:
		print("There is no one in this room to talk to.")


def main_help_menu():
	print('\n#########################################')
	print('#          Acceptable Commands          #')
	print('#########################################')
	print('#               - Look -                #')
	print('#               - Move -                #')
	print('#               - Talk -                #')
	print('#              - Search -               #')
	print('#               - Quit -                #')
	print('#    - Show map -    - Show notes -     #')
	print('#       - Show evidence/suspects -      #')
	print('#      - Add to evidence/suspects -     #')
	print('#   - Remove from evidence/suspects -   #')
	print('#########################################')
	prompt()


def show_map():
	if myPlayer.location in ['a1', 'a2', 'a3', 'a4']:
		print('\nJEWELRY STORE')
		print('---------------------------------')
		print('|           |    |               |')
		print('|  Closet   _    _   Security    |')
		print('|           |    |    Office     |')
		print('|-----------|    |---------------|')
		print('|           |                    |')
		print('|    MGR    |                    |')
		print('|    Office |        Showroom    |')
		print('|           _                    |')
		print('|           |                    |')
		print('------------|----------| |-------')
	elif myPlayer.location in ['b1', 'b2', 'b3', 'b4']:
		print("\nTONY JOBS' APARTMENT")
		print('|-------------------------| |-----|')
		print('|               |                 |')
		print('|    Office     |    Living Room  |')
		print('|               |                 |')
		print('|----| |--------|                 |')
		print('|                       ----------|')
		print('|----| |-----|                    |')
		print('|            |       Dining       |')
		print('|   Bedroom  |         Room       |')
		print('|            |                    |')
		print('|---------------------------------|')
	elif myPlayer.location in ['c1', 'c2', 'c3', 'c4']:
		print("\nBARRY RHODES' APARTMENT")
		print('|-------------------------| |-----|')
		print('|               |                 |')
		print('|    Office     |    Living Room  |')
		print('|               |                 |')
		print('|----| |--------|                 |')
		print('|                       ----------|')
		print('|----| |-----|                    |')
		print('|            |       Dining       |')
		print('|   Bedroom  |         Room       |')
		print('|            |                    |')
		print('|---------------------------------|')
	else:
		print("\nABANDONED BUILDING")
		print('|------------------------|')
		print('|                        |')
		print('|                        |')
		print('|   Abandoned Building   |')
		print('|                        _')
		print('|                        |')
		print('|------------------------|')

def show_notes():
	os.system('clear')
	if len(items_found) == 0:
		print("You currently have no notes.")
		print("(To add more, look around each room and search objects)")
	else:
		print('#' * 40)
		print('#' + (' ' * 16) + 'Notes' + (' ' * 17) + '#')
		print('#' * 40)
		print('#' + (' ' * 38) + '#')
		for i in range(len(items_found)):
			if len(items_found[i]) < 10:
				print('#' + (' ' * int((40 - int(len(items_found[i]))) / 2)) + items_found[i].title() + \
					  (' ' * int((38 - int(len(items_found[i]))) / 2)) + '#')
				print('#' + (' ' * 38) + '#')

			elif 10 > len(items_found[i]) > 15:
				print('#' + (' ' * int((38 - int(len(items_found[i]))) / 2)) + items_found[i].title() + \
					  (' ' * int((38 - int(len(items_found[i])) / 2))) + '#')
				print('#' + (' ' * 38) + '#')
			else:
				print('#' + (' ' * math.ceil((38 - int(len(items_found[i]))) / 2)) + items_found[i].title() + \
					(' ' * int((38 - int(len(items_found[i]))) / 2)) + '#')
				print('#' + (' ' * 38) + '#')

		print('#' * 40)

def show_evidence():
	os.system('clear')
	if len(evidence) == 0:
		print("There are no pieces of evidence on your list.")
		print("(To add more, type 'add to evidence' as command)")
	else:
		print('#' * 40)
		print('#' + (' ' * 15) + 'Evidence' + (' ' * 15) + '#')
		print('#' * 40)
		print('#' + (' ' * 38) + '#')
		for i in range(len(evidence)):
			if len(evidence[i]) < 10:
				print('#' + (' ' * int((40 - int(len(evidence[i]))) / 2)) + evidence[i].title() + \
					  (' ' * int((38 - int(len(evidence[i]))) / 2)) + '#')
				print('#' + (' ' * 38) + '#')

			elif 10 > len(evidence[i]) > 15:
				print('#' + (' ' * int((38 - int(len(evidence[i]))) / 2)) + evidence[i].title() + \
					  (' ' * int((38 - int(len(evidence[i])) / 2))) + '#')
				print('#' + (' ' * 38) + '#')
			else:
				print('#' + (' ' * math.ceil((38 - int(len(evidence[i]))) / 2)) + evidence[i].title() + \
					(' ' * int((38 - int(len(evidence[i]))) / 2)) + '#')
				print('#' + (' ' * 38) + '#')

		print('#' * 40)


def show_suspects():
	os.system('clear')
	if len(suspects) == 0:
		print("There are no names on your list of suspects.")
		print("(To add a name, type 'add to suspects' as command)")
	else:
		def condition():
		    if len(suspects) == 1:
		        print('#' + (' ' * 38) + '#')
		        print('#' + (' ' * 38) + '#')
		    else:
		        print('#' + (' ' * 38) + '#')
		print('#' * 40)
		print('#' + (' ' * 13) + 'Suspect List' + (' ' * 13) + '#')
		print('#' * 40)
		condition()
		for i in range(len(suspects)):
		    if len(suspects[i]) > 10:
		        print('#' + (' ' * int((38 - int(len(suspects[i])) - 1) / 2)) + suspects[i].title() + \
		              (' ' * 14) + '#')
		        print('#' + (' ' * 38) + '#')
		    else:
		        print('#' + (' ' * math.ceil((38 - int(len(suspects[i]))) / 2)) + suspects[i].title() + \
		              (' ' * int((38 - int(len(suspects[i]))) / 2)) + '#')
		        print('#' + (' ' * 38) + '#')
		condition()
		print('#' * 40)

def add_evidence():
	os.system('clear')
	show_notes()
	print('\n\nWhat would you like to add to evidence?')
	print('(Note: You must have 3 correct pieces of evidence to arrest a suspect)')
	player_input = input("> ")
	if len(evidence) == 3:
		os.system('clear')
		print("You already have the max pieces of evidence recorded.")
		print("You must delete evidence from the list to submit another.")
	else:
		if player_input.lower() not in items_found:
			os.system('clear')
			print("That is either undiscovered or irrelevant. Try again.")
		elif player_input.lower() in items_found:
			if player_input.lower() in evidence:
				os.system('clear')
				print("That has already been added to your list of evidence.")
			else:
				os.system('clear')
				print("{} has been added to evidence!".format(player_input.title()))
				evidence.append(player_input.lower())

def add_suspect():
	os.system('clear')
	print('#' * 56)
	print('#' + (' ' * 17) + 'Persons of Interest' + (' ' * 18) + '#')
	print('#' * 56)
	print('#' + (' ' * 54) + '#')
	for i in range(len(persons)):
	    if len(persons[i]) > 10:
	        print('#' + (' ' * int((54 - int(len(persons[i])) - 1) / 2)) + persons[i].title() + \
	              (' ' * int((54 - int(len(persons[0]))) / 2)) + '#')
	        print('#' + (' ' * 54) + '#')
	    else:
	        print('#' + (' ' * math.ceil((54 - int(len(persons[i]))) / 2)) + persons[i].title() + \
	              (' ' * int((54 - int(len(persons[0]))) / 2)) + '#')
	        print('#' + (' ' * 54) + '#')
	print('#' * 56)
	print("\n\nWho would you like to add to your list of suspects?")
	print("(type the full name)")
	choice = input("> ")
	if choice.lower() not in persons:
		os.system('clear')
		print("That is not a person of interest.")
		prompt()
	elif choice.lower() in suspects:
		os.system('clear')
		print("{} is already on your list of suspects.".format(choice.title()))
		prompt()
	else:
		os.system('clear')
		print("{} has been added to your list of suspects!".format(choice.title()))
		suspects.append(choice.lower())

def remove_suspect():
	os.system('clear')
	if len(suspects) == 0:
		print("There is currently no name added to your suspect list.")
	else:
		show_suspects()
		print("\n\nWho would you like to remove from your suspect list?")
		player_input = input("> ")
		if player_input.lower() not in suspects:
			os.system('clear')
			print("That name is not on your list. Please try again.")
			print("(Type the full name of your suspect)")
		else:
			os.system('clear')
			print("{} has been removed from your list of suspects!".format(player_input.title()))
			suspects.remove(player_input.lower())

def remove_evidence():
	os.system('clear')
	if len(evidence) == 0:
		print("There are currently no pieces of evidence added to your list.")
	else:
		show_evidence()
		print("\n\nWhat would you like to remove from your evidence list?")
		player_input = input("> ")
		if player_input.lower() not in evidence:
			os.system('clear')
			print("That evidence is not on your list. Please try again.")
		else:
			os.system('clear')
			print("{} has been removed from your list of evidence!".format(player_input.title()))
			evidence.remove(player_input.lower())



#### Conversations ####

def liz_rhodes_convo():
	def branch_1():
		print("\n\n<1> How long has your security officer worked here?")
		print("<2> Why wasn't the security officer here watching the store?")
		print("<3> Got it..")
		resp = input("> ")
		while resp not in ['1', '2', '3']:
				print("Please type '1', '2', or '3'")
				resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Liz Rhodes: "Steve has been here since before I started. I don\'t know, maybe 6')
			print('years or more.')
			branch_1()
		elif resp == '2':
			os.system('clear')
			print('Liz Rhodes: Well he\'s supposed to be here all the time while the store is open,')
			print("but everyday around this time he steps out to the local coffee shop to get some")
			print("coffees for him and I. Mr. Jobs doesn't know about it, but he's always in his")
			print("office the first few hours of the day, so he never notices. It's kind of our")
			print("little secret.")
			branch_1()
		elif resp == '3':
			liz_rhodes_convo()
	os.system('clear')
	print('Liz: "How may I help you, Detective?"')
	print("\n\n<1> Can you tell me what happened, Ms. Rhodes?")
	print("<2> How long have you worked for Mr. Jobs?")
	print("<3> Thank you, Ms. Rhodes. That'll be all for now.")
	if discoveries['disc6']:
		print("<4> Ms. Rhodes, can you tell me about your relationship with Tony?")
	resp = input("> ")
	if discoveries['disc6']:
		while resp not in ['1', '2', '3', '4']:
			print("Please type '1', '2', '3', or '4'")
			resp = input("> ")
	else:
		while resp not in ['1', '2', '3']:
			print("Please type '1', '2', or '3'")
			resp = input("> ")
	if resp == '1':
		os.system('clear')
		print('Liz: "I was helping a customer find an engagement ring when this masked man')
		print('entered, shouting and waving a gun around. He told us all to remain calm')
		print('and nobody would get hurt. He handed me a black bag and told me to put')
		print('all the diamonds inside."')
		print('\n\n<1> What happened after that?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		else:
			os.system('clear')
			print("Liz: \"He then pulled out a bunch of blindfolds and told us all to put")
			print("them on and lay down on the ground or he'd shoot us! So we did. Then")
			print("after about 10 minutes or so our security officer came in and found us.")
			print("He called the police right away.\"")
			branch_1()
	elif resp == "2":
		os.system('clear')
		print('Liz Rhodes: "I\'ve worked here for about 2 years. I love it here, we\'ve never')
		print('had any kind of trouble like this."')
		print('\n\n<1> Ok.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			liz_rhodes_convo()
	elif resp == "3":
		os.system('clear')
		print('Liz Rhodes: "Of course, Detective."')
	elif discoveries['disc6'] == True and resp == '4':
		os.system('clear')
		print('Liz Rhodes: "Relationship? I mean.. he\'s my boss. That\'s all."')
		print('\n\n<1> Ms. Rhodes, he just confirmed you two \"date.\" So what\'s the real story?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Liz Rhodes: "Ok, ok. We have been seeing eachother. I didn\'t say anything')
			print('because it\'s not allowed. If anyone found out about it, we could be in a')
			print('lot of trouble."')
			print('\n\n<1> Who is the third person in this picture?')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Liz Rhodes: "That\'s my brother, Barry. He and Tony were good friends.')
				print('He did some work for Tony on the office last year."')
				print('\n\n<1> I\'d like to speak with him as well. Can you give me his address?')
				resp = input("> ")
				while resp != '1':
					print("Please type '1'")
					resp = input("> ")
				if resp == '1':
					os.system('clear')
					print('Liz Rhodes: "Sure. I\'ll write it down."')
					print("\n\n\nShe hands you the address to Barry Rhodes apartment.")
					discoveries['disc7'] = True
					persons.append('barry rhodes')


def dave_smith_convo():
	os.system('clear')
	print('Dave Smith: "How\'s it going, Detective?"')
	print('\n\n<1> Mr. Smith, can you tell me what happened here today?')
	print('<2> What were you doing here at the jewelry store?')
	print('<3> That\'s good for now. Don\'t go anywhere.')
	resp = input("> ")
	while resp not in ['1', '2', '3']:
		print("Please type '1', '2', or '3'")
		resp = input("> ")
	if resp == '1':
		os.system('clear')
		print('Dave Smith: "Well this man came in with a gun and starting yelling at us to')
		print('give him the diamonds and get on the ground. It was madness. I thought I was')
		print('going to die!"')
		print('\n\n<1> Did you notice anything about the thief that stood out?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Dave Smith: "You mean other than the grey jumper, ski mask, and shiny gun?')
			print('Not really."')
			print('\n\n<1> Okay.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				dave_smith_convo()
	elif resp == '2':
		os.system('clear')
		print('Dave Smith: "I was here looking for an engagement ring for my girlfriend. I')
		print('heard they have the best prices in town."')
		print('\n\n<1> So you decided why not just steal the diamonds instead?')
		print('    Maybe make some money in the process?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Dave Smith: "What? No! I didn\'t steal anything! I\'m a victim here!"')
			print('\n\n<1> Sure')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				dave_smith_convo()
	elif resp == '3':
		os.system('clear')
		print('Dave Smith: "I\'ll be here."')





def john_gibbs_convo():
	if discoveries['disc11']:
		os.system('clear')
		print('Officer Gibbs: "You found the missing jewelry!"')
		print("\n\n<1> Yes I did. And it's time to make an arrest.")
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if len(suspects) == 0:
			suspects.append('barry rhodes')
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: ""Okay, Detective {}, who do we arrest?'.format(myPlayer.name))
			resp = input("Press enter...")
			while resp != '':
				resp = input("Press enter...")
			if resp == '':
				show_suspects()
				print('\n\nChoose one:')
				choice = input("> ")
				while choice.lower() not in suspects:
					print("\nPlease type the full name as it appears")
					choice = input("> ")
				if choice.lower() in suspects:
					if choice.lower() == 'barry rhodes':
						myPlayer.game_over = True
						game_win()
					else:
						game_loss()
	def final_move():
		answer = ['contracted work', 'hidden tunnel', 'utilities bills']
		os.system('clear')
		print('Officer Gibbs: "Really? Well there\'s no way he is going to just')
		print('let you search his building. You\'ll need to get a warrant first.')
		print('Get me 3 pieces of hard evidence and I can get you a warrant.')
		print('\n\n<1> I have the 3 pieces of evidence now.')
		print('<2> On second thought...')
		resp = input("> ")
		while resp not in ['1', '2']:
			print("Please type '1' or '2'")
			resp = input("> ")
		if resp == '1' and len(evidence) < 3:
			os.system('clear')
			print('Officer Gibbs: "You don\'t have 3 pieces of evidence."')
			print("To add more, type 'add to evidence' as command")
		elif resp == '1' and len(evidence) == 3:
			os.system('clear')
			print('Officer Gibbs: "So, what should I give to the judge?"')
			resp = input("Press enter...")
			while resp != '':
				resp = input("Press enter...")
			else:
				show_evidence()
				print("\n\nSubmit these as evidence? (Yes or No)")
				choice = input("> ")
				while choice.lower() not in ['yes', 'no']:
					print("\n\nSubmit these as evidence? (Yes or No)")
					choice = input("> ")
				if choice.lower() == 'yes':
					sorted_evidence = sorted(evidence)
					if sorted_evidence == answer:
						os.system('clear')
						print('Officer Gibbs: "That is perfect! The judge will definitely sign a warrant')
						print('for this! Come with me."')
						print("\n\n<1> Let's go.")
						resp = input("> ")
						while resp != '1':
							print("Please type '1'")
							resp = input("> ")
						if resp == '1':
							movement_handler('d1')
					else:
						os.system('clear')
						print('Officer Gibbs: "I really don\'t think the judge will sign a warrant on that \nevidence."')
		else:
			pass

	if discoveries['disc1'] == False:
		os.system('clear')
		print('Officer Gibbs: "Detective {}, it\'s nice to see you."'.format(myPlayer.name))
		print('\n\n<1> What can you tell me?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: "Nothing you haven\'t already been briefed on, Detective,')
			print("but I am waiting on word back from the city about some possible video")
			print('footage from the street cameras. I\'ll let you know when I hear anything."')
	elif discoveries['disc1'] == True and discoveries['disc2'] == False:
		os.system('clear')
		print('Officer Gibbs: "Detective, I got word back from the city about those"')
		print('street cameras.')
		print('\n\n<1> Please tell me we found something.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: "Well, it\'s kinda odd. The camera across the street shows the') 
			print("suspect entering the store at 10:30am. But then no one comes out. The next")
			print('person to go through that door is the security officer at 10:55am."')
			print('\n\n<1> That is odd...')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Officer Gibbs: "Do you think the suspect is someone here in this building?"')
				discoveries['disc2'] = True
				print("\n\nThe idea troubles you. Better go collect some more information.")
	elif discoveries['disc7']:
		os.system('clear')
		print('Officer Gibbs: "How\'s the case coming, Detective?"')
		print('\n\n<1> I need to go visit the home of Tony Jobs.')
		print('<2> I need to go visit the home of Barry Rhodes.')
		print('<3> I have some more looking around to do.')
		if discoveries['disc10']:
			print('<4> Barry Rhodes owns an abandonded building next door. I need access.')
		resp = input("> ")
		if discoveries['disc10']:
			while resp not in ['1', '2', '3', '4']:
				print("Please type '1', '2', '3' or '4'")
				resp = input("> ")
		else:
			while resp not in ['1', '2', '3']:
				print("Please type '1', '2', or '3'")
				resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: "I can have an officer escort you over there."')
			print('Are you ready to go now?')
			print('\n\n<1> I\'m ready.')
			print('<2> On second thought...')
			resp = input("> ")
			while resp not in ['1', '2']:
				print("Please type '1' or '2'")
				resp = input("> ")
			if resp == '1':
				movement_handler('b1')
			else:
				os.system('clear')
				print('Officer Gibbs: "Sounds good, Detective."')
		elif resp == '2':
			os.system('clear')
			print('Officer Gibbs: "I can have an officer escort you over there.')
			print('Are you ready to go now?"')
			print('\n\n<1> I\'m ready.')
			print('<2> On second thought...')
			resp = input("> ")
			while resp not in ['1', '2']:
				print("Please type '1' or '2'")
				resp = input("> ")
			if resp == '1' and discoveries['bRhodes'] == False:
				movement_handler('c1')
				barry_rhodes_setup()
			elif resp == '1' and discoveries['bRhodes']:
				movement_handler('c1')
			else:
				os.system('clear')
				print('Officer Gibbs: "Sounds good, Detective."')
		elif resp == '3':
			os.system('clear')
			print('Officer Gibbs: "Sounds good, Detective."')
		elif resp == '4' and discoveries['disc10']:
			final_move()
	elif discoveries['disc1'] and discoveries['disc2'] and discoveries['disc4']:
		os.system('clear')
		print('Officer Gibbs: "How\'s the case coming, Detective?"')
		print('\n\n<1> I think I\'m getting closer. I need to go visit the home of Tony Jobs.')
		print('<2> I have some more looking around to do.')
		resp = input("> ")
		while resp not in ['1', '2']:
			print("Please type '1' or '2'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: "I can have an officer escort you over there."')
			print('Are you ready to go now?')
			print('\n\n<1> I\'m ready.')
			print('<2> On second thought...')
			resp = input("> ")
			while resp not in ['1', '2']:
				print("Please type '1' or '2'")
				resp = input("> ")
			if resp == '1':
				movement_handler('b1')
			else:
				os.system('clear')
				print('Officer Gibbs: "Sounds good, Detective."')
		else:
			os.system('clear')
			print('Officer Gibbs: "Sounds good, Detective."')
	elif discoveries['disc1'] and discoveries['disc2']:
		os.system('clear')
		print('Officer Gibbs: "Detective {}, it\'s nice to see you."'.format(myPlayer.name))
		print('\n\n<1> What can you tell me?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Officer Gibbs: Nothing you haven\'t already been briefed on, Detective."')


def steve_perry_convo():
	def branch_1():
		print('\n\n<1> I find it hard to believe that it\'s just a coincidence.')
		print('<2> Isn\'t it your job to watch this place while it is open?')
		print('<3> I see...')
		resp = input(">")
		while resp not in ['1', '2', '3']:
			print("Please type '1', '2' or '3'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Steve Perry: "It is! Honest! Or maybe-- maybe the guy knew I\'d leave and took')
			print('the opportunity. I promise, I had nothing to do with this!"')
			branch_1()
		elif resp == '2':
			os.system('clear')
			print('Steve Perry: "It is. I didn\'t think it would be a problem. Nothing ever happens')
			print('here. And, it\'s not like I was gone a long time. I just wanted some caffeine to')
			print('stay awake!"')
			branch_1()
		elif resp == '3':
			steve_perry_convo()
	os.system('clear')
	print('Steve Perry: "Uhh... Hey, Detective. Something I can do for you?"')
	print('\n\n<1> You wanna tell me why you weren\'t here while the store was being robbed?')
	print('<2> What can you tell me about Tony Jobs?')
	print('<3> Dave Smith, have you seen him in here before?')
	print('<4> Can you show me the footage from the showroom cameras?')
	print('<5> I\'ll come back to you. Gotta check something out, first.')
	resp = input("> ")
	while resp not in ['1', '2', '3', '4', '5']:
		print("Please type '1', '2', '3', '4', or '5'")
		resp = input("> ")
	if resp == '1':
		os.system('clear')
		print('Steve Perry: "I stepped out for a few minutes. I went to get coffee from down')
		print(' the street. I had no idea something like this was going to happen, I swear."')
		branch_1()
	elif resp == '2':
		os.system('clear')
		print('Steve Perry: "Tony? Well, he\'s an alright guy, I guess. Started managing the')
		print('place right around the time I started working here. Guess it\'s been about 6')
		print('years now."')
		print('\n\n<1> Do you think he\'s responsible for the robbery?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input ("> ")
		if resp == '1':
			os.system('clear')
			print('Steve Jobs: "No, I don\'t think so. He loves working here. He makes good money.')
			print('Can\'t see why he\'d want to ruin that."')
			print('\n\n<1> Hmm.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				steve_perry_convo()
	elif resp == '3':
		os.system('clear')
		print('Steve Perry: "The customer in the showroom? Not that I can recall."')
		print('\n\n<1> Is there another security officer you work with?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Steve Perry: "It\'s just me. I work 7 days a week. We aren\'t open for more than 6')
			print('hours a day, so it really isn\'t that bad."')
			print('\n\n<1> Why wouldn\'t the thief just steal the jewelry when you\'re not open, then?')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Steve Perry: "Probably because this place is like Fort Knox when we are closed.')
				print('State-of-the-art security system, with lasers and sensors. Seems like the')
				print('daytime would be the perfect time to pull off something like this."')
				print('\n\n<1> You don\'t say.')
				resp = input("> ")
				while resp != '1':
					print("Please type '1'")
					resp = input("> ")
				if resp == '1':
					steve_perry_convo()
	elif resp == '4':
		if discoveries['disc1']:
			os.system('clear')
			print('Steve Perry: "I already told you I can\'t."')
			print('\n\n<1> Right.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				steve_perry_convo()
		else:
			os.system('clear')
			print('Steve Perry: "No, I can\'t. Looks like the thief came in and swiped the tapes.')
			print(' Wiped the backups on the computer, too. Even my emails have been deleted."')
			print('\n\n<1> Isn\'t that stuff password protected? The thief would have to have access to that information.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Steve Perry: "It is. Someone obviously knew what they were doing."')
				discoveries['disc1'] = True
				print('\n\n<1> Right.')
				resp = input("> ")
				while resp != '1':
					print("Please type '1'")
					resp = input("> ")
				if resp == '1':
					steve_perry_convo()
	elif resp == '5':
		os.system('clear')
		print('Steve Perry: "Yes, sir. Of course."')

def tony_jobs_convo():
	if discoveries['disc5']:
		os.system('clear')
		print('Tony Jobs: "Find anything useful at my place, Detective?"')
		print('\n\n<1> As a matter of fact I did. What is your relationship with Liz Rhodes?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Tony Jobs: "She and I have been... dating, I guess. What does that have to')
			print('do with the case?"')
			print('\n\n<1> I\'m not sure yet. Maybe I\'ll go have a chat with her about it.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Tony Jobs: "Whatever you say, Detective."')
				discoveries['disc6'] = True
	else:
		os.system('clear')
		print('Tony Jobs: "You must be the Detective. Good."')
		print('\n\n<1> It seems you\'ve got yourself a bit of a problem, here, Mr. Jobs.')
		print('<2> Tell me what happened.')
		print('<3> Do you have any idea who might have done this? Seen anybody lurking around?')
		print('<4> We\'ll talk later.')
		if discoveries['disc3']:
			print('<5> I found a spreadsheet with your finances on it. Seems like you had a motive.')
		resp = input("> ")
		if discoveries['disc3']:
			while resp not in ['1', '2', '3', '4', '5']:
				print("Please type '1', '2', '3', '4', or '5'")
				resp = input("> ")
		else:
			while resp not in ['1', '2', '3', '4']:
				print("Please type '1', '2', '3', or '4'")
				resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Tony Jobs: "Tell me about it. Thank God for insurance."')
			print('\n\n<1> Seems kind of convenient. Perhaps this was all intentional?')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Tony Jobs: "What are you saying? You think that I had something to do with')
				print('this? I love this place. I would never risk that."')
				print('\n\n<1> Okay, relax.')
				resp = input("> ")
				while resp != '1':
					print("Please type '1'")
					resp = input("> ")
				if resp == '1':
					tony_jobs_convo()
		elif resp == '2':
			os.system('clear')
			print('Tony Jobs: "I was reading some emails when I heard some yelling in the showroom.')
			print('When I went to check it out, I had a gun pointed to my head and was forced to')
			print('put on a blindfold."')
			print('\n\n<1> Ok..')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				tony_jobs_convo()
		elif resp == '3':
			os.system('clear')
			print('Tony Jobs: "I can\'t think of anyone. Maybe security can help you with that."')
			print('\n\n<1> I\'ll talk to him.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				tony_jobs_convo()
		elif resp == '4':
			os.system('clear')
			print('Tony Jobs: "Looking forward to it."')
		elif discoveries['disc3'] == True and resp == '5':
			os.system('clear')
			print('Tony Jobs: "Alright, I\'ll admit, things have been rough for me. I have a bit of')
			print('a problem walking away from the table. I had a few bad runs and lost a lot of')
			print('money gambling. But that still wouldn\'t make me pull off something stupid')
			print('like this."')
			print('\n\n<1> But not only do you have motive, you have access. Passwords, keys...')
			print('    You even know when your security officer leaves everyday for coffee.')
			print('    It\'s starting to look more and more like you played a role here.')
			print('    I\'m going to need to search your home.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Tony Jobs: "Of course, Detective. Anything to clear my name."')
				discoveries['disc4'] = True

def assisting_officer_convo():
	os.system('clear')
	print('Officer: "Need anything, Detective?"')
	print('\n\n<1> I need to go back to the jewelry store.')
	print('<2> Not right now, thanks.')
	resp = input("> ")
	while resp not in ['1', '2']:
		print("Please type '1' or '2'")
		resp = input("> ")
	if resp == '1':
		os.system('clear')
		print('Officer: "Ok, I can escort you back. Are you ready to go?"')
		print('\n\n<1> Ready.')
		print('<2> Not yet.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			movement_handler('a1')
	elif resp == '2':
		os.system('clear')
		print('Officer: "Yes, sir."')


def barry_rhodes_setup():
	os.system('clear')
	print("You knock on the door and a man answers.")
	print('\nBarry Rhodes: "Hello? How may I help you?"')
	print('\n\n<1> Mr. Rhodes, my name is Detective {}. I am investigating'.format(myPlayer.name))
	print('    a robbery at Polished Jewelry Store on West 5th street.')
	print('    Mind if I ask you a few questions?')
	resp = input("> ")
	while resp != '1':
		print("Please type '1'")
		resp = input("> ")
	if resp == '1':
		os.system('clear')
		print('Barry Rhodes: "Sure, come on in."')
		print("\nYou enter the home with the assisting officer.")
		print('\n\n<1> Thanks.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input("> ")
		if resp == '1':
			os.system('clear')
			print('Barry Rhodes: "How can I help?"')
			print('\n\n<1> Mr. Rhodes, have you ever been to that jewelry store before?')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input("> ")
			if resp == '1':
				os.system('clear')
				print('Barry Rhodes: "Yeah, many times. My sister works there. I helped her get the job')
				print('a few years back. My good friend, Tony, runs the place."')
				print('\n\n<1> I see.')
				resp = input("> ")
				while resp != '1':
					print("Please type '1'")
					resp = input("> ")
				if resp == '1':
					discoveries['bRhodes'] = True
					barry_rhodes_convo()
				
def barry_rhodes_convo():
	def branch1():
		print('\n\n<1> I saw an old photo of you three. Looks like you used to be pretty close.')
		print('<2> Liz mentioned you did some work for Tony. Mind elaborating?')
		print('<3> Were you aware of your sister\'s relationship with Mr. Jobs?')
		print('<4> This is a nice place, you mind if I take a look around?')
	os.system('clear')
	print('Barry Rhodes: "Need something, Detective?"')
	branch1()
	if 'utilities bills' in items_found:
		print('<5> I saw some mail in your office with an address near the store. Looked like')
		print('    a utility bill. Wanna tell me what that is?')
	resp = input("> ")
	if 'utilities bills' not in items_found:
		while resp not in ['1', '2', '3', '4']:
			print("Please type '1', '2', '3', or '4'")
			resp = input("> ")
	else:
		while resp not in ['1', '2', '3', '4', '5']:
			print("Please type '1', '2', '3', '4', or '5")
			resp = input("> ") 
	if resp == '1':
		os.system('clear')
		print('Barry Rhodes: "Yeah, Tony and I used to be inseperable. But you know how')
		print('things go, you get busy and you stop hanging out as much. Haven\'t really')
		print('talked to him much lately."')
		print('\n\n<1> I see.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input()
		if resp == '1':
			barry_rhodes_convo()
	elif resp == '2':
		os.system('clear')
		print('Barry Rhodes: "Sure. Uh.. yeah. I helped with a few little projects around')
		print('the shop. I\'m a contractor so I\'m pretty handy and I wanted to help Tony')
		print('out a little."')
		print('\n\n<1> Were you paid for this work?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input()
		if resp == '1':
			os.system('clear')
			print('Barry Rhodes: "Not really, I did it as a favor. He didn\'t have a big budget but')
			print('he wanted to impress the owners and try to drive business a bit so I helped him')
			print('out as best I could. He bought me a few beers for it."')
			print('\n\n<1> I see...')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input()
			if resp == '1':
				discoveries['disc8'] = True
				barry_rhodes_convo()
				items_found.append('contracted work')
	elif resp == '3':
		os.system('clear')
		print('Barry Rhodes: "Relationship? I don\'t know, really. I knew they were kinda close,')
		print('but beyond that I had no idea anything was going on."')
		print('\n\n<1> You don\'t talk with your sister much, either?')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input()
		if resp == '1':
			os.system('clear')
			print('Barry Rhodes: "Not lately, no. Both been busy I guess."')
			print('\n\n<1> Sure.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input()
			if resp == '1':
				barry_rhodes_convo()
	elif resp == '4':
		os.system('clear')
		print('Barry Rhodes: "You want to look around my place? I don\'t see why..."')
		print('\n\n<1> I will only be a minute. I insist.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input()
		if resp == '1':
			os.system('clear')
			print('Barry Rhodes: "Fine. Go ahead, I have nothing to hide."')
	elif 'utilities bills' in items_found and resp == '5':
		os.system('clear')
		print('Barry Rhodes: "Yeah, it is. I bought a small building downtown to set up some')
		print('offices for my new company."')
		print('\n\n<1> And it just so happens to be directly next to the jewelry store.')
		resp = input("> ")
		while resp != '1':
			print("Please type '1'")
			resp = input()
		if resp == '1':
			os.system('clear')
			print('Barry Rhodes: "I assure you, that\'s a coincidence. It was just too good a deal')
			print('to pass up."')
			print('\n\n<1> Hmm... Ok, Mr. Rhodes. You sit tight. Don\'t go too far.')
			print('    I may be needing to see you again.')
			resp = input("> ")
			while resp != '1':
				print("Please type '1'")
				resp = input()
			if resp == '1':
				os.system('clear')
				print('Barry Rhodes: "Fine."')
				discoveries['disc9'] = True
				final_clue()






#### Game Functionality ####
def game_loss():
	os.system('clear')
	print("\n\n")
	print('   ____________      ___   _____________     ______ __    _________________')
	print('  /  ______/   \\    /   \\ /   /   _____/    /  ___ \\  |  /  /   _____/ __  \\')
	print(' /  /  __ /  /\\ \\  /  /\\ _/  /   __/       /  /  / /  | /  /   __/  / /_/  /')
	print('/  /__/  /  ____ \\/  /   /  /   / ___     /  / _/ /|  |/  /   / ___/  _  _/')
	print('\\_______/ _/   \\_/__/   / _/ _______/     \\______/ | ____/ _______/ _/ \\ _\\')
	print("\n\n\nYou have arrested the wrong person! Please play again!")
	resp = input("Press Enter...")
	while resp != '':
		resp = input("Press Enter...")
	if resp == '':
		os.system('clear')
		sys.exit()

def game_win():
	os.system('clear')
	print('#' * 80)
	print('#' + (' ' * 32) + 'Case 1: Solved' + (' ' * 32) + '#')
	print('#' * 80)
	print('\n' + (' ' * 27) + 'Congratulations, Detecive.')
	print('\n' + (' ' * 25) + 'You\'ve solved your first case.')
	print('\n\n' + (' ' * 21) + 'Stay tuned for another case coming soon!')
	print('\n\n\n\n\n')
	resp = input("Press Enter...")
	while resp != '':
		resp = input("Press Enter...")
	if resp == '':
		os.system('clear')
		sys.exit()

def main_game_loop():
	while myPlayer.game_over is False:
		prompt()
	if myPlayer.game_over:
		game_win()
		

def setup_game():
	os.system('clear')

	### Name Collection ###
	question1 = "Hello, Detective. What is your last name?\n"
	for character in question1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	player_name = input('> ')
	while player_name == '':
		print("\nSorry, I didn't catch that. What is your last name?")
		player_name = input('> ')
	else:
		myPlayer.name = player_name.title()


	### Introduction ###
	question2 = "Thank you, Detective " + player_name + ".\n"
	for character in question2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	


	speech1 = "Welcome to your first case, Detective.\n"
	speech2 = "You must do your best to discover all the clues in order to solve it.\n"
	speech3 = "A wrongful accusation could result in a wrongful imprisonment.\n"
	speech4 = "And the real perpetrator could go free...\n"

	for character in speech1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	for character in speech4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.1)

	
	print("\n\n#################################")
	print("# Your first case starts now... #")
	print("#################################")
	clickStart = input("\nPress Enter to Begin...")
	while clickStart not in ['']:
		clickStart = input("Press Enter to Begin...")
	else:
		os.system('clear')


	speech1 = "-November 13th, 2018: 11:43am-\n"
	speech2 = "\nYou arrive on scene at Polished Jewelry Store on West 5th St.\n"
	speech3 = "Officer John Gibbs is first to arrive.\n"
	speech4 = "Officer Gibbs gives you the following account:\n"
	for character in speech1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)

	print("\n\nSuspect wearing a jumper and a ski mask enters the jewelry store at 10:30am."
		"\nAccording to witnesses, the suspect is armed with a pistol, and orders"
		"\nemployee Liz Rhodes to fill his bag with all the diamonds in the showcase."
		"\nEveryone in the building is then blindfolded and forced to lay down in the"
		"\nshowroom while the suspect escaped.")
	clickStart = input("\n\nPress Enter...")
	while clickStart not in ['']:
		clickStart = input("Press Enter...")
	else:
		os.system('clear')

	speech1 = "The witnesses in the building are as follows:\n"
	speech2 = "Liz Rhodes: employee\n"
	speech3 = "Tony Jobs: manager\n"
	speech4 = "Dave Smith: customer\n"
	speech5 = "\n\nThe security officer, Steve Perry, was out of the building at the time\n"
	speech6 = "getting coffee. He returned at 10:55am to discover the crime scene.\n"
	for character in speech1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech5:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech6:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	clickStart = input("\n\nPress Enter...")
	while clickStart not in ['']:
		clickStart = input("Press Enter...")
	else:
		os.system('clear')
	print("You are now standing in the Jewelry Store showroom.\n")

	main_game_loop()


title_screen()




