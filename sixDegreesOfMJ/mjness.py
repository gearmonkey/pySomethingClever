#!/usr/bin/env python
# encoding: utf-8
"""
getMJtracksUsers.py

A fairly simple script that queries the soundcloud api users and tracks for string matches to various ways of saying micheal jackson.  
A list of matching users and a dictionary of matching tracks is built (members of the class mjness()) Upon completion the mjness class instance is written to a pickle file.

Created by Benjamin Fields on 2009-07-12.
Copyright (c) 2009 Goldsmith University of London. All rights reserved.
"""

import sys
import os
import cPickle
import scapi

CONSUMER = 'FMTLJvzSO2GcjEwBuGfoKw'
CONSUMER_SECRET = 'Xg9NDHP5FnwgZYXWA2T0Dl6lYuxTzTmKdwhel1MaUmQ'
TOKEN = 'rX3liZEqpYyKrWynPsGnw'
TOKEN_SECRET  = 'MkRMw5iygVrtNThtc6S3hLvVihtDv7mK1KLj7KkXdM'

OUTFILE='mjness.pkl'


def initScope():
	auth = scapi.authentication.OAuthAuthenticator(CONSUMER, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
	connector = scapi.ApiConnector('api.soundcloud.com', authenticator=auth)
	return scapi.Scope(connector)
	

class mjness(object):
	__init__(self):
		self.usersList = []
		self.trackDict = {}
		self.someMJ = [ '"michael jackson"',
						'"king of pop"',
						'"mj"',
						'"micheal jackson"',
						'"michel jackson"',
						'"michaël jackson"',
						'"jackson, michael"',
						'michaeljackson',
						'kingofpop',
						'michealjackson',
						'micheljackson',
						'michaëljackson',
						'jackson,michael',
						'king_of_pop',
						'micheal_jackson',
						'michel_jackson',
						'michaël_jackson',
						'jackson_michael',
						'jacko'	]


def main():
	print 'fetching MJish users...'
	someMJness = mjness()
	# First check for matching users, actually skip this for now
	# for mjstring in someMJness.someMJ:
	# 		root = initScope()
	# 		tmpUsers = list(root.users(q=mjstring))
	# 		for user in tmpUsers:
	# 			someMJness.usersList += [user.id]
	# 		page = 1
	# 		while (len(tmpUsers) == 50):
	# 			tmpUsers = list(root.users(q=mjstring, __offset__=50*page))
	# 			for user in tmpUsers:
	# 				someMJness.usersList += [user.id]
	# 			page += 1
	# 			if page > 20:
	# 				#enough results
	# 				break
	# 	cPickle.dump(someMJness, OUTFILE)
	# 	someMJness.usersList = list(set(someMJness.usersList))
		
	for mjstring in someMJness.someMJ:
			root = initScope()
			tmpTrack = list(root.tracks(q=mjstring, order=hotness))
			for track in tmpTracks:
				someMJness.tmpTrack[track.user-id.id]
			page = 1
			while (len(tmpTracks) == 50):
				tmpTrack = list(root.tracks(q=mjstring,order=hotness,  __offset__=50*page))
				for user in tmpTrack:
					someMJness.tmpTrack += [user.id]
				page += 1
				if page > 20:
					#enough results
					break
		cPickle.dump(someMJness, OUTFILE)
		someMJness.usersList = list(set(someMJness.usersList))


if __name__ == '__main__':
	main()

