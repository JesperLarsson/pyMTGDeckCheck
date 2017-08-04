#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
By: Jesper Larsson (https://github.com/JesperLarsson), Linköping, Sweden 2017
Feel free to use the code for anything as licensed under GPL

Check out the README file for instructions!
"""

try:
	# MTG format to validate against
	validationFormat = "Standard"
	cardCountMin = 60 # Set too 100 for commander

	# Validate python version
	import sys
	if sys.version_info[0] < 3:
		print("You are running an old version of python (likely v2.X) which is not compatible with the magicthegathering.io libraries. Please install the latest version of python 3 instead")
		raw_input("Press enter to exit") # We use raw_input instead here, normal input is dangerous to use in python 2
		sys.exit(1)

	# magicthegathering.io API,
	#   docs: https://github.com/MagicTheGathering/mtg-sdk-python
	try:
		from mtgsdk import *
	except ImportError:
		try:
			# Try to install it via package manager
			print("Unable to find magicthegathering.io, it will be installed automatically")
			import pip
			pip.main(['install', "mtgsdk"])
			from mtgsdk import *
		except ImportError:
			#  install using "pip install mtgsdk" when in path C:\Python3\Scripts
			print("Unable to find the magicthegathering.io SDK and automatic installation failed, please install them manually by running 'pip install mtgsdk' in your python scripts folder")
			input("Press enter to exit")
			sys.exit(2)

	# http calls to whatsinstandard.com API (V4)
	#   no docs available
	whatsinstandardAPIUrl = r"http://whatsinstandard.com/api/4/sets.json"

	import re
	import json
	import urllib.request
	from pprint import pprint

	if (len(sys.argv) != 2):
		print("No deck file was found, please give it as an argument to this script via commandline. You can also drag-and-drop the file on Windows")
		input("Press enter to exit")
		sys.exit(3)

	inputFilename = sys.argv[1]
	deckIsValid = True # Entire deck is valid or not

	# calls whatsinstandard.com API to get all set rotation info
	jsonSetRotations = json.loads(urllib.request.urlopen(whatsinstandardAPIUrl).read())
	def findRoationInfo(setCodes):
		# match setcode OR name, whatsinstandard and magicthegathering.io use different set codes sometimes
		for setInfo in reversed(jsonSetRotations):
			for compareSetCode in setCodes:
				if setInfo["code"] == compareSetCode:
					return setInfo

		print("  SANITY CHECK FAILED: Unable to find set " + setCodes)
		return None

	#
	# read card list from file
	#
	fo = open(inputFilename, "r")
	cardlist = fo.readlines()
	fo.close()

	cards = []
	totalCardCount = 0
	for lineIter in cardlist:
		if len(lineIter.strip()) == 0 or "Sideboard:" in lineIter or "Mainboard:" in lineIter:
			continue # skip whitespace and headers

		m = re.match(r"(\d+)? ?(.+)", lineIter)
		if (not m):
			print("ERROR, could not parse line: " + lineIter)
			continue
		# count prefix is optional, just in case it's a manual list
		cardCount = 1
		if m.groups()[0]:
			cardCount = int(m.groups()[0].strip())
		cardName = m.groups()[1].strip()

		totalCardCount += cardCount

		# Skip basic lands, they never rotate and we can have any amount of them
		if (cardName == "Wastes" or cardName == "Island" or 
			cardName == "Plains" or cardName == "Mountain" or 
			cardName == "Swamp" or cardName == "Forest"):
			continue

		# check card count
		if (cardCount > 4):
			print("Too many copies of '" + cardName + "' (" + str(cardCount) + "), only 4 copies are allowed")
			deckIsValid = False

		# Save card name
		if (not cardName in cards): # no duplicates
			cards.append(cardName)
	print("=== " + str(totalCardCount) + " CARDS TOTAL IMPORTED ===")

	if (totalCardCount < cardCountMin):
		print("Too few cards in total (" + str(totalCardCount) + ")")
		deckIsValid = False

	#
	# look up cards on magicthegathering.io
	#
	cardRotations = {}
	for card in cards:
		query = Card.where(name="\"" + card + "\"").all() # quotes required for exact string match

		# we may get multiple hits on each name from different sets
		isLegal = False
		formatFound = False # sanity check
		cardMatchObj = None # save a valid card object for later
		for cardIter in query:
			if (cardIter.rarity == "Special"):
				# Masterpiece series, skip them, we cant look them up on whatsinstandard.com as it doesn't support their unique set codes
				#   They all have a duplicate card with the correct set code anyway which we identify on the next loop
				continue
			cardMatchObj = cardIter # Save for later

			if (cardIter.name.lower() != card.lower()):
				print("  SANITY CHECK FAILED: Card name missmatch for " + card)
				continue

			# check card legality, legalities is a tuple of dictionaries
			for legalDict in cardIter.legalities:
				if (legalDict["format"] == validationFormat):
					formatFound = True
					if (legalDict["legality"] == "Legal"):
						isLegal = True
					break

		if (not cardMatchObj):
			print("ERROR:" + str(card) + " could not be found")
			deckIsValid = False
			continue

		# print results
		print(cardMatchObj.name)
		if (not formatFound):
			# No format definition found, meaning it's not legal
			deckIsValid = False
			isLegal = False
			#print(str(cardMatchObj.legalities)) # debug info
		if (not isLegal):
			deckIsValid = False
			print("  " + " Not " + validationFormat + " legal!");

		# dump all fields of a card for debugging
		#if (cardMatchObj.name == "Dispel"):
		#	print(str(cardMatchObj.__dict__))

		# check card rotation if card is legal and we're checking against standard
		if (isLegal and validationFormat == "Standard"):
			rotationInfo = findRoationInfo(cardMatchObj.printings)
			if (not rotationInfo):
				continue # skip

			exit_date = rotationInfo["exit_date"] # announced rotation date
			if (not exit_date):
				exit_date = rotationInfo["rough_exit_date"] # use rotation estimate instead

			exit_date = exit_date.replace("T00:00:00.000Z", "") # remove unnecessary timestamp and timezone
			if (exit_date in cardRotations):
				cardRotations[exit_date].append(cardMatchObj.name)
			else:
				cardRotations[exit_date] = [cardMatchObj.name]
			
	#
	# Print rotation results
	#
	print("") #NL
	for rotation_date in cardRotations.keys():
		cardList = cardRotations[rotation_date]

		print("These cards rotate " + rotation_date + ":")
		for rotateCard in cardList:
			print("  " + rotateCard)

	#
	# Deck validity
	#
	if (deckIsValid):
		print("Your deck seems to be valid")
	else:
		print("Your deck is not valid")
				
	print("")
	input("Press enter to exit")
	sys.exit(0)
except KeyboardInterrupt:
	# Execution aborted by user with Ctrl+C
	sys.exit(4)
except Exception as ex:
	print("") #NL
	print("An error has occurred. Details:")
	print(ex)
	raise ex

	input("Press enter to exit")
	sys.exit(5)
