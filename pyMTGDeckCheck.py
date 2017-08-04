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

	# Validate python version
	import sys
	if sys.version_info[0] == 2:
		print("You are running python 2 which is not compatible with magicthegathering.io libraries. Please install the latest version of python 3 instead")
		raw_input("Press enter to exit") # We use raw_input instead here, normal input is dangerous to use in python 2
		sys.exit(1)

	# magicthegathering.io API, auto install using "pip install mtgsdk" when in path C:\Python3\Scripts, requires python 3
	#   docs: https://github.com/MagicTheGathering/mtg-sdk-python
	try:
		from mtgsdk import *
	except ImportError:
		print("You have not installed the magicthegathering.io library, see README file for installation instructions")
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

	# calls whatsinstandard.com API to get all set rotation info
	jsonSetRotations = json.loads(urllib.request.urlopen(whatsinstandardAPIUrl).read())
	def findRoationInfo(setCodes):
		# match setcode OR name, whatsinstandard and magicthegathering.io use different set codes sometimes
		for setInfo in reversed(jsonSetRotations):
			for compareSetCode in setCodes:
				if setInfo["code"] == compareSetCode:
					return setInfo

		print("\tSANITY CHECK FAILED: Unable to find set " + setCodes)
		return None

	#
	# read card list from file
	#
	fo = open(inputFilename, "r")
	cardlist = fo.readlines()
	fo.close()

	cards = []
	totalCardCount = 0
	for cardIter in cardlist:
		if len(cardIter.strip()) == 0 or "Sideboard:" in cardIter or "Mainboard:" in cardIter:
			continue # skip whitespace and headers

		m = re.match(r"(\d+?) ?(.+)", cardIter)
		if (not m):
			print("ERROR, could not parse line: " + cardIter)
			continue
		# count prefix is optional, just in case it's a manual list
		cardCount = 1
		if m.groups()[0]:
			cardCount = int(m.groups()[0].strip())
		cardName = m.groups()[1].strip()

		if (not cardName in cards): # no duplicates
			cards.append(cardName)
		totalCardCount += cardCount
	print("=== " + str(totalCardCount) + " CARDS TOTAL IMPORTED ===")

	#
	# look up cards on magicthegathering.io
	#
	cardRotations = {}
	for card in cards:
		# Skip basic lands, they never rotate
		if (card == "Wastes" or card == "Island" or card == "Plains" or card == "Mountain" or card == "Swamp" or card == "Forest"):
			continue

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

			if (cardIter.name != card):
				print("\tSANITY CHECK FAILED: Card name missmatch for " + card)
				continue

			# check card legality, legalities is a tuple of dictionaries
			for legalDict in cardIter.legalities:
				if (legalDict["format"] == validationFormat):
					formatFound = True
					if (legalDict["legality"] == "Legal"):
						isLegal = True
					break

		# print results
		print(cardMatchObj.name)
		if (not formatFound):
			print("\tSANITY CHECK FAILED: Could not find format legality definition for card " + card + " for " + validationFormat)
			print(str(cardMatchObj.legalities))
		if (not isLegal):
			print("\t" + " Not " + validationFormat + " legal!");

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
			print("\t" + rotateCard)
				
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

	input("Press enter to exit")
	sys.exit(5)
