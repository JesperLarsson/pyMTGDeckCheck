#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
By: Jesper Larsson (https://github.com/JesperLarsson), Linköping Sweden 2017
Feel free to use the code for anything, licensed under GPL.

Simple script for verifying deck legality and checking for when cards will rotate out of standard
- Supports all other MTG formats like modern and commander as well (but doesn't check rotation for eternal formats)
- Automatically checks if there is a reprint in a newer set for a card
"""

# MTG format to validate against
validationFormat = "Standard"

# magicthegathering.io API, auto install using "pip install mtgsdk" when in path C:\Python3\Scripts, requires python 3
# docs: https://github.com/MagicTheGathering/mtg-sdk-python
from mtgsdk import *

# http calls to whatsinstandard.com API (V4)
# no docs available
whatsinstandardAPIUrl = r"http://whatsinstandard.com/api/4/sets.json"

import re
import json
import sys
import urllib.request
from pprint import pprint

if (len(sys.argv) != 2):
	print("Please give your deck file as an input argument to this script")
	sys.exit(1)

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
	if m.groups(1):
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
			# They all have a duplicate card with the correct set code anyway which we identify on the next loop
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

	# debug dump everything
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

		if (exit_date in cardRotations):
			cardRotations[exit_date].append(cardMatchObj.name)
		else:
			cardRotations[exit_date] = [cardMatchObj.name]
		
#
# Print rotation results
#
if (cardRotations != {}):
	print("") #NL
	for rotation_date in cardRotations:
		cardList = cardRotations[rotation_date]
		print("These cards rotate on " + rotation_date + ":")
		for rotateCard in cardList:
			print("\t" + rotateCard)
			
