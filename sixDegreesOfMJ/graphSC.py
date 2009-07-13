#build the graph and write it to a pickle. 
#
#

import scapi
import igraph
import sys
from logging import log, error, warning, info, debug
import logging
#from numpy import *
# import pygraphviz as pg
import os
from time import sleep


CONSUMER = 'FMTLJvzSO2GcjEwBuGfoKw'
CONSUMER_SECRET = 'Xg9NDHP5FnwgZYXWA2T0Dl6lYuxTzTmKdwhel1MaUmQ'
TOKEN = 'rX3liZEqpYyKrWynPsGnw'
TOKEN_SECRET  = 'MkRMw5iygVrtNThtc6S3hLvVihtDv7mK1KLj7KkXdM'

#The following is a glorious hack 
HIGHESTUSERID = 170300
DUMPREGULARITY = 2000
DUMPFILE = "testdump.pkl"
##end glorious hack
def initScope():
	auth = scapi.authentication.OAuthAuthenticator(CONSUMER, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
	connector = scapi.ApiConnector('api.soundcloud.com', authenticator=auth)
	root = scapi.Scope(connector)
	return root
	
def setLogger():
	'''just set the logger'''
	loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
	                     	  "datefmt":'%d.%m.%y %H:%M:%S',
								"level": logging.DEBUG,
								#"filename":logPath + "musicGrabber.log",
								"filemode":"w"}
	logging.basicConfig(**loggingConfig)
	
# def main():
# 	root = initScope()
# 	#this will take a looooong time, I wonder if I can build the network as I walk the soundcloud userlist...
# 	users = list(root.users())
	


help_message = '''
this package interfaces w/ soundcloud.com to analyze and plot graphs of soundcloud artists/users

by Ben Fields 11/07/2009 (c) 
based heavily on the graph analysis scripts of Kurt Jacobson.

dependencies:
- igraph (http://cneurocvs.rmki.kfki.hu/igraph/)


builds the graph, then saves the graph as a graphml file to completeSCgraph.graphml

periodically saves the partial graph to %s


''', DUMPFILE

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

class graph(object):
	'''G = graph() -> returns a graph object encapsulating an igraph G 
		includeEnds is a bool value to include nodes w/ no actual rdf file (ends)
		*** NOTE includeEnds is disabled permanently ***'''
	def __init__(self):
		setLogger()
		debug("creating graph object...")
		print("creating graph object...")
		self.G = igraph.Graph(directed=True)
		info("call populate() to build graph...")
	
	def addMetaData(self, idx, user):
		self.G.vs[idx]['username'] = user.username
		self.G.vs[idx]['city'] = user.city
		self.G.vs[idx]['permalink'] = user.permalink
		self.G.vs[idx]['description'] = user.description
		self.G.vs[idx]['myspace_name'] = user.myspace_name
		self.G.vs[idx]['country'] = user.country
		self.G.vs[idx]['uri'] = user.uri
		self.G.vs[idx]['discogs_name'] = user.discogs_name
		self.G.vs[idx]['website'] = user.website
		self.G.vs[idx]['followers_count'] = user.followers_count
		self.G.vs[idx]['avatar_url'] = user.avatar_url
		self.G.vs[idx]['followings_count'] = user.followings_count
		self.G.vs[idx]['website_title'] = user.website_title
		self.G.vs[idx]['full_name'] = user.full_name
		self.G.vs[idx]['online'] = user.online
		self.G.vs[idx]['track_count'] = user.track_count
		self.G.vs[idx]['permalink_url'] = user.permalink_url
		self.G.vs[idx]['id'] = user.id

	def populate(self, seed=1, userCap=None):
		'''populate the igraph w/ the userMap from SoundCloud. 
		seed is the user number to start the breadth first walk, defaults to 1.
		userCap is the maximum number of users, if unspecified walk will continue untill exhausted.'''
		debug("starting build")
		print "starting build"
	
		
		self.G.add_vertices(HIGHESTUSERID + 1) #we're ignoring vs[0] so the graph index
		print "added " + str(HIGHESTUSERID + 1) + " vertices to the graph."
		for idx, vert in enumerate(self.G.vs):
			if (idx%DUMPREGULARITY == 0):
				self.G.write(DUMPFILE, format = "pickle")
			#if idx < 100: continue
			sleep(.5)
			root = initScope()
			try:
				currentUser = root.users(idx)
			except scapi.UnknownContentType, err:
				debug("a bit of trouble grabbing content for userID " + str(idx))
				print "a bit of trouble grabbing content for userID " + str(idx)
				continue
			except Exception, err:
				debug("a bit of trouble unexpected trouble grabbing content for userID " + str(idx) + "\nError String Given:: " + str(err))
				print "a bit of trouble unexpected trouble grabbing content for userID " + str(idx) + "\nError String Given:: " + str(err)
				continue
			if currentUser == None:
				debug("no content for userID " + str(idx) + " probably not a valid ID.")
				print "no content for userID " + str(idx) + " probably not a valid ID."
				continue
			self.addMetaData(idx, currentUser)
			sleep(.5)
			root = initScope()
			followingList = list(currentUser.followings())
			page = 1
			#if we recieved a full page, ask for more pages till the number of follows aligns with the metadata
			while(len(followingList) != int(currentUser.followings_count)):
				followingList += list(currentUser.followings(__offset__=(50*page)))
				page += 1
				if (page == 50):
					debug("turned too many pages with user: " + str(idx) + " continuing anyway...")
					print "turned too many pages with user: " + str(idx) + " continuing anyway..."
					break
			debug("about to add " + str(len(followingList)) + " edges to the graph.")
			print "about to add " + str(len(followingList)) + " edges to the graph."
			for following in followingList:
				try:
					self.G.add_edges((vert.index, following['id']))
				except Exception, err:
					debug("Encountered an error adding an edge from " + str(vert.index) + " to " + str(following['id']) + ".\n\tError message: " + str(err) + "\n\t\tcontinuing...")
					print "Encountered an error adding an edge from " + str(vert.index) + " to " + str(following['id']) + ".\n\tError message: " + str(err) + "\n\t\tcontinuing..."

			
		

def main(argv=None):

	loggingConfig = {"format":'%(asctime)s %(levelname)-8s %(message)s',
						"datefmt":'%d.%m.%y %H:%M:%S',
						"level": logging.DEBUG,
						"filename":"soundCloudBuild.log",
						"filemode":"w"}	
	logging.basicConfig(**loggingConfig)
	G = graph()
	G.populate()
	G.g.write("completeSCgraph.graphml", format = "graphml")
	





if __name__ == "__main__":
	sys.exit(main())
