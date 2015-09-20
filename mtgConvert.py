# Convert Magic Workstation (from mtgtop8.com) to Cockatrice xml
# Written by Bob Hennessey - 2015
#
# Very specific to the export from mtgtop8 for the several decks I used to test. I hope that they don't export in other ways...
#
# Usage - Requires Python
# ---------- python mtgConvert.py path-to-mtgtop8-file output-path.cod

import sys

def main():
	
	# Grab file paths from argument list
	INPUTPATH = sys.argv[1]
	OUTPUTPATH = sys.argv[2]

	# define the deck instance
	deck = Deck()

	# Read input file
	inputFile = open(INPUTPATH)
	# create output file
	outputFile = open(OUTPUTPATH, "w+")

	# cli output
	print "Parsing File .......... "
	# read through file: each line is a card
	for line in inputFile:
		# trim leading whitespace
		line = line.strip()
		# split the line into tokens
		tokens = line.split()
		
		# check first token to get card zone
		if tokens[0] == '//': 			# this line is a comment, ignore
			pass
		elif tokens[0] == "SB:":		# SB: indicates sideboard card
			# create card
			quantity = tokens[1]
			card = Card(getCardNameFromRaw(tokens), quantity)
			# add card to sideboard
			deck.addCard(card, "sb")
		else: 							# else we have a mainboard card
			# create card
			quantity = tokens[0]
			card = Card(getCardNameFromRaw(tokens), quantity)
			# add card to mainboard
			deck.addCard(card, "mb")
	
	# cli output
	print "Writing .cod File ..... "
	# store xml data as string and write to file
	xml = compileDeckToString(deck)
	outputFile.write(xml)
	
	# cli output
	print "Finished."
	
	
#end main

def getCardNameFromRaw(card):
	"getCardNameFromRaw returns the name of the card from a raw line, removing the extra nonsense"
	
	cardName = ""
	
	# determine sideboard or mainboard
	if card[0] == "SB:": 			# sideboard
		card.pop(0)					# remove SB:
		card.pop(0)					# remove quantity
		card.pop(0)					# remove set
	else:
		card.pop(0)					# remove quantity
		card.pop(0)					# remove set
	# create the name string	
	for word in card:
		cardName += word + " "
	# clean up the name
	cardName = cardName.strip()
		
	return cardName
	
#end getCardNameFromRaw

def compileDeckToString(deck):
	"compileDeckToString takes a deck as a list and prints it in cockatrice-xml format as a string"
	
	# header stuff
	deckAsString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	deckAsString += "<cockatrice_deck version=\"1\">\n"
	deckAsString += "<deckname></deckname>\n"
	deckAsString += "<comments></comments>\n"
	deckAsString += "<zone name=\"main\">\n"
	
	# mainboard cards go here
	for card in deck.m_mainboard:
		deckAsString += card.getAsXML()
		deckAsString += "\n"
	
	# close main and open side
	deckAsString += "</zone>"
	deckAsString += "<zone name=\"side\">\n"
	
	# sideboard cards go here
	for card in deck.m_sideboard:
		deckAsString += card.getAsXML()
		deckAsString += "\n"
	
	# closing stuff
	deckAsString += "</zone>\n"
	deckAsString += "</cockatrice_deck>\n"
	
	
	return deckAsString
	
#end compileDeckToString


class Deck:
	
	# class members
	m_mainboard = []
	m_sideboard = []
	
	# class methods
	def __init__(self):
		return
	#end __init__
	
	def addCard(self, card, zone):
		if zone == "mb":
			self.m_mainboard.append(card)
		elif zone == "sb":
			self.m_sideboard.append(card)
		else:
			return "Invalid Zone"
		return "Card Added"
	#end addCard
	
	def printDeck(self):
		print "Mainboard:"
		for card in self.m_mainboard:
			card.printCard()
		print "Sideboard"
		for card in self.m_sideboard:
			card.printCard()
		return
	#end printDeck
	
	def countDeck(self):
		mbCount = 0
		sbCount = 0
		for card in self.m_mainboard:
			mbCount += card.getQuantity()
		for card in self.m_sideboard:
			sbCount += card.getQuantity()
		return "Mainboard: ", mbCount, "Sideboard: ", sbCount
	
#end Deck

class Card:
	
	# class members
	m_name = ""
	m_quantity = 0

	# class methods
	def __init__(self, name, quantity):
		self.m_name = name
		self.m_quantity = quantity
		return
	#end __init__
	
	def printCard(self):
		print self.m_name, ", (", self.m_quantity, ")"
		return
	#end printCard
	
	def getAsXML(self):
		cardString = "<card number=\"" + self.m_quantity + "\" price=\"0\" name=\"" + self.m_name + "\"/>"
		return cardString
	
	def getQuantity(self):
		return int(self.m_quantity)
	#end getQuantity

#end Card
















# Call main
if __name__ == "__main__":
	main()
	
# EOF